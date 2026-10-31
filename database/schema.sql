DROP TABLE IF EXISTS buses;
DROP TABLE IF EXISTS bus_stops;
DROP TABLE IF EXISTS bus_routes;
DROP TABLE IF EXISTS route_stops;
DROP TABLE IF EXISTS alternative_routes;
DROP TABLE IF EXISTS complaints;

-- 1. Bus Stops Table (For Nearest Bus Stop Finder, Autocomplete & Map Plots)
CREATE TABLE bus_stops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stop_name TEXT NOT NULL UNIQUE,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    area TEXT,
    landmark TEXT
);

-- 2. Bus Routes Table (Master registry of all Vizag bus routes)
CREATE TABLE bus_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number TEXT NOT NULL UNIQUE,
    route_name TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    via TEXT NOT NULL,
    bus_type TEXT DEFAULT 'Metro Express',
    frequency_mins INTEGER DEFAULT 15,
    first_bus_time TEXT DEFAULT '05:30 AM',
    last_bus_time TEXT DEFAULT '10:30 PM',
    fare_min INTEGER DEFAULT 10,
    fare_max INTEGER DEFAULT 35,
    total_stops INTEGER DEFAULT 0
);

-- 3. Route Stops Table (Ordered list of stops for each bus route)
CREATE TABLE route_stops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number TEXT NOT NULL,
    stop_sequence INTEGER NOT NULL,
    stop_name TEXT NOT NULL,
    distance_km REAL DEFAULT 0.0,
    eta_from_start_mins INTEGER DEFAULT 0
);

-- 4. Buses Table (Live Running Fleet instances with Real-time GPS & Occupancy)
CREATE TABLE buses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    current_location TEXT NOT NULL,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    eta_minutes INTEGER NOT NULL,
    crowd_percentage INTEGER NOT NULL,
    crowd_status TEXT NOT NULL,
    next_bus_eta INTEGER NOT NULL,
    speed_kmh INTEGER DEFAULT 32,
    bus_type TEXT DEFAULT 'Metro Express'
);

-- 5. Alternative Routes Table (Multimodal and Connecting Routes)
CREATE TABLE alternative_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    option_type TEXT NOT NULL,
    route_details TEXT NOT NULL,
    total_time_mins INTEGER NOT NULL
);

-- 6. Complaints & AI Ticket Management Table
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL UNIQUE,
    bus_number TEXT NOT NULL,
    complaint_text TEXT NOT NULL,
    ai_category TEXT DEFAULT 'Pending',
    ai_priority TEXT DEFAULT 'Medium',
    status TEXT DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
