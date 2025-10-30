'''
WorkerStateMachineStack
Implements the improved 'Classandra Data Pipeline' Step Functions worker.

| Version | Date       | Author           | Notes                                                                  |
|---------|------------|------------------|------------------------------------------------------------------------|
| v1.10   | 2025-08-18 | Mohammad Rohan   | Add event normalization                                                |
| v1.0    | 2025-08-18 | Mohammad Rohan   | Fixed ordering, event-driven config injection                          |
'''

from aws_cdk import (
    Stack, Duration, RemovalPolicy,
    aws_logs as logs,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)
from constructs import Construct
import yaml
from pathlib import Path

LAMBDA_CONFIG_PATH = Path(__file__).parent.parent / "lambda" / "config" / "lambda_config.yaml"

class WorkerStateMachineStack(Stack):
    """
    Implements the improved 'Classandra Data Pipeline' Step Functions worker.

    Assumptions:
    - EventBridge rule passes only the event ' into the state machine
      (RuleTargetInput.from_event_path('$')), so JSONPaths start at '$'.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- Load lambda_config.yaml ---
        with open(LAMBDA_CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)

        # --- Extract Step Function lambdas ---
        sm_lambda_names = {}
        for category in config.get("lambdas", []):
            if category.get("category") == "statemachine":
                for l in category.get("lambdas", []):
                    name = l["lambda_name"]
                    sm_lambda_names[name] = _lambda.Function.from_function_name(
                        self, f"{name}Ref", name
                    )

        update_case_fn = sm_lambda_names["update_case"]
        create_case_fn = sm_lambda_names["create_case"]
        translate_case_fn = sm_lambda_names["translate_case"]
        classify_case_fn = sm_lambda_names["classify_case"]

        # --- Failure sink ---
        record_failure = sfn.Fail(self, "Record Failure")

        # --- Helper for LambdaInvoke ---
        def lambda_task(title: str, fn: _lambda.IFunction, result_path: str) -> tasks.LambdaInvoke:
            t = tasks.LambdaInvoke(
                self, title,
                lambda_function=fn,
                payload=sfn.TaskInput.from_object({"detail.$": "$"}),
                payload_response_only=True,
                result_path=result_path,
                task_timeout=sfn.Timeout.duration(Duration.seconds(60)),
            )
            # Common retries
            t.add_retry(
                # add more error types here depending on whether they should be retried automatically.
                errors=[
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException",
                ],
                interval=Duration.seconds(1),
                max_attempts=3,
                backoff_rate=2.0,
            )
            # Catch all → failure branch
            t.add_catch(record_failure, result_path="$.error")
            return t

        # --- Lambda tasks ---
        update_cases = lambda_task("Update Cases", update_case_fn, "$.update_result")
        update_cases.add_retry(
            errors=["EventLagRetry"], interval=Duration.seconds(10),
            max_attempts=3, backoff_rate=2.0,
        )

        insert_new_cases = lambda_task("Insert New Cases", create_case_fn, "$.create_result")
        translate_data = lambda_task("Translate Data", translate_case_fn, "$.translate_result")
        classify_data = lambda_task("Classify Data", classify_case_fn, "$.classify_result")

        # --- Terminal states ---
        done = sfn.Succeed(self, "Done")
        skip_classification = sfn.Succeed(self, "Skip Classification")
        skip_translation = sfn.Succeed(self, "Skip Translation")
        after_update = sfn.Succeed(self, "After Update")
        unknown_change = sfn.Succeed(self, "Unknown ChangeType")

        # --- Choice: Run Classification ---
        choice_classification = sfn.Choice(self, "Choice - Run Classification")
        choice_classification.when(
            sfn.Condition.and_(
                sfn.Condition.number_equals("$.translate_result.statusCode", 200),
                # sfn.Condition.is_present("$.Description"),
                # sfn.Condition.is_present("$.OwnerId"),
                # sfn.Condition.is_present("$.RecordTypeId"),
            ),
            classify_data.next(done),
        ).otherwise(skip_classification)

        # --- Choice: Run Translation ---
        choice_translation = sfn.Choice(self, "Choice - Run Translation")
        choice_translation.when(
            sfn.Condition.and_(
                sfn.Condition.number_equals("$.create_result.statusCode", 200),
                # sfn.Condition.is_present("$.Description"),
            ),
            translate_data.next(choice_classification),
        ).otherwise(skip_translation)

        # --- Choice: Change Event type ---
        choice_change_event = sfn.Choice(self, "Choice - Change Event")
        choice_change_event.when(
            sfn.Condition.string_equals("$.ChangeEventHeader.changeType", "UPDATE"),
            update_cases.next(after_update),
        ).when(
            sfn.Condition.string_equals("$.ChangeEventHeader.changeType", "CREATE"),
            insert_new_cases.next(choice_translation),
        ).otherwise(unknown_change)

        # --- Definition: inject → choose ---
        definition = choice_change_event

        # --- State Machine ---
        log_group = logs.LogGroup(self, "WorkerLogs", removal_policy=RemovalPolicy.DESTROY)

        self.state_machine = sfn.StateMachine(
            self, "ClassandraDataPipeline",
            definition_body=sfn.DefinitionBody.from_chainable(definition),
            logs=sfn.LogOptions(
                destination=log_group,
                level=sfn.LogLevel.ALL,
                include_execution_data=True,
            ),
            tracing_enabled=True,
            timeout=Duration.minutes(5),
        )
