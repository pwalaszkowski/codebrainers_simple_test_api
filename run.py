import logging
import threading
import time
import tkinter as tk
import urllib.request
import webbrowser
from tkinter import ttk
from urllib.parse import urlparse

import uvicorn

from main import app

logger = logging.getLogger(__name__)

HOST = "127.0.0.1"
PORT = 8000
APP_URL = f"http://{HOST}:{PORT}"

server = None
server_ready = False


# -------------------------
# SERVER
# -------------------------
def start_server():
    global server

    config = uvicorn.Config(app, host=HOST, port=PORT, log_config=None, loop="asyncio")

    server = uvicorn.Server(config)
    server.run()


def is_server_up(url, timeout=0.5):
    scheme = urlparse(url).scheme
    if scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {scheme!r}")

    # Scheme validated above; url is always the local APP_URL constant, not user input.
    try:
        with urllib.request.urlopen(url, timeout=timeout):  # nosec B310
            return True
    except OSError:
        return False


def wait_until_ready(update_status, enable_button):
    global server_ready

    update_status("⏳ Uruchamianie serwera...")

    for _ in range(120):
        if is_server_up(APP_URL):
            server_ready = True

            update_status("✅ Aplikacja gotowa")


            return

        time.sleep(0.5)

    update_status("❌ Błąd uruchamiania")


# -------------------------
# ACTIONS
# -------------------------
def open_browser():
    webbrowser.open(APP_URL)


def stop_server_and_exit(root):

    try:
        if server:
            server.should_exit = True

    finally:
        root.destroy()


# -------------------------
# UI
# -------------------------
def show_window():

    root = tk.Tk()

    root.title("Employee Manager")
    root.geometry("800x600")
    root.resizable(False, False)

    # ---------- COLORS ----------
    BG = "#0f1115"
    CARD = "#161a22"
    TEXT = "#e5e7eb"
    MUTED = "#9ca3af"
    ACCENT = "#ff8c00"

    root.configure(bg=BG)

    # ---------- CARD ----------
    card = tk.Frame(root, bg=CARD, bd=0, highlightthickness=0)

    card.place(relx=0.5, rely=0.5, anchor="center", width=430, height=240)

    # ---------- LOGO ----------
    logo = tk.Label(
        card,
        text="</> Employee Manager",
        bg=CARD,
        fg=ACCENT,
        font=("Segoe UI", 15, "bold"),
    )

    logo.pack(pady=(20, 10))

    # ---------- TITLE ----------
    title = tk.Label(
        card, text="Status aplikacji", bg=CARD, fg=TEXT, font=("Segoe UI", 18, "bold")
    )

    title.pack(pady=(5, 15))

    # ---------- STATUS ----------
    status_var = tk.StringVar(value="Uruchamianie...")

    status = tk.Label(
        card, textvariable=status_var, bg=CARD, fg=MUTED, font=("Segoe UI", 12)
    )

    status.pack(pady=(0, 20))

    # ---------- BUTTONS ----------
    style = ttk.Style()

    try:
        style.theme_use("clam")
    except Exception:
        logger.debug("ttk theme 'clam' unavailable, using default theme", exc_info=True)

    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=10)

    btn_open = ttk.Button(
        card,
        text="🌐 Otwórz aplikację",
        command=open_browser,
        state="disabled",
        style="Accent.TButton",
    )

    btn_open.pack(pady=8)

    # ---------- URL ----------
    info = tk.Label(card, text=APP_URL, bg=CARD, fg=MUTED, font=("Consolas", 10))

    info.pack(pady=(10, 20))

    # ---------- CLOSE ----------
    btn_exit = ttk.Button(
        card, text="Zamknij", command=lambda: stop_server_and_exit(root)
    )

    btn_exit.pack()

    # ---------- HELPERS ----------
    def set_status(text):

        status_var.set(text)

        root.update_idletasks()

    def enable_open_button():

        btn_open.config(state="normal")

    # ---------- MONITOR ----------
    def monitor():

        wait_until_ready(set_status, enable_open_button)

    threading.Thread(target=monitor, daemon=True).start()

    root.mainloop()


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()

    show_window()
