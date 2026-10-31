# Vizag Bus AI – Smart Public Transport & Route Explorer

An intelligent public transit and real-time fleet operations portal for the **Greater Visakhapatnam Municipal Corporation (GVMC)** and surrounding suburban areas (Anakapalle, Bheemunipatnam, Pendurthi, Kothavalasa, Atchutapuram, Desapatrunipalem).

---

## 🚀 Key Features

### 1. 🚏 Bus Route & Stops Explorer (Look Up by Bus Number)
* **Search any Bus Number** (e.g., `400K`, `900K`, `28A`, `38`, `222`, `500`, `60C`, `88K`, `111`, etc.) to view its complete ordered route stops from Origin to Destination.
* **Stop-by-Stop Stepper**: Displays sequential order, distance (km), estimated arrival time from start (+mins), area, and landmark.
* **Real-time Live Radar on Stops**: Highlights if a running bus is currently approaching or passing that stop, with ETA and crowd occupancy.
* **Interactive Map Trace**: Draws the complete route polyline connecting every stop with numbered pins and glowing live bus markers.
* **APSRTC Fare Range**: Shows estimated fares (`₹10 – ₹35`), operating hours, and dispatch frequency.

### 2. 🏛️ Vizag Stop Directory ("Which Buses Halt Here?")
* Select from **70+ geolocated stops** across Greater Visakhapatnam.
* Instantly view every bus line halting at that stop, including its destination, frequency, and stop sequence.
* Direct one-click jump to inspect the full route.

### 3. 🎯 Smart Journey Planner (Direct + Intermediate Search)
* Unlike basic terminal matching, the smart transit search identifies **intermediate stop connectivity**. For example, searching **NAD Junction ➔ Siripuram** finds all lines (`400K`, `38`, `400`, `38A`, etc.) that connect both stops in sequence.
* Provides **multimodal connecting options** (connecting bus routes, shared auto + express bus combos, feeder routes).
* **Instant Commuter Route & Fare Summary**: Fast, deterministic transit calculations showing fastest departure, least-crowded bus, and estimated APSRTC fare.

### 4. ⚡ Live Fleet Radar Simulation & Corridor Filters
* Live tracking of **57 running buses** across Greater Visakhapatnam.
* **⚡ Live Simulation Toggle**: Auto-refresh and live fleet radar pulse every 10 seconds.
* Quick corridor filter tabs: **All GVMC**, **South / Gajuwaka**, **Beach Road**, **Simhachalam / West**, **Madhurawada / North**, and **Central Vizag**.
* Real-time crowd occupancy indicators: **Comfortable (<45%)**, **Moderate (45–74%)**, and **Overcrowded (75%+)**.

### 5. 🚨 24x7 Transit SOS & Emergency Helplines
* Instant one-tap access to 24/7 helplines across Greater Visakhapatnam:
  * APSRTC Central Enquiry (Toll-Free): `0866-2570005` / `149`
  * Dwaraka Bus Station (RTC Complex) Control: `0891-2746400`
  * Vizag City Police / Disha SOS: `112` / `100`
  * Women Safety Helpline: `181`
  * GVMC Citizen Grievance Toll-Free: `1800-425-00001`

### 6. 🌐 Telugu (తెలుగు) Bilingual Support
* Quick header toggle (`🌐 తెలుగు / EN`) offering authentic local Telugu names for major Visakhapatnam stops and transit hubs (ద్వారకా బస్ కాంప్లెక్స్, గాజువాక, ఎన్.ఎ.డి జంక్షన్, మద్దిలపాలెం, సిరిపురం, etc.).

### 7. 📍 Geolocation & Nearest Stop Finder
* **Locate Me**: Pins the user's location with animated radar pulse (defaults to Siripuram if location permissions are denied).
* **Nearest Bus Stop**: Uses the Haversine formula to find the closest of 70+ stops with walking distance and estimated walk time.

### 8. 🎫 Commuter Grievance & Auto-Ticket Dispatch
* Commuters can report issues (overcrowding, delays, skipped stops, rash driving).
* Automatic priority and category classification with unique tracking tickets (e.g., `TICK-XXXXXX`).
* One-click ticket copy button (`📋 Copy Ticket ID`) for easy tracking.

### 9. 🔐 Fleet Management Portal (Control Center)
* Secure manager login (`User ID: admin`, `Password: admin123`).
* **Dispatch New Bus Route**: Add running buses with quick coordinate fill presets for Vizag stops.
* **Live Camera Crowd Simulator**: Simulates real-time computer vision passenger occupancy updates.
* **Ticket Queue Management**: Review and resolve commuter grievances.

---

## 🗄️ Database Architecture

The SQLite database (`database/vizag_bus.db`) contains 6 core relational tables:
1. `bus_stops`: 70+ major Vizag stops with precise latitude, longitude, area, and landmark.
2. `bus_routes`: 30 master bus route lines with source, destination, via, bus type, frequency, timings, and fares.
3. `route_stops`: 266 mapped stop sequences linking bus routes to their ordered stops, distances (km), and ETAs.
4. `buses`: 57 live running fleet instances with real-time GPS coordinates, current location, ETA, and crowd percentage.
5. `alternative_routes`: Multimodal connecting route options.
6. `complaints`: Grievance queue with auto-generated ticket IDs and status tracking.

---

## 🛠️ Getting Started

### 1. Requirements
* Python 3.10+
* Dependencies:
  ```bash
  pip install fastapi uvicorn google-genai python-dotenv
  ```

### 2. Initialize / Seed Database
To recreate the schema and seed all 70+ stops, 30 routes, and 57 active buses:
```bash
python database/seed_data.py
```

### 3. Run Application (Backend + Frontend)
```bash
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
* **Web App (Interactive UI)**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **API Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **API Health Check**: [http://127.0.0.1:8000/api](http://127.0.0.1:8000/api)

*(Optional: You can also double-click `frontend/index.html` to open it directly in any browser)*

---

## 🔑 Default Manager Credentials
* **User ID**: `admin`
* **Password**: `admin123`
*(Configurable inside `frontend/index.html` under `MANAGER_CREDENTIALS`)*
