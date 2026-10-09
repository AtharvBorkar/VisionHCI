"""
Hand Gesture -> Keyboard Controller (Subway Surfers style)
------------------------------------------------------------
Swipe your hand UP / DOWN / LEFT / RIGHT in front of the webcam
to trigger the corresponding arrow key press.

Install requirements first:
    pip install opencv-python mediapipe pydirectinput

Run:
    python gesture_control.py

Then click into the game window (so it has focus) and start swiping.
Press ESC in the camera window to quit.
"""

import cv2
import mediapipe as mp
import time
from collections import deque
import pydirectinput

pydirectinput.PAUSE = 0  # no artificial delay between key actions

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# ---------------- Tuning knobs ----------------
SWIPE_THRESHOLD = 0.35     # how far (0-1 normalized) the hand must move to count as a swipe
WINDOW_SECONDS = 0.35      # how far back in time we look to measure the movement
COOLDOWN = 0.45           # minimum seconds between two triggered gestures
# ------------------------------------------------

KEY_MAP = {
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
}


def trigger_key(direction):
    key = KEY_MAP[direction]
    print(f"Swipe detected: {direction.upper()}  ->  key '{key}'")
    pydirectinput.press(key)


def main():
    cap = cv2.VideoCapture(0)
    history = deque()   # stores (timestamp, x, y) of palm center
    last_trigger_time = 0.0

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    ) as hands:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image = cv2.flip(image, 1)  # mirror so movement feels natural
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            results = hands.process(rgb)

            now = time.time()
            direction_shown = None

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # landmark 9 = middle finger MCP, a good stable "palm center" point
                palm = hand_landmarks.landmark[9]
                cx, cy = palm.x, palm.y

                history.append((now, cx, cy))
                # drop entries older than our detection window
                while history and now - history[0][0] > WINDOW_SECONDS:
                    history.popleft()

                if history and (now - last_trigger_time) > COOLDOWN:
                    old_t, old_x, old_y = history[0]
                    dx = cx - old_x
                    dy = cy - old_y

                    if abs(dx) > SWIPE_THRESHOLD or abs(dy) > SWIPE_THRESHOLD:
                        if abs(dx) > abs(dy):
                            direction = "right" if dx > 0 else "left"
                        else:
                            direction = "down" if dy > 0 else "up"

                        trigger_key(direction)
                        direction_shown = direction
                        last_trigger_time = now
                        history.clear()  # reset so we don't double-trigger on the same swipe
            else:
                history.clear()

            if direction_shown:
                cv2.putText(image, direction_shown.upper(), (40, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            cv2.imshow("Hand Gesture Control (ESC to quit)", image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()