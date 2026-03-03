import threading
import time
import webbrowser
import tkinter as tk
import urllib.request
import uvicorn
from backend.main import app

HOST = "127.0.0.1"
PORT = 8000
APP_URL = f"http://{HOST}:{PORT}"

server = None
server_ready = False

def start_server():
    global server
    config = uvicorn.Config(
        app,
        host=HOST,
        port=PORT,
        log_config=None,
        loop="asyncio"
    )
    server = uvicorn.Server(config)
    server.run()

def is_server_up(url, timeout=0.5):
    try:
        with urllib.request.urlopen(url, timeout=timeout):
            return True
    except Exception:
        return False

def wait_until_ready(update_status):
    global server_ready
    update_status("Uruchamianie serwera…")
    for _ in range(120):  # do ~60s
        if is_server_up(APP_URL):
            server_ready = True
            update_status("Gotowe")
            return
        time.sleep(0.5)
    update_status("Błąd startu")

def open_browser():
    webbrowser.open(APP_URL)

def stop_server_and_exit(root):
    # eleganckie zatrzymanie Uvicorna
    try:
        if server:
            server.should_exit = True
    finally:
        root.destroy()

def show_window():
    root = tk.Tk()
    root.title("Employee Manager")
    root.geometry("360x180")
    root.resizable(False, False)

    title = tk.Label(root, text="Status aplikacji", font=("Segoe UI", 12))
    title.pack(pady=10)

    status_var = tk.StringVar(value="Uruchamianie…")
    status = tk.Label(root, textvariable=status_var, font=("Segoe UI", 12))
    status.pack(pady=5)

    def set_status(text):
        status_var.set(text)
        root.update_idletasks()

    btn_open = tk.Button(root, text="Otwórz aplikację", width=22, command=open_browser, state="disabled")
    btn_open.pack(pady=8)

    info = tk.Label(root, text=APP_URL, font=("Segoe UI", 9))
    info.pack(pady=5)

    btn_exit = tk.Button(root, text="Zamknij", width=12, command=lambda: stop_server_and_exit(root))
    btn_exit.pack(pady=8)

    # wątek sprawdzający gotowość
    def monitor():
        wait_until_ready(set_status)
        if server_ready:
            btn_open.config(state="normal")

    threading.Thread(target=monitor, daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    show_window()