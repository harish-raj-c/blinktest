import asyncio
import json
import time

from fastmcp import FastMCP
from nats.aio.client import Client as NATS
from blink_test import BlinkTest

# =====================================================
# Configuration
# =====================================================

NATS_URL = "nats://192.168.0.187:4222"

mcp = FastMCP("Blink Test MCP")

blink_test = BlinkTest()


# =====================================================
# NATS Message Handlers
# =====================================================

async def face_handler(msg):
    data = json.loads(msg.data.decode())
    blink_test.update_face(data)


async def depth_handler(msg):
    data = json.loads(msg.data.decode())
    blink_test.update_depth(data)


async def blink_handler(msg):
    data = json.loads(msg.data.decode())
    blink_test.update_blink(data)


# =====================================================
# Background NATS Listener
# =====================================================

async def nats_monitor():
    nc = NATS()

    await nc.connect(NATS_URL)
    print(f"Connected to NATS: {NATS_URL}")

    await nc.subscribe(
        "vision.eye.cam0.face",
        cb=face_handler,
    )

    await nc.subscribe(
        "vision.eye.cam0.depth",
        cb=depth_handler,
    )

    await nc.subscribe(
        "vision.eye.cam0.blink",
        cb=blink_handler,
    )

    print("Subscribed to NATS topics")

    while True:

        if blink_test.running:

            if blink_test.is_finished():
                blink_test.stop()
                print("Blink test completed")

        await asyncio.sleep(0.1)


# =====================================================
# MCP Tools
# =====================================================

@mcp.tool()
def get_status():
    """
    Get current calibration and test status.
    """

    ready, status = blink_test.calibration_status()

    return {
        "ready": ready,
        "status": status,
        "running": blink_test.running,
        "face_detected": blink_test.face_detected,
        "depth_center": blink_test.depth_center,
        "blink_count": blink_test.blink_count,
    }


@mcp.tool()
def start_test():
    """
    Start blink test.
    """

    if blink_test.running:
        return {
            "success": False,
            "message": "Test already running",
        }

    ready, status = blink_test.calibration_status()

    if not ready:
        return {
            "success": False,
            "message": status,
        }

    blink_test.start()

    return {
        "success": True,
        "message": "Blink test started",
    }


@mcp.tool()
def stop_test():
    """
    Stop blink test and return results.
    """

    if not blink_test.running:
        return {
            "success": False,
            "message": "No active test",
        }

    blink_test.stop()

    elapsed = (
        time.time() - blink_test.start_time
        if blink_test.start_time
        else 0
    )

    blink_rate = (
        (blink_test.blink_count / elapsed) * 60
        if elapsed > 0
        else 0
    )

    avg_ear = (
        sum(blink_test.ear_values) / len(blink_test.ear_values)
        if blink_test.ear_values
        else 0
    )

    avg_distance = (
        sum(blink_test.distance_values) / len(blink_test.distance_values)
        if blink_test.distance_values
        else 0
    )

    score = blink_test.get_eye_comfort_score(
        blink_rate,
        avg_ear,
    )

    return {
        "success": True,
        "duration": round(elapsed, 1),
        "total_blinks": blink_test.blink_count,
        "blink_rate": round(blink_rate, 1),
        "average_ear": round(avg_ear, 3),
        "average_distance": round(avg_distance, 1),
        "eye_comfort_score": score,
        "category": blink_test.get_category(blink_rate),
        "recommendation": blink_test.get_recommendation(score),
    }


@mcp.tool()
def reset_test():
    """
    Reset blink test.
    """

    blink_test.reset()

    return {
        "success": True,
        "message": "Blink test reset",
    }


@mcp.tool()
def current_metrics():
    """
    Get current live metrics while the test is running.
    """

    elapsed = (
        time.time() - blink_test.start_time
        if blink_test.start_time and blink_test.running
        else 0
    )

    return {
        "running": blink_test.running,
        "elapsed": round(elapsed, 1),
        "blink_count": blink_test.blink_count,
        "face_detected": blink_test.face_detected,
        "distance": blink_test.depth_center,
    }


# =====================================================
# Main
# =====================================================

async def main():
    asyncio.create_task(nats_monitor())

    await mcp.run_async(
        transport="http",
        host="0.0.0.0",
        port=8001,
    )

if __name__ == "__main__":
    asyncio.run(main())