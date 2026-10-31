import os
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

from backend.db import (
    fetch_buses,
    fetch_alternatives,
    update_crowd_level,
    save_complaint,
    save_complaint_ticket,
    update_ticket_status,
    fetch_complaints,
    fetch_all_stops,
    fetch_all_routes,
    fetch_route_details,
    fetch_buses_passing_stop,
    fetch_buses_by_number,
    create_new_bus,
)

# Load GEMINI_API_KEY from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(
    title="Vizag Bus AI API",
    description="Smart Public Transport & Fleet Operations API for Greater Visakhapatnam & surrounding areas",
    version="2.0.0"
)

# Allow Frontend (HTML/JS) to call this Backend without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
INDEX_HTML_PATH = os.path.join(FRONTEND_DIR, "index.html")
MANAGEMENT_HTML_PATH = os.path.join(FRONTEND_DIR, "management.html")

# Mount frontend directory for static assets
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/", include_in_schema=False)
def serve_root():
    """Serves the Vizag Bus Commuter Web Application."""
    if os.path.exists(INDEX_HTML_PATH):
        return FileResponse(INDEX_HTML_PATH)
    return {
        "title": "Vizag Bus AI API",
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/management", include_in_schema=False)
@app.get("/admin", include_in_schema=False)
def serve_management():
    """Serves the separate Fleet Management & Control Center Application."""
    if os.path.exists(MANAGEMENT_HTML_PATH):
        return FileResponse(MANAGEMENT_HTML_PATH)
    if os.path.exists(INDEX_HTML_PATH):
        return FileResponse(INDEX_HTML_PATH)
    return {
        "title": "Vizag Bus Management Portal",
        "status": "online"
    }

@app.get("/api")
@app.get("/api/health")
def api_health():
    """API health and system status endpoint."""
    return {
        "status": "online",
        "service": "Vizag Bus Transit API",
        "version": "2.0.0",
        "docs": "/docs",
        "endpoints": [
            "/api/buses",
            "/api/routes",
            "/api/stops",
            "/api/complaints"
        ]
    }


# =========================================================
# REQUEST MODELS
# =========================================================

class CrowdUpdateRequest(BaseModel):
    bus_number: str
    crowd_percentage: int


class ComplaintRequest(BaseModel):
    bus_number: str
    complaint_text: str


class NewBusRequest(BaseModel):
    bus_number: str
    source: str
    destination: str
    current_location: str
    lat: float
    lng: float
    eta_minutes: int
    crowd_percentage: int


class TicketStatusUpdate(BaseModel):
    status: str


# =========================================================
# 1. GET BUSES & SMART SEARCH
# =========================================================

@app.get("/api/buses")
def get_buses(source: str = None, destination: str = None):
    """
    Search buses by source and destination (direct + intermediate route stops),
    or return all active buses in Visakhapatnam when filters are omitted.
    """
    buses = fetch_buses(source, destination)
    alternatives = (
        fetch_alternatives(source, destination)
        if (source and destination)
        else []
    )

    return {
        "buses": buses,
        "alternatives": alternatives
    }


# =========================================================
# 2. BUS ROUTE EXPLORER & STOPS DIRECTORY (NEW FEATURE)
# =========================================================

@app.get("/api/routes")
def get_all_routes():
    """Get list of all 30+ registered Vizag bus lines with route summary."""
    return {
        "routes": fetch_all_routes()
    }


@app.get("/api/routes/{bus_number}")
def get_route_stops(bus_number: str):
    """
    Get full stop-by-stop route sequence, GPS coordinates, distance,
    estimated transit times, and currently active buses for a specific bus number.
    """
    details = fetch_route_details(bus_number)
    return details


@app.get("/api/stops/{stop_name}/buses")
def get_buses_passing_stop_api(stop_name: str):
    """Get all bus numbers that halt at a given stop."""
    return {
        "stop_name": stop_name,
        "buses": fetch_buses_passing_stop(stop_name)
    }


# =========================================================
# 3. SIMULATE COMPUTER VISION CROWD DETECTION
# =========================================================

@app.post("/api/simulate-crowd")
def simulate_crowd(data: CrowdUpdateRequest):
    updated = update_crowd_level(
        data.bus_number,
        data.crowd_percentage
    )

    return {
        "message": "Crowd level updated via CV simulation",
        "data": updated
    }


# =========================================================
# 4. GEMMA AI SMART RECOMMENDATION
# =========================================================

@app.get("/api/ai-recommend")
def ai_recommendation(source: str, destination: str):
    buses = fetch_buses(source, destination)
    alternatives = fetch_alternatives(source, destination)

    if not buses:
        return {
            "recommendation": "No direct or connecting buses found for this route right now."
        }

    prompt = f"""
    You are Vizag Bus AI, a smart public transport assistant for Visakhapatnam.

    A commuter wants to travel from {source} to {destination}.

    Available Buses right now:
    {buses}

    Alternative / Connecting Routes:
    {alternatives}

    Give a short, crisp 3-bullet point answer:

    1. When should I leave? (Calculate based on ETA)
    2. Which bus should I take? (Compare crowd_percentage vs waiting time)
    3. What if my bus is full? (Mention the less-crowded bus or alternative route)
    """

    if not API_KEY or API_KEY == "your_actual_api_key_here":
        best_bus = min(buses, key=lambda b: b.get('crowd_percentage', 100))
        fastest_bus = min(buses, key=lambda b: b.get('eta_minutes', 999))
        return {
            "recommendation": (
                f"• Leave in {fastest_bus['eta_minutes']} mins for "
                f"Bus {fastest_bus['bus_number']} ({fastest_bus['crowd_percentage']}% full), OR wait "
                f"{best_bus['eta_minutes']} mins for "
                f"Bus {best_bus['bus_number']} ({best_bus['crowd_percentage']}% full).\n\n"
                f"• Recommendation: Avoid congested buses. Board Bus {best_bus['bus_number']} "
                f"({best_bus['crowd_percentage']}% full - {best_bus.get('crowd_status', 'Comfortable')}).\n\n"
                f"• Alternative Option: "
                f"{alternatives[0]['route_details'] if alternatives else 'Take connecting city express via NAD or Maddilapalem.'}"
            )
        }

    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt,
        )
        return {
            "recommendation": response.text
        }
    except Exception as e:
        return {
            "recommendation": (
                f"AI Commuter Advice: Board Bus {buses[0]['bus_number']} arriving in {buses[0]['eta_minutes']} mins "
                f"({buses[0]['crowd_status']}). Alternate: Bus {buses[-1]['bus_number']} in {buses[-1]['eta_minutes']} mins. "
                f"(Fallback notice: {str(e)})"
            )
        }


