import sqlite3
import os

# Points directly to vizag-bus-AI/database/vizag_bus.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "vizag_bus.db")

def get_db_path() -> str:
    """Dynamically locates SQLite database for local dev or Render containers."""
    if os.environ.get("DB_PATH") and os.path.exists(os.environ["DB_PATH"]):
        return os.path.abspath(os.environ["DB_PATH"])
    
    candidates = [
        os.path.join(BASE_DIR, "database", "vizag_bus.db"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "vizag_bus.db"),
        os.path.join(os.getcwd(), "database", "vizag_bus.db"),
        os.path.join(os.getcwd(), "vizag_bus.db"),
    ]
    for cand in candidates:
        if os.path.exists(cand):
            return os.path.abspath(cand)
    return DB_PATH

def get_connection():
    target_path = get_db_path()
    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row  # Converts rows into easy Python dictionaries
    return conn

# =========================================================================
# 1. BUS STOPS & ROUTE LOOKUPS
# =========================================================================

def fetch_all_stops():
    """Get all 70+ bus stops in Visakhapatnam ordered alphabetically."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus_stops ORDER BY stop_name ASC")
    stops = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return stops

def fetch_all_routes():
    """Get list of all registered bus lines in Visakhapatnam."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus_routes ORDER BY bus_number ASC")
    routes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return routes

def fetch_route_details(bus_number):
    """
    Get full details for a bus line:
    - Route metadata (Origin, Destination, via, frequency, fare, timings)
    - Full sequential list of all stops along this route with GPS coords
    - Active running buses currently live on this line
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Route info
    cursor.execute("SELECT * FROM bus_routes WHERE LOWER(bus_number) = LOWER(?)", (bus_number,))
    route_row = cursor.fetchone()
    route_info = dict(route_row) if route_row else None

    # Ordered stops with coords
    cursor.execute("""
        SELECT rs.bus_number, rs.stop_sequence, rs.stop_name, rs.distance_km, rs.eta_from_start_mins,
               bs.lat, bs.lng, bs.area, bs.landmark
        FROM route_stops rs
        LEFT JOIN bus_stops bs ON rs.stop_name = bs.stop_name
        WHERE LOWER(rs.bus_number) = LOWER(?)
        ORDER BY rs.stop_sequence ASC
    """, (bus_number,))
    stops = [dict(row) for row in cursor.fetchall()]

    # Active running buses on this line
    cursor.execute("SELECT * FROM buses WHERE LOWER(bus_number) = LOWER(?) ORDER BY eta_minutes ASC", (bus_number,))
    active_buses = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        "route": route_info,
        "stops": stops,
        "active_buses": active_buses
    }

def fetch_buses_passing_stop(stop_name):
    """Get all bus numbers that halt at a given stop."""
    conn = get_connection()
    cursor = conn.cursor()
    search_term = f"%{stop_name.strip()}%"
    cursor.execute("""
        SELECT rs.bus_number, rs.stop_sequence, br.route_name, br.source, br.destination,
               br.via, br.bus_type, br.frequency_mins, br.fare_min, br.fare_max
        FROM route_stops rs
        JOIN bus_routes br ON rs.bus_number = br.bus_number
        WHERE LOWER(rs.stop_name) LIKE LOWER(?)
        ORDER BY rs.bus_number ASC
    """, (search_term,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

# =========================================================================
# 2. RUNNING BUS SEARCH & MULTIMODAL ALTERNATIVES
# =========================================================================

def fetch_buses(source=None, destination=None):
    """
    Smart transit finder:
    - If source and destination are given:
      1. Direct terminal matching buses (e.g. source -> destination)
      2. ANY bus route where source appears before destination in route_stops!
         (e.g., searching NAD Junction to Siripuram finds 400K, 38, etc.)
    - If not given, returns all active live buses.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if source and destination:
        s_term = f"%{source.strip()}%"
        d_term = f"%{destination.strip()}%"
        # Also clean tokens (e.g. 'Gajuwaka Junction' -> 'Gajuwaka')
        s_token = f"%{source.strip().split()[0]}%"
        d_token = f"%{destination.strip().split()[0]}%"

        # 1. Find bus numbers that have both stops in sequence in route_stops
        cursor.execute("""
            SELECT DISTINCT rs1.bus_number
            FROM route_stops rs1
            JOIN route_stops rs2 ON rs1.bus_number = rs2.bus_number
            WHERE (LOWER(rs1.stop_name) LIKE LOWER(?) OR LOWER(rs1.stop_name) LIKE LOWER(?))
              AND (LOWER(rs2.stop_name) LIKE LOWER(?) OR LOWER(rs2.stop_name) LIKE LOWER(?))
              AND rs1.stop_sequence < rs2.stop_sequence
        """, (s_term, s_token, d_term, d_token))
        matching_lines = [row["bus_number"] for row in cursor.fetchall()]

        # 2. Query active buses that either run on these lines OR have matching endpoints
        if matching_lines:
            placeholders = ",".join(["?"] * len(matching_lines))
            cursor.execute(f"""
                SELECT * FROM buses
                WHERE bus_number IN ({placeholders})
                   OR (
                        (LOWER(source) LIKE LOWER(?) OR LOWER(source) LIKE LOWER(?))
                        AND (LOWER(destination) LIKE LOWER(?) OR LOWER(destination) LIKE LOWER(?))
                   )
                ORDER BY eta_minutes ASC
            """, (*matching_lines, s_term, s_token, d_term, d_token))
        else:
            cursor.execute("""
                SELECT * FROM buses
                WHERE (LOWER(source) LIKE LOWER(?) OR LOWER(source) LIKE LOWER(?))
                  AND (LOWER(destination) LIKE LOWER(?) OR LOWER(destination) LIKE LOWER(?))
                ORDER BY eta_minutes ASC
            """, (s_term, s_token, d_term, d_token))

        rows = [dict(row) for row in cursor.fetchall()]
    else:
        cursor.execute("SELECT * FROM buses ORDER BY eta_minutes ASC")
        rows = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return rows

