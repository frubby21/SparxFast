import pyautogui
from google import genai
from PIL import Image
import time
import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import requests
import subprocess
import threading

APP_NAME = "SparxFast"
VERSION = "1.0.4"

GITHUB_RAW_VERSION_URL = "https://raw.githubusercontent.com/frubby21/SparxFast/refs/heads/main/version.json"
GITHUB_INSTALLER_URL = "https://github.com/frubby21/SparxFast/raw/refs/heads/main/apps/SparxFastSetup.exe"

# PATH CONFIG
BASE_DIR = os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), APP_NAME)
LOG_FILE = os.path.join(BASE_DIR, "sparx.log")
SCREENSHOT_PATH = os.path.join(BASE_DIR, "sparx_capture.png")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
HUB_REGISTRY = os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), "flobby25 Hub", "installed_apps.json")

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR, exist_ok=True)

# --- CONFIG HELPERS ---

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except: pass
    return {"key": None, "always_on_top": True}

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def is_managed_by_hub():
    """Checks the Hub registry for this specific app name."""
    if os.path.exists(HUB_REGISTRY):
        try:
            with open(HUB_REGISTRY, "r") as f:
                data = json.load(f)
                return APP_NAME in data.get("apps", [])
        except: return False
    return False

# --- LOGIC ---

def check_for_self_update(status_label):
    if is_managed_by_hub(): return 
    try:
        response = requests.get(GITHUB_RAW_VERSION_URL, timeout=5)
        remote_version = response.json().get("version")
        if remote_version != VERSION:
            if messagebox.askyesno("Update", f"v{remote_version} available. Download and install?"):
                status_label.config(text="Downloading...", foreground="#ffa500")
                r = requests.get(GITHUB_INSTALLER_URL, stream=True)
                temp_path = os.path.join(os.environ['TEMP'], "SparxFastSetup.exe")
                with open(temp_path, 'wb') as f:
                    for chunk in r.iter_content(8192): f.write(chunk)
                subprocess.Popen([temp_path, "/SILENT", "/SP-"])
                os._exit(0)
    except: pass

def search_log(code):
    if not os.path.exists(LOG_FILE):
        messagebox.showinfo("Error", "No log file found. Solve a question first.")
        return
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for entry in f.read().split('-'*40):
            if f"CODE: {code.upper()}" in entry.upper():
                messagebox.showinfo(f"History: {code}", entry.strip())
                return
    messagebox.showwarning("Not Found", f"Code {code} not found in logs. Check your input.")

def solve_task(config, status_label, root):
    if not config.get("key"):
        messagebox.showerror("Error", "No Gemini API key found. Please enter one in Settings.")
        return
    
    status_label.config(text="Capturing...", foreground="#00ffcc")
    root.update()
    
    time.sleep(2)
    x1, y1 = pyautogui.position()
    time.sleep(2)
    x2, y2 = pyautogui.position()
    
    try:
        width, height = x2 - x1, y2 - y1
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        screenshot.save(SCREENSHOT_PATH)
        
        client = genai.Client(api_key=config["key"])
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=["Identify Bookwork Code. Solve math. Format: CODE: [Code] ANSWER: [Answer] STEPS: [1-sentence]", Image.open(SCREENSHOT_PATH)]
        )
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{response.text}\n{'-'*40}")
        messagebox.showinfo("Solution", response.text)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        status_label.config(text="System Ready", foreground="white")

# --- SETTINGS WINDOW ---

def open_settings(root, current_config):
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("280x160")
    settings_win.attributes("-topmost", True)
    settings_win.grab_set()

    tk.Label(settings_win, text="App Settings", font=("Arial", 10, "bold")).pack(pady=10)

    # API Key Button
    def update_key():
        new_key = simpledialog.askstring("API Key", "Enter Gemini API Key:", initialvalue=current_config.get("key", ""))
        if new_key:
            current_config["key"] = new_key
            save_config(current_config)

    tk.Button(settings_win, text="Change Gemini Key", command=update_key, width=20).pack(pady=5)

    # Always On-Top Toggle
    ontop_var = tk.BooleanVar(value=current_config.get("always_on_top", True))
    
    def toggle():
        current_config["always_on_top"] = ontop_var.get()
        root.attributes("-topmost", current_config["always_on_top"])
        save_config(current_config)

    tk.Checkbutton(settings_win, text="Always On-Top", variable=ontop_var, command=toggle).pack(pady=5)

# --- MAIN GUI ---

def run_gui():
    root = tk.Tk()
    config = load_config()
    
    root.title(APP_NAME)
    root.geometry("350x280")
    root.configure(bg="#212121")
    root.attributes("-topmost", config.get("always_on_top", True))

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", font=("Segoe UI", 10), padding=5)
    style.configure("Main.TLabel", background="#212121", foreground="white")

    managed = is_managed_by_hub()
    origin_text = "Flobby Hub Managed" if managed else "Standalone Installer"
    origin_color = "#00ffcc" if managed else "#ffa500"
    
    ttk.Label(root, text=f"{APP_NAME} v{VERSION}", font=("Segoe UI", 14, "bold"), style="Main.TLabel").pack(pady=(20, 5))
    ttk.Label(root, text=f"Source: {origin_text}", font=("Segoe UI", 8), style="Main.TLabel", foreground=origin_color).pack(pady=(0, 10))

    status_label = ttk.Label(root, text="System Ready", font=("Segoe UI", 8), style="Main.TLabel")
    status_label.pack(pady=5)
    
    ttk.Button(root, text="Start Capture", command=lambda: solve_task(config, status_label, root), width=25).pack(pady=5)
    ttk.Button(root, text="Search History", command=lambda: search_log(simpledialog.askstring("Search", "Enter Code:")), width=25).pack(pady=5)
    ttk.Button(root, text="Settings", command=lambda: open_settings(root, config), width=25).pack(pady=5)
    
    threading.Thread(target=check_for_self_update, args=(status_label,), daemon=True).start()
    
    root.mainloop()

if __name__ == "__main__":
    run_gui()