# =========================================================
# 5. STOP SUGGESTIONS & NEAREST STOP
# =========================================================

@app.get("/api/stops")
def get_stops():
    return {
        "stops": fetch_all_stops()
    }


# =========================================================
# 6. FILTER RUNNING BUSES BY BUS NUMBER
# =========================================================

@app.get("/api/buses/number/{bus_number}")
def get_buses_by_line(bus_number: str):
    return {
        "buses": fetch_buses_by_number(bus_number)
    }


# =========================================================
# 7. ADMIN - ADD NEW BUS ROUTE
# =========================================================

@app.post("/api/admin/buses")
def add_bus(data: NewBusRequest):
    create_new_bus(
        data.bus_number,
        data.source,
        data.destination,
        data.current_location,
        data.lat,
        data.lng,
        data.eta_minutes,
        data.crowd_percentage
    )

    return {
        "message": f"Bus {data.bus_number} added successfully to live network"
    }


# =========================================================
# 8. ADMIN - UPDATE TICKET STATUS
# =========================================================

@app.patch("/api/admin/tickets/{ticket_id}")
def update_ticket(ticket_id: str, data: TicketStatusUpdate):
    update_ticket_status(
        ticket_id,
        data.status
    )

    return {
        "message": f"Ticket {ticket_id} updated to {data.status}"
    }


# =========================================================
# 9. SUBMIT COMPLAINT WITH TICKET ID
# =========================================================

@app.post("/api/complaints")
def submit_complaint(data: ComplaintRequest):
    ticket_id = f"TICK-{uuid.uuid4().hex[:6].upper()}"

    # Smart Categorization & Priority Logic
    text = data.complaint_text.lower()

    category = (
        "Overcrowding & Frequency"
        if any(w in text for w in ["crowd", "full", "rush", "standing", "capacity", "no space"])
        else (
            "Rash Driving / Safety"
            if any(w in text for w in ["speed", "rash", "brake", "accident", "signal", "danger", "reckless"])
            else (
                "Route Skip / Delay"
                if any(w in text for w in ["skip", "delay", "late", "missed", "stopped", "not stopping"])
                else "Cleanliness & Maintenance"
            )
        )
    )

    priority = (
        "High"
        if any(w in text for w in ["skip", "safety", "emergency", "accident", "danger", "injury", "police"])
        else "Medium"
    )

    save_complaint_ticket(
        ticket_id,
        data.bus_number,
        data.complaint_text,
        category,
        priority
    )

    return {
        "ticket_id": ticket_id,
        "message": f"Ticket {ticket_id} raised successfully",
        "category": category,
        "priority": priority
    }


# =========================================================
# 10. GET ALL COMPLAINTS
# =========================================================

@app.get("/api/complaints")
def list_complaints():
    return {
        "complaints": fetch_complaints()
    }
