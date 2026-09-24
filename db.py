"""SQLite-backed storage for employee records.

Deliberately minimal — no ORM, just the stdlib `sqlite3` module, since the
schema is one flat table and the app has no other persistence needs.
`main.active_tokens` intentionally stays in-memory rather than moving here:
bearer tokens are short-lived (10-minute TTL) session state, not data
anyone expects — or wants — to survive a server restart.

A new connection is opened per call rather than sharing one across
requests. FastAPI runs these sync functions in a threadpool, and a single
sqlite3.Connection isn't safe to share across threads; a fresh
short-lived connection per call sidesteps that entirely, and SQLite's own
file-level locking (helped along by WAL mode + a busy_timeout below)
handles the rest.
"""

import os
import sqlite3
import sys
from pathlib import Path

_APP_NAME = "EmployeeManager"


def _default_db_dir() -> Path:
    """The directory employees.db lives in when DB_PATH isn't set."""
    if not getattr(sys, "frozen", False):
        # Source checkout: keep the database next to the code, where a
        # developer expects to find it (and to be able to delete it).
        return Path(__file__).resolve().parent

    # Packaged build (PyInstaller). Two tempting directories are both wrong:
    #
    #   - sys._MEIPASS (used for read-only bundled assets — see STATIC_DIR in
    #     main.py) is a fresh temp extraction directory every launch, so a
    #     database written there silently vanishes on the next start.
    #   - the directory holding sys.executable, which is what this module
    #     used before. On macOS that's run.app/Contents/MacOS — *inside* the
    #     bundle. Writing there breaks the code signature's sealed resources
    #     on first launch (`codesign --verify --deep --strict` then reports
    #     "a sealed resource is missing or invalid"), and fails outright once
    #     the app sits in /Applications or runs translocated from a
    #     read-only mount.
    #
    # Use the per-user data directory each platform reserves for this, so the
    # database is writable and persists across launches without the app ever
    # modifying itself.
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / _APP_NAME
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local"
        return Path(base) / _APP_NAME
    base = os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share"
    return Path(base) / _APP_NAME


# Overridable via env var — e.g. tests point this at an isolated, throwaway
# file (see tests/conftest.py) so pytest runs never touch a real
# employees.db a developer might have sitting next to the app.
DB_PATH = Path(os.environ.get("DB_PATH", _default_db_dir() / "employees.db"))


def _connect() -> sqlite3.Connection:
    # On a packaged build's first run the per-user data directory above won't
    # exist yet, and sqlite3 won't create a missing parent for us — it just
    # raises "unable to open database file". Cheap no-op once it's there.
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the employees table if it doesn't exist yet. Safe to call on every startup."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                salary INTEGER NOT NULL,
                age INTEGER NOT NULL,
                position TEXT NOT NULL,
                on_leave INTEGER NOT NULL
            )
            """
        )


def next_id() -> int:
    """The id the next inserted employee should get: 1, or max(id) + 1.

    Called once at startup to seed main.current_id from whatever's already
    on disk, so restarting the app doesn't hand out an id that collides
    with an employee created before the restart.
    """
    with _connect() as conn:
        row = conn.execute("SELECT MAX(id) AS max_id FROM employees").fetchone()
        return (row["max_id"] or 0) + 1


def list_employees() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM employees ORDER BY id").fetchall()
        return [_row_to_dict(row) for row in rows]


def insert_employee(emp_id: int, data: dict) -> dict:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO employees (id, name, salary, age, position, on_leave) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                emp_id,
                data["name"],
                data["salary"],
                data["age"],
                data["position"],
                int(data["on_leave"]),
            ),
        )
    return {"id": emp_id, **data}


def update_employee(emp_id: int, data: dict) -> dict | None:
    """Update an existing employee. Returns the updated row, or None if emp_id doesn't exist."""
    with _connect() as conn:
        cursor = conn.execute(
            "UPDATE employees SET name = ?, salary = ?, age = ?, position = ?, on_leave = ? "
            "WHERE id = ?",
            (
                data["name"],
                data["salary"],
                data["age"],
                data["position"],
                int(data["on_leave"]),
                emp_id,
            ),
        )
        if cursor.rowcount == 0:
            return None

    return {"id": emp_id, **data}


def delete_employee(emp_id: int) -> bool:
    """Delete an employee. Returns whether a row was actually deleted."""
    with _connect() as conn:
        cursor = conn.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        return cursor.rowcount > 0


def reset_employees() -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM employees")


def _row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "salary": row["salary"],
        "age": row["age"],
        "position": row["position"],
        "on_leave": bool(row["on_leave"]),
    }
