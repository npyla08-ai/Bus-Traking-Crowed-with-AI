import sqlite3
import os

def resolve_db_path() -> str:
    # 1. Check if DB_PATH environment variable is provided
    if os.environ.get("DB_PATH") and os.path.exists(os.environ["DB_PATH"]):
        return os.path.abspath(os.environ["DB_PATH"])
    
    candidates = [
        # database/ directory (monorepo local dev or repo root)
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/vizag_bus.db")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/vizagbus.db")),
        # backend/ directory (production / Render container)
        os.path.abspath(os.path.join(os.path.dirname(__file__), "vizag_bus.db")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "vizagbus.db")),
        # current working directory
        os.path.abspath(os.path.join(os.getcwd(), "database/vizag_bus.db")),
        os.path.abspath(os.path.join(os.getcwd(), "database/vizagbus.db")),
        os.path.abspath(os.path.join(os.getcwd(), "vizag_bus.db")),
        os.path.abspath(os.path.join(os.getcwd(), "vizagbus.db")),
    ]
    for cand in candidates:
        if os.path.exists(cand):
            return cand
    
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "vizag_bus.db"))

DB_PATH = resolve_db_path()

def get_db():
    try:
        from seed import init_db
    except ImportError:
        try:
            from backend.seed import init_db
        except ImportError:
            init_db = None

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if init_db is not None:
        init_db(DB_PATH)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
