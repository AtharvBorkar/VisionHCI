# 🏄VisionHCI-Subway Surfers Hand Gesture Controller

> Control **Subway Surfers** (or any arrow-key driven game) with real-time **hand swipe gestures** detected via your webcam — no hardware, no controller required.

---

## 📸 Demo

| Gesture | Action |
|---------|--------|
| ✋ Swipe **Up** | Jump (`↑`) |
| 🤚 Swipe **Down** | Roll / Slide (`↓`) |
| ✋ Swipe **Left** | Move Left (`←`) |
| 🤚 Swipe **Right** | Move Right (`→`) |

---

## 🧠 How It Works

The script uses your webcam feed to track your hand in real time:

1. **OpenCV** captures frames from the webcam and mirrors them for natural movement.
2. **MediaPipe Hands** detects and tracks 21 hand landmarks per frame.
3. The **middle-finger MCP joint (landmark #9)** is used as a stable "palm center" point.
4. A rolling time-window history of palm positions is maintained.
5. When the palm moves more than a configurable threshold distance within a short time window, it is classified as a swipe (`UP`, `DOWN`, `LEFT`, or `RIGHT`).
6. **pydirectinput** synthesizes the corresponding arrow key press directly into the OS — works even with games that ignore `pyautogui`.

```
Webcam → OpenCV → MediaPipe → Swipe Logic → pydirectinput → Game
```

---

## 🗂️ Project Structure

```
VisionHCI/
├── main.py        # Core gesture detection and key-press logic
└── README.md      # This file
```

---

## ⚙️ Requirements

| Package | Purpose |
|---------|---------|
| `opencv-python` | Webcam capture & display |
| `mediapipe` | Real-time hand landmark detection |
| `pydirectinput` | Low-level Windows keyboard input (DirectInput compatible) |

> **Platform:** Windows only (pydirectinput uses the Win32 API).  
> **Python:** 3.8 – 3.12

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/VisionHCI.git
cd VisionHCI
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install opencv-python mediapipe pydirectinput
```

---

## ▶️ Running the Controller

```bash
python main.py
```

1. A camera preview window titled **"Hand Gesture Control (ESC to quit)"** will open.
2. **Click into the Subway Surfers game window** so it has keyboard focus.
3. Hold your hand in front of the webcam and swipe in any direction.
4. Press **`ESC`** in the camera window to exit.

---

## 🎛️ Tuning Parameters

All tuning knobs are at the top of [`main.py`](main.py#L28-L32):

| Constant | Default | Description |
|----------|---------|-------------|
| `SWIPE_THRESHOLD` | `0.35` | Minimum normalized distance (0–1) the palm must travel to register a swipe. **Lower = more sensitive.** |
| `WINDOW_SECONDS` | `0.35` | Time window (seconds) over which movement is measured. |
| `COOLDOWN` | `0.45` | Minimum delay (seconds) between two consecutive gesture triggers — prevents double-firing. |

> **Tip:** If swipes are triggering too easily, increase `SWIPE_THRESHOLD`. If they feel laggy, decrease `WINDOW_SECONDS`.

---

## 🔑 Key Mapping

Keys can be remapped by editing the `KEY_MAP` dictionary in [`main.py`](main.py#L34-L39):

```python
KEY_MAP = {
    "up":    "up",
    "down":  "down",
    "left":  "left",
    "right": "right",
}
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| Camera not opening | Make sure no other app is using the webcam. Try changing `cv2.VideoCapture(0)` to `1` or `2`. |
| Gestures not registering in-game | Ensure the **game window is focused** (click on it before swiping). |
| False positives / double triggers | Increase `COOLDOWN` or `SWIPE_THRESHOLD`. |
| `pydirectinput` not working | Run the script as **Administrator** (right-click → "Run as administrator"). |
| Slow / laggy detection | Lower webcam resolution or use `model_complexity=0` (already set by default). |

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for:

- Support for additional gestures (e.g., pinch to pause)
- Multi-platform support (Linux/macOS via `pynput`)
- GUI configuration panel for tuning parameters
- Support for other games / custom key bindings

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [MediaPipe](https://mediapipe.dev/) by Google — for the blazing-fast hand tracking model.
- [OpenCV](https://opencv.org/) — for webcam capture and frame processing.
- [pydirectinput](https://github.com/learncodebygaming/pydirectinput) — for reliable DirectInput key injection on Windows.
