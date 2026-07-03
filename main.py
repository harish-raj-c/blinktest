import asyncio
import json

from nats.aio.client import Client as NATS

from blink_test import BlinkTest


NATS_URL = "nats://192.168.0.187:4222"

blink_test = BlinkTest()


async def face_handler(msg):
    data = json.loads(msg.data.decode())

    blink_test.update_face(data)


async def depth_handler(msg):
    data = json.loads(msg.data.decode())

    blink_test.update_depth(data)


async def blink_handler(msg):
    data = json.loads(msg.data.decode())

    blink_test.update_blink(data)


async def monitor():
    while True:

        if not blink_test.running:

            ready, status = blink_test.calibration_status()

            print(f"\rCalibration: {status}", end="")

            if ready:
                print("\nStarting in 3 seconds...")
                await asyncio.sleep(3)

                blink_test.start()

        else:

            if blink_test.is_finished():
                blink_test.stop()

                print("Waiting for next user...\n")

                await asyncio.sleep(5)

        await asyncio.sleep(0.1)


async def main():

    nc = NATS()

    await nc.connect(NATS_URL)

    print(f"\nConnected to {NATS_URL}")

    await nc.subscribe(
        "vision.eye.cam0.face",
        cb=face_handler
    )

    await nc.subscribe(
        "vision.eye.cam0.depth",
        cb=depth_handler
    )

    await nc.subscribe(
        "vision.eye.cam0.blink",
        cb=blink_handler
    )

    print("Subscribed to:")
    print(" - vision.eye.cam0.face")
    print(" - vision.eye.cam0.depth")
    print(" - vision.eye.cam0.blink")

    await monitor()


if __name__ == "__main__":
    asyncio.run(main())