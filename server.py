import base64
import cv2
import numpy as np
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
import uvicorn
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector

app = FastAPI()

# Load detectors
mp_face = mp.solutions.face_detection.FaceDetection(0.6)
mp_pose = mp.solutions.pose.Pose(0.6, 0.6)
hand_detector = HandDetector(maxHands=2, detectionCon=0.75)

@app.get("/")
def home():
    return {"status": "OK", "message": "Realtime gesture AI server running"}

@app.get("/client.html")
def client_page():
    return FileResponse("client.html")

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    print("Client connected.")

    try:
        while True:
            msg = await ws.receive_text()
            data = json.loads(msg)
            b64 = data.get("image", "")

            if "," in b64:
                b64 = b64.split(",")[1]

            # Decode
            try:
                frame = cv2.imdecode(
                    np.frombuffer(base64.b64decode(b64), np.uint8),
                    cv2.IMREAD_COLOR
                )
            except:
                continue

            if frame is None:
                continue

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            # Face detection
            face = mp_face.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if face.detections:
                for det in face.detections:
                    bb = det.location_data.relative_bounding_box
                    x, y = int(bb.xmin*w), int(bb.ymin*h)
                    bw, bh = int(bb.width*w), int(bb.height*h)
                    cv2.rectangle(frame, (x,y), (x+bw,y+bh), (255,0,0), 2)

            # Hand detection
            try:
                hands, frame = hand_detector.findHands(frame, draw=True)
                if hands:
                    for hnd in hands:
                        f = hand_detector.fingersUp(hnd)
                        count = sum(f)
                        x, y, _, _ = hnd["bbox"]
                        cv2.putText(frame, f"{hnd['type']}:{count}",
                                    (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7,(0,255,0),2)
            except:
                pass

            # Pose detection
            pose = mp_pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if pose.pose_landmarks:
                lm = pose.pose_landmarks.landmark
                L = lm[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
                R = lm[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
                cv2.circle(frame, (int(L.x*w), int(L.y*h)), 8, (0,255,255), -1)
                cv2.circle(frame, (int(R.x*w), int(R.y*h)), 8, (0,255,255), -1)

            # Encode back to base64
            _, jpg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            encoded = base64.b64encode(jpg).decode("ascii")
            await ws.send_text(json.dumps({"image": f"data:image/jpeg;base64,{encoded}"}))

    except Exception as e:
        print("Disconnected:", e)
    finally:
        print("Client disconnected.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
