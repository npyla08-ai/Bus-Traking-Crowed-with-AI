import sqlite3
import os
import shutil

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

def sync_all_db_files():
    """Keep all SQLite database copies in repository synchronized with the active DB_PATH."""
    try:
        targets = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/vizag_bus.db")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/vizagbus.db")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "vizag_bus.db")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "vizagbus.db")),
        ]
        for dest in targets:
            if os.path.normcase(dest) != os.path.normcase(DB_PATH):
                try:
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copy2(DB_PATH, dest)
                except Exception:
                    pass
    except Exception as e:
        print(f"Database sync notice: {e}")

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
