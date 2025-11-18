Real-Time Body & Gesture Detection System

A Python-based real-time face, hand, finger, and body gesture detection system built using YOLOv8, OpenCV, cvzone, and MediaPipe.

This project captures webcam input and performs live detection of:

👤 Face detection

✋ Hand tracking + finger count

🤟 Gesture recognition (V sign, fist, OK, etc.)

🧍 Basic body estimation (shoulders)

The system also includes a built-in fallback mode that uses skin segmentation whenever MediaPipe is unavailable. Everything runs completely offline.

✨ Features
✅ 1. Real-Time Face Detection

Uses Haar Cascade to detect faces and draw bounding boxes.

✅ 2. Hand & Finger Detection

Uses cvzone HandDetector (MediaPipe)

Detects left/right hand

Counts number of fingers

Shows bounding box + label

✅ 3. Gesture Recognition

Recognizes common gestures like:

✌️ V Sign

✊ Fist

👌 OK Sign

✅ 4. Fallback Hand Detection (YOLO + Skin Mask)

If cvzone fails, the system switches to a custom hand detection method:

YOLO detects the person region

Skin segmentation isolates hand region

Convex hull + defects used for finger counting

Zero dependencies? No problem — system still works.

✅ 5. Body Part Estimation

Estimates left & right shoulder positions using YOLO person bounding box.

✅ 6. Tkinter Control Panel

Small popup window with an Exit button to stop the application cleanly.



| Component          | Technology              |
| ------------------ | ----------------------- |
| Object Detection   | YOLOv8 (Ultralytics)    |
| Hand Tracking      | cvzone + MediaPipe      |
| Fallback Detection | Skin-color segmentation |
| Rendering          | OpenCV                  |
| UI                 | Tkinter                 |
| Language           | Python 3.x              |




#run it to install 
pip install ultralytics opencv-python numpy cvzone mediapipe==0.10.21
