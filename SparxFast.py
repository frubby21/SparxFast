import pyautogui
from google import genai
from PIL import Image
import time
import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

APP_NAME = "SparxFast"
BASE_DIR = os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), APP_NAME)
LOG_FILE = os.path.join(BASE_DIR, "sparx.log")
SCREENSHOT_PATH = os.path.join(BASE_DIR, "sparx_capture.png")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR, exist_ok=True)

def get_api_key():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f).get("key")
    return None

def save_api_key(key):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"key": key}, f)

def search_log(code):
    if not os.path.exists(LOG_FILE):
        messagebox.showinfo("Error", "Log file not found.")
        return
    found = False
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        entries = f.read().split('-'*40)
        for entry in entries:
            if f"CODE: {code}" in entry.upper():
                messagebox.showinfo(f"Result: {code}", entry.strip())
                found = True
    if not found:
        messagebox.showwarning("Not Found", f"Code {code} not found.")

def solve_task():
    api_key = get_api_key()
    if not api_key:
        messagebox.showerror("Error", "No API Key set.")
        return
    
    client = genai.Client(api_key=api_key)
    
    time.sleep(2)
    x1, y1 = pyautogui.position()
    time.sleep(2)
    x2, y2 = pyautogui.position()

    width, height = x2 - x1, y2 - y1
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot.save(SCREENSHOT_PATH)
    
    prompt = "Identify the Bookwork Code. Solve the math problem. Format: CODE: [Code]\nANSWER: [Final Answer]\nSTEPS: [1-sentence max]"
    
    try:
        img = Image.open(SCREENSHOT_PATH)
        response = client.models.generate_content(model="gemini-3-flash-preview", contents=[prompt, img])
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{response.text}\n{'-'*40}")

        messagebox.showinfo("Solution", response.text)
    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

def set_key_dialog():
    key = simpledialog.askstring("API Key", "Enter Gemini API Key:")
    if key:
        save_api_key(key)

def search_dialog():
    code = simpledialog.askstring("Search", "Enter Bookwork Code:")
    if code:
        search_log(code.upper())

def run_gui():
    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry("300x200")
    root.attributes("-topmost", True)

    tk.Label(root, text="SparxFast v1.0", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Button(root, text="Start Capture", command=solve_task, width=20, bg="#4CAF50", fg="white").pack(pady=5)
    tk.Button(root, text="Search Log", command=search_dialog, width=20).pack(pady=5)
    tk.Button(root, text="Settings (API Key)", command=set_key_dialog, width=20).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    run_gui()