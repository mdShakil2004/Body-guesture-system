# Realtime Gesture AI (Face + Hands + Body Pose)

Real-time webcam → Cloud → AI processing → Browser output.

This project streams live webcam video from the browser to a FastAPI server (running on Colab or any backend). The server processes the frame using:





- Mediapipe Face Detection  
- Mediapipe Pose (Shoulders)  
- cvzone Hand Tracking  
- OpenCV  

Then sends the processed frame back to the browser **in real-time** using WebSockets.

---

## 🚀 Features
- Real-time < 100ms latency  
- Face detection  
- Hand tracking + finger count  
- Body pose (shoulders)  
- WebSocket-based video streaming  
- Cloudflare tunnel (no login, free)  
- Works on laptop and phone  
- Works in Google Colab  

---

## 📦 Files
- `server.py` – FastAPI WebSocket + AI processing  
- `client.html` – Browser webcam stream UI  
- `run_server.ipynb` – Start server in Colab with Cloudflare tunnel  
- `requirements.txt`  

---

## 🧠 How It Works

Browser → WebSocket → FastAPI → Mediapipe/cvzone → WebSocket → Browser

---

## 🔧 Run in Colab

1. Upload repo  
2. Open `run_server.ipynb`  
3. Run all cells  
4. Open the printed URL:






here tunnel :  example ->>   
import subprocess, re, time

print("Starting Cloudflare tunnel...")
proc = subprocess.Popen(
    ["cloudflared", "tunnel", "--url", "http://0.0.0.0:8000"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
)

public_url = None
for _ in range(60):
    line = proc.stdout.readline().strip()
    print(line)
    match = re.search(r"https://[-a-zA-Z0-9]+\.trycloudflare\.com", line)
    if match:
        public_url = match.group(0)
        break
    time.sleep(0.5)

print("PUBLIC URL:", public_url)
print("CLIENT PAGE:", public_url + "/client.html")


