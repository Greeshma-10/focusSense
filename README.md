# 🧠 FocusSense: Distraction Detection System 👁️‍🗨️

**FocusSense** is an innovative computer vision system that detects signs of user distraction through real-time head movement and blink rate analysis. It offers insights into engagement levels, making it ideal for remote learning, online meetings, and productivity tracking.

---

## ✨ About The Project

In today’s digital-first world, maintaining focus is a challenge. **FocusSense** tackles this issue by using subtle facial cues—like head turns or blink patterns—to infer distraction or drowsiness. The system is designed to be non-intrusive and provide actionable feedback via a focus score.

---

## 🌟 Features

- 🎯 **Real-time Distraction Detection**: Continuously monitors focus indicators.
- 🧍 **Head Movement Analysis**: Tracks changes in head orientation.
- 👁️ **Blink Rate Monitoring**: Detects drowsiness and disengagement through blink frequency.
- 📈 **Focus Score Calculation**: Combines all metrics into a real-time concentration score.
- 🖥️ **User Interface**: Displays live feedback on focus levels.
- 🧩 **Modular Design**: Easily extend or improve each component (tracking, scoring, UI, etc).

---

## 🛠️ Technologies Used

- **Python** – Core language
- **OpenCV** – Video processing and head pose estimation
- **Dlib** – Facial landmark detection
- **NumPy** – Numerical operations
- **Flask** *(optional)* – For web-based interface
- **HTML/CSS/JS** – Frontend UI (if web app)

---

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.x
- Pip
- Virtual Environment (optional but recommended)

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Greeshma-10/focusSense
cd FocusSense

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirement.txt
```
⚠️ Ensure that requirement.txt includes opencv-python, dlib, numpy, flask, etc.

## 🏃 Running the Application
```bash
# Run the main program
python main.py
```
If using Flask for UI:

```bash
python app.py
```
Navigate to http://127.0.0.1:5000 in your browser (if web-based UI is implemented).

## 📂 Project Structure
```text

FocusSense/
├── templates/              # HTML templates (for web UI)
├── .gitignore              # Ignore files like __pycache__/, venv/, etc.
├── app.py                  # Flask web app (optional)
├── focus_tracker.py        # Core logic for detecting head movement and blink rate
├── main.py                 # Main script to run system
├── requirement.txt         # Required Python packages
├── score_calculator.py     # Logic to compute focus score
├── ui.py                   # UI rendering logic
└── utils.py                # Utility/helper functions
```
🧑‍💻 Made with ❤️ by Greeshma-10
****
