import cv2
import threading
import psutil
import win32gui
import win32process
import time
import os
import sys
import winreg as reg
from flask import Flask, jsonify
from deepface import DeepFace
import webview 

app = Flask(__name__)

SAFE_AGE_LIMIT = 18
CAMERA_INDEX = 0 
BLOCK_LIST = ["vlc.exe", "kmplayer.exe", "pikashow.exe", "moviebox.exe", "torrent.exe"]
CENSOR_KEYWORDS = ["18+", "adult", "porn", "sex", "restricted", "mature", "mirzapur", "webseries", "dating", "crime thriller"]

system_status = {"active": True, "alert": False, "detected_age": "Scanning..."}

def add_to_startup():
    path = os.path.realpath(sys.argv[0])
    try:
        key = reg.HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(open_key, "AgeGuardAI", 0, reg.REG_SZ, path)
        reg.CloseKey(open_key)
    except Exception:
        pass

def kill_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        psutil.Process(pid).kill()
    except Exception:
        pass

def monitor_system():
    global system_status
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while True:
        if not system_status["active"]:
            time.sleep(1)
            continue

        success, frame = cap.read()
        if not success:
            time.sleep(0.5)
            continue

        try:
            results = DeepFace.analyze(frame, actions=['age'], enforce_detection=False, detector_backend='opencv')
            if results and len(results) > 0:
                raw_age = int(results[0]['age'])
                age = raw_age - 3
                system_status["detected_age"] = max(1, age)

                if age < SAFE_AGE_LIMIT:
                    window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow()).lower()
                    if any(key in window_title for key in CENSOR_KEYWORDS):
                        system_status["alert"] = True
                        kill_active_window()

                    for proc in psutil.process_iter(['name']):
                        try:
                            if proc.info['name'] and proc.info['name'].lower() in BLOCK_LIST:
                                proc.kill()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                else:
                    system_status["alert"] = False
        except Exception:
            pass

        time.sleep(0.5)

@app.route('/status')
def get_status():
    return jsonify(system_status)

@app.route('/toggle')
def toggle():
    system_status["active"] = not system_status["active"]
    return jsonify({"active": system_status["active"]})

@app.route('/')
def dashboard_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AgeGuard AI</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                background: #121212;
                color: #ffffff;
                padding: 30px;
                margin: 0;
            }
            h1 { color: #4285f4; margin-bottom: 5px; }
            p { color: #aaaaaa; font-size: 14px; }
            .age-box {
                font-size: 60px;
                font-weight: bold;
                margin: 25px 0;
                color: #4285f4;
            }
            .alert-box {
                color: #ea4335;
                font-weight: bold;
                margin: 15px 0;
                display: none;
                padding: 10px;
                border: 1px solid #ea4335;
                border-radius: 8px;
                background: rgba(234, 67, 53, 0.1);
            }
            button {
                padding: 15px 30px;
                border-radius: 30px;
                border: none;
                background: #34a853;
                color: white;
                font-weight: bold;
                cursor: pointer;
                font-size: 14px;
            }
            button:hover { background: #2d9247; }
        </style>
    </head>
    <body>
        <h1>AgeGuard Pro Shield</h1>
        <p>Parental Control Active</p>
        
        <div class="age-box" id="age">Scanning...</div>
        
        <div id="alertMsg" class="alert-box">🚨 RESTRICTED CONTENT BLOCKED</div>
        
        <button onclick="toggleShield()">Enable/Disable Guard</button>
        
        <p style="font-size:12px; color:gray; margin-top:30px;">Stealth Mode: ON | Autostart: ENABLED</p>

        <script>
            function updateStatus() {
                fetch('/status')
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('age').innerText = data.detected_age;
                        document.getElementById('alertMsg').style.display = data.alert ? 'block' : 'none';
                    })
                    .catch(e => console.error(e));
            }

            function toggleShield() {
                fetch('/toggle')
                    .then(r => r.json())
                    .then(data => {
                        alert("Guard State Changed! Active: " + data.active);
                    })
                    .catch(e => console.error(e));
            }

            setInterval(updateStatus, 1000);
        </script>
    </body>
    </html>
    """

def run_server():
    app.run(host='127.0.0.1', port=5000)

if __name__ == "__main__":
    add_to_startup()
    threading.Thread(target=run_server, daemon=True).start()
    threading.Thread(target=monitor_system, daemon=True).start()
    
    print("Launching Desktop Dashboard...")
    webview.create_window('AgeGuard AI Dashboard', 'http://127.0.0.1:5000', width=450, height=600)
    webview.start()