def fetch_buses_by_number(bus_number):
    """Get all active running bus instances for a bus line number."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buses WHERE LOWER(bus_number) = LOWER(?) ORDER BY eta_minutes ASC", (bus_number,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def fetch_alternatives(source, destination):
    """Get multimodal/connecting route options for a route."""
    conn = get_connection()
    cursor = conn.cursor()
    s_key = source.split()[0]
    d_key = destination.split()[0]
    cursor.execute("""
        SELECT * FROM alternative_routes
        WHERE (LOWER(source) LIKE LOWER(?) OR LOWER(source) LIKE LOWER(?))
          AND (LOWER(destination) LIKE LOWER(?) OR LOWER(destination) LIKE LOWER(?))
    """, (f"%{source}%", f"%{s_key}%", f"%{destination}%", f"%{d_key}%"))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

# =========================================================================
# 3. LIVE FLEET & CROWD LEVEL UPDATES (CV SIMULATOR)
# =========================================================================

def update_crowd_level(bus_number, crowd_percentage):
    """Update bus occupancy (used for Computer Vision crowd simulation)."""
    if crowd_percentage >= 75:
        status = "Overcrowded"
    elif crowd_percentage >= 45:
        status = "Moderate"
    else:
        status = "Comfortable"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE buses
        SET crowd_percentage = ?, crowd_status = ?
        WHERE bus_number = ?
    """, (crowd_percentage, status, bus_number))
    conn.commit()
    conn.close()
    return {"bus_number": bus_number, "crowd_percentage": crowd_percentage, "crowd_status": status}

def create_new_bus(bus_number, source, destination, current_location, lat, lng, eta_minutes, crowd_percentage):
    """Admin function to add a newly dispatched bus to the active fleet."""
    status = "Overcrowded" if crowd_percentage >= 75 else ("Moderate" if crowd_percentage >= 45 else "Comfortable")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO buses (bus_number, source, destination, current_location, lat, lng, eta_minutes, crowd_percentage, crowd_status, next_bus_eta, speed_kmh, bus_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 32, 'Metro Express')
    """, (bus_number, source, destination, current_location, lat, lng, eta_minutes, crowd_percentage, status, eta_minutes + 15))
    conn.commit()
    conn.close()

# =========================================================================
# 4. COMPLAINTS & GRIEVANCE TICKETS
# =========================================================================

def save_complaint(bus_number, complaint_text, ai_category="Pending", ai_priority="Medium"):
    """Legacy helper for saving complaint without ticket_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO complaints (bus_number, complaint_text, ai_category, ai_priority)
        VALUES (?, ?, ?, ?)
    """, (bus_number, complaint_text, ai_category, ai_priority))
    conn.commit()
    conn.close()

def save_complaint_ticket(ticket_id, bus_number, complaint_text, ai_category, ai_priority):
    """Save a commuter complaint with auto-generated Ticket ID and AI priority."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO complaints (ticket_id, bus_number, complaint_text, ai_category, ai_priority, status)
        VALUES (?, ?, ?, ?, ?, 'Open')
    """, (ticket_id, bus_number, complaint_text, ai_category, ai_priority))
    conn.commit()
    conn.close()

def update_ticket_status(ticket_id, new_status):
    """Admin function to resolve or update a commuter ticket."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    conn.close()

def fetch_complaints():
    """Get all complaints ordered by newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
