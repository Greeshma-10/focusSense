import os
import subprocess
import threading
from flask import Flask, render_template
import signal

app = Flask(__name__)

process = None  # Global variable to hold the subprocess

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start')
def start_focus_session():
    global process
    if process and process.poll() is None:
        return "Focus session already running!"

    python_path = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')
    process = subprocess.Popen([python_path, 'main.py'])
    return "Focus session started!"

@app.route('/stop')
def stop_focus_session():
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()
        process = None
        return "Focus session stopped."
    return "No session is running."

if __name__ == '__main__':
    app.run(debug=True)
