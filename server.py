from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from nats.aio.client import Client as NATS
from blink_test import BlinkTest
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NATS_URL = "nats://192.168.0.187:4222"
blink_test = BlinkTest()

# Store connected clients
active_websockets = set()


@app.get("/api/status")
async def get_status():
    """Get current blink test status"""
    ready, status = blink_test.calibration_status()
    return {
        "ready": ready,
        "status": status,
        "running": blink_test.running,
        "face_detected": blink_test.face_detected,
        "depth_center": blink_test.depth_center
    }


@app.post("/api/start")
async def start_test():
    """Start the blink test"""
    if blink_test.running:
        return {"success": False, "message": "Test already running"}

    blink_test.start()
    return {"success": True, "message": "Test started"}


@app.post("/api/stop")
async def stop_test():
    """Stop the blink test and get results"""
    if not blink_test.running:
        return {"success": False, "message": "No test running"}
    
    blink_test.stop()
    
    elapsed = 0
    if blink_test.start_time:
        elapsed = __import__('time').time() - blink_test.start_time
    
    blink_rate = (blink_test.blink_count / elapsed) * 60 if elapsed > 0 else 0
    
    avg_ear = 0
    if blink_test.ear_values:
        avg_ear = sum(blink_test.ear_values) / len(blink_test.ear_values)
    
    avg_distance = 0
    if blink_test.distance_values:
        avg_distance = sum(blink_test.distance_values) / len(blink_test.distance_values)
    
    score = blink_test.get_eye_comfort_score(blink_rate, avg_ear)
    category = blink_test.get_category(blink_rate)
    recommendation = blink_test.get_recommendation(score)
    
    return {
        "success": True,
        "results": {
            "duration": round(elapsed, 1),
            "total_blinks": blink_test.blink_count,
            "blink_rate": round(blink_rate, 1),
            "avg_ear": round(avg_ear, 3),
            "avg_distance": round(avg_distance, 1),
            "eye_comfort_score": score,
            "category": category,
            "recommendation": recommendation
        }
    }


@app.post("/api/reset")
async def reset_test():
    """Reset the blink test"""
    blink_test.reset()
    return {"success": True, "message": "Test reset"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_websockets.add(websocket)
    
    try:
        while True:
            # Send current status
            ready, status = blink_test.calibration_status()
            data = {
                "type": "status",
                "ready": ready,
                "status": status,
                "running": blink_test.running,
                "face_detected": blink_test.face_detected,
                "depth_center": blink_test.depth_center,
                "blink_count": blink_test.blink_count,
                "elapsed": round(__import__('time').time() - blink_test.start_time, 1) if blink_test.start_time and blink_test.running else 0
            }
            await websocket.send_json(data)
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_websockets.discard(websocket)


async def face_handler(msg):
    data = json.loads(msg.data.decode())
    blink_test.update_face(data)


async def depth_handler(msg):
    data = json.loads(msg.data.decode())
    blink_test.update_depth(data)


async def blink_handler(msg):
    data = json.loads(msg.data.decode())
    blink_test.update_blink(data)


async def nats_monitor():
    """Monitor NATS messages and manage test lifecycle"""
    nc = NATS()
    await nc.connect(NATS_URL)
    print(f"Connected to {NATS_URL}")
    
    await nc.subscribe("vision.eye.cam0.face", cb=face_handler)
    await nc.subscribe("vision.eye.cam0.depth", cb=depth_handler)
    await nc.subscribe("vision.eye.cam0.blink", cb=blink_handler)
    
    print("Subscribed to NATS topics")
    
    while True:
        if not blink_test.running:
            ready, status = blink_test.calibration_status()
            if ready:
                print("Ready to start test")
        else:
            if blink_test.is_finished():
                blink_test.stop()
                print("Test finished automatically")
        await asyncio.sleep(0.1)


@app.on_event("startup")
async def startup_event():
    """Start NATS listener on server startup"""
    asyncio.create_task(nats_monitor())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
