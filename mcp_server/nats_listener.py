# nats_listener.py

import json

from nats.aio.client import Client as NATS

from config import (
    NATS_URL,
    FACE_SUBJECT, 
    DEPTH_SUBJECT,
    BLINK_SUBJECT,
)


class NATSListener:

    def __init__(self, blink_test):
        self.nc = NATS()
        self.blink_test = blink_test

    async def connect(self):

        await self.nc.connect()

        print(f"Connected to {NATS_URL}")

    async def subscribe(self):

        await self.nc.subscribe(
            FACE_SUBJECT,
            cb=self.face_callback
        )

        await self.nc.subscribe(
            DEPTH_SUBJECT,
            cb=self.depth_callback
        )

        await self.nc.subscribe(
            BLINK_SUBJECT,
            cb=self.blink_callback
        )

        print("\nSubscribed Subjects:")
        print(FACE_SUBJECT)
        print(DEPTH_SUBJECT)
        print(BLINK_SUBJECT)

    async def face_callback(self, msg):

        data = json.loads(msg.data.decode())

        print("\nFACE:", data)

        self.blink_test.update_face(data)

    async def depth_callback(self, msg):

        data = json.loads(msg.data.decode())

        print("\nDEPTH:", data)

        self.blink_test.update_depth(data)

    async def blink_callback(self, msg):

        data = json.loads(msg.data.decode())

        print("\nBLINK:", data)

        self.blink_test.update_blink(data)