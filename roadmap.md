# 🛠️ Dood App Development Roadmap (24 Weeks)

**Project Goal:** Build a full-stack mobile + web application (Dood) that connects users with nearby mechanics — even in offline zones — using a scalable, beautiful, and real-time architecture.

**Working Schedule:** 2 hours/day, 5 days/week  
**Tech Stack:**
- **Mobile:** React Native (Expo), Google Maps SDK, Supabase
- **Web (Admin):** Next.js + TypeScript, Supabase
- **Backend:** Supabase (Auth, DB, Realtime, Edge Functions), Python Microservices (as needed)
- **CI/CD & Hosting:** GitHub Actions, Azure, Expo EAS

---

## 🎨 Design Theme: "Rescue Grid"

**Concept:** A smooth, grid-based UI inspired by roadside safety and modern mobility tech.  
- **Primary Colors:** Deep Blue (#1F3B4D), Emergency Red (#E63946), Signal Yellow (#F1C40F)
- **Typography:** Rounded sans-serif fonts (e.g., Inter, Nunito)
- **Icons:** Line-based icons (Lucide or Feather)
- **Mobile Design:** Card UI, swipeable panels, live location overlays
- **Web Design:** Grid dashboard with expandable sidebars, dark/light toggle, map-first layout

---

## 📆 Weekly Breakdown

### **Week 1: Nov 04 – Nov 08**
📦 Project setup: GitHub repo, monorepo layout, CI/CD basics
- Initialize GitHub repo and set up GitHub Actions
- Configure Expo + Next.js boilerplates
- Set up Supabase project

### **Week 2: Nov 11 – Nov 15**
🔐 Authentication
- Implement Supabase Auth (email/password + OAuth)
- Login/signup screens for mobile and web
- Secure routes using RLS and Next.js middleware

### **Week 3: Nov 18 – Nov 22**
🧱 Database Modeling
- Define schema for Users, Mechanics, Services, Requests
- Apply RLS policies
- Test CRUD in Supabase Studio

### **Week 4: Nov 25 – Nov 29**
🖼️ UI Foundation (Mobile)
- Build basic screens: Home, Request Help, Mechanic List
- Setup navigation using React Navigation

### **Week 5: Dec 02 – Dec 06**
🖼️ UI Foundation (Web Admin)
- Build basic dashboard layout in Next.js
- Connect to Supabase tables
- Create forms for viewing/editing mechanic records

### **Week 6: Dec 09 – Dec 13**
📍 Geolocation Integration
- Integrate Google Maps SDK in mobile
- Capture and transmit user/mechanic locations
- Show location map on admin dashboard

### **Week 7: Dec 16 – Dec 20**
⚡ Realtime & Status Updates
- Supabase Realtime for live mechanic updates
- Mobile: show mechanic en route
- Web: track live requests

### **Week 8: Dec 23 – Dec 27**
🆘 Offline SOS System
- Integrate NetInfo + local DB (e.g. SQLite)
- Cache location and queue help requests
- Trigger Supabase Edge Function on reconnect

### **Week 9: Dec 30 – Jan 03**
💬 Mechanic-User Communication
- Implement in-app chat via Supabase or PubNub
- Notify mechanic of incoming help request

### **Week 10: Jan 06 – Jan 10**
💰 Payments (Prototype)
- Setup Razorpay or Stripe test env
- Simulate user payment flow

### **Week 11: Jan 13 – Jan 17**
📸 Profile + Uploads
- Profile image upload via Supabase Storage
- Mechanic KYC photo uploads

### **Week 12: Jan 20 – Jan 24**
🚚 Service Flow Logic
- Finalize request lifecycle (user ↔ mechanic)
- Add ratings & status states

### **Week 13: Jan 27 – Jan 31**
🛠️ Admin Controls (Phase 1)
- Admin CRUD: services, users, complaints
- Filtering, searching, pagination

### **Week 14: Feb 03 – Feb 07**
📱 Mobile Polish (Phase 1)
- Improve UI components
- Error handling and loaders

### **Week 15: Feb 10 – Feb 14**
🌐 Web Polish (Phase 1)
- Refine dashboard UX
- Add charts and reporting (e.g. with Chart.js)

### **Week 16: Feb 17 – Feb 21**
🧪 Testing Setup
- Jest + React Native Testing Library
- Supabase Edge Function unit tests

### **Week 17: Feb 24 – Feb 28**
🔄 Background Jobs
- Add async jobs (e.g. notify mechanic batch)
- Use Supabase Functions or cron logic

### **Week 18: Mar 03 – Mar 07**
🔔 Notifications
- Setup Expo Push Notifications
- Email fallback via Supabase

### **Week 19: Mar 10 – Mar 14**
📦 Offline Caching (Phase 2)
- Cache recent mechanic list, map tiles
- Enable background sync pattern

### **Week 20: Mar 17 – Mar 21**
📊 Analytics & Monitoring
- Add Azure Monitor, basic Supabase usage logs
- Set up basic heatmaps for requests

### **Week 21: Mar 24 – Mar 28**
🛡️ Security Audit
- Review all RLS policies
- Env variable audit and key rotation

### **Week 22: Mar 31 – Apr 04**
🚀 Final UI Polish
- Improve animations, cards, theming
- Build custom map pins and live tracking

### **Week 23: Apr 07 – Apr 11**
📖 Docs & Support
- Internal setup docs (ENV, onboarding)
- Feature glossary for maintainers

### **Week 24: Apr 14 – Apr 18**
🎉 Launch Prep
- Build production mobile apps (EAS)
- Final deployment of web and Supabase schema
- Launch!

