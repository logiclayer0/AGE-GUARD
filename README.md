# AgeGuard AI

AgeGuard AI is an automated, AI-driven Windows desktop application designed for real-time age detection and parental control enforcement. It continuously monitors the active camera feed, predicts user age, and dynamically terminates browser windows or blacklisted desktop processes if restricted content is detected for underage users.

---

## Key Features

- **Real-Time Age Detection**: Uses DeepFace and OpenCV for background age classification.
- **Active Window Content Filtering**: Scans active window titles against prohibited keywords and closes non-compliant windows.
- **Process Blocking**: Terminates blacklisted media/torrent applications when underage detection triggers.
- **Desktop UI Integration**: Built with Flask and PyWebView for a native desktop dashboard interface.
- **Windows Startup Persistence**: Automatically configures Windows Registry startup entries.

---

## Tech Stack

- **Language**: Python 3.10+
- **Computer Vision & AI**: OpenCV, DeepFace, TensorFlow
- **GUI Framework**: PyWebView, Flask, HTML5/JS
- **OS Utilities**: PyWin32, Psutil, Winreg

---

## Setup & Installation

### Prerequisites
- Windows OS (10/11)
- Python 3.10 or higher
- Connected Web Camera

### Installation Steps

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/AgeGuard-AI.git](https://github.com/your-username/AgeGuard-AI.git)
   cd AgeGuard-AI