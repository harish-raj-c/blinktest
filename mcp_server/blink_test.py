# blink_test.py

import time

from config import (
    TEST_DURATION,
    MIN_DEPTH,
    MAX_DEPTH,
)


class BlinkTest:

    def __init__(self):
        self.reset()

    def reset(self):
        self.running = False

        self.face_detected = False
        self.depth_center = None
        self.last_depth_time = 0

        self.start_time = None

        self.blink_count = 0
        self.last_blink_time = 0
        self.ear_values = []

        self.distance_values = []

    def update_face(self, data):
        self.face_detected = data.get("face_detected", False)
        if not self.running:
            distance_str = f"{self.depth_center:.1f}mm" if self.depth_center else "N/A"
            print(f"\rFace: {'DETECTED' if self.face_detected else 'NOT DETECTED'} | Distance: {distance_str}", end="")

    def update_depth(self, data):
        self.depth_center = data.get("center")
        self.last_depth_time = time.time()

        if self.running and self.depth_center is not None:
            self.distance_values.append(self.depth_center)
            elapsed = time.time() - self.start_time
            position = self.get_distance_category(self.depth_center)
            print(f"\rDuration: {elapsed:.1f}s | Distance: {self.depth_center:.1f}mm ({position}) | Blinks: {self.blink_count}", end="")

    def update_blink(self, data):

        if not self.running:
            return

        avg_ear = data.get("avg_ear", 0)
        blink = data.get("blink", False)

        self.ear_values.append(avg_ear)

        if blink:

            current_time = time.time()

            if current_time - self.last_blink_time > 0.30:
                self.blink_count += 1
                print(f"BLINK #{self.blink_count} DETECTED | EAR={avg_ear:.3f}")

                self.last_blink_time = current_time

    def calibration_status(self):

        if not self.face_detected:
            return False, "Your face is not detected. Please position yourself in front of the camera."

        if self.depth_center is None:
            return False, "Depth data missing. Ensure camera is working properly."

        # Check if depth data is stale (older than 1 second)
        if time.time() - self.last_depth_time > 1.0:
            return False, "Stay still. Waiting for stable depth measurement..."

        if self.depth_center < MIN_DEPTH:
            return False, f"You are too close to the camera. Move back to {MIN_DEPTH}-{MAX_DEPTH}mm."

        if self.depth_center > MAX_DEPTH:
            return False, f"You are too far from the camera. Move closer to {MIN_DEPTH}-{MAX_DEPTH}mm."

        return True, "Ready - Position is perfect!"

    def start(self):

        self.running = True
        self.start_time = time.time()

        self.blink_count = 0
        self.ear_values = []

        print("\n")
        print("=" * 40)
        print("BLINK TEST STARTED")
        print("=" * 40)

    def is_finished(self):

        if not self.running:
            return False

        elapsed = time.time() - self.start_time

        return elapsed >= TEST_DURATION

    def stop(self):

        self.running = False

        elapsed = time.time() - self.start_time

        blink_rate = (self.blink_count / elapsed) * 60

        avg_ear = 0

        if self.ear_values:
            avg_ear = sum(self.ear_values) / len(self.ear_values)

        avg_distance = 0

        if self.distance_values:
            avg_distance = (
                sum(self.distance_values)
                / len(self.distance_values)
            )

        score = self.get_eye_comfort_score(
            blink_rate,
            avg_ear
        )

        recommendation = self.get_recommendation(score)

        category = self.get_category(blink_rate)

        print("\n")
        print("=" * 60)
        print("BLINK TEST RESULT")
        print("=" * 60)
        print(f"Duration             : {elapsed:.1f} seconds")
        print(f"Total Blinks         : {self.blink_count}")
        print(f"Blink Rate           : {blink_rate:.1f} blinks/minute")
        print(f"Average Distance     : {avg_distance:.1f}mm")
        print(f"Position Category    : {self.get_distance_category(avg_distance)}")
        print(f"Average EAR          : {avg_ear:.3f}")
        print(f"Eye Comfort Score    : {score}/100")
        print(f"Category             : {category}")
        print("\nRecommendation:")
        print(recommendation)
        print("=" * 60)

    def get_category(self, blink_rate):

        if blink_rate >= 15:
            return "Excellent"

        elif blink_rate >= 12:
            return "Good"

        elif blink_rate >= 8:
            return "Mild Eye Strain"

        elif blink_rate >= 5:
            return "Moderate Eye Strain"

        return "Possible Dry Eye Risk"

    def get_distance_category(self, distance):

        if distance < 120:
            return "Too Close"

        elif distance > 240:
            return "Too Far"

        return "Optimal"
    
    def get_eye_comfort_score(self, blink_rate, avg_ear):

        score = 100

        if blink_rate < 10:
            score -= 30

        if blink_rate < 15:
            score -= 10

        if blink_rate < 30:
            score -= 15

        if avg_ear < 0.20:
            score -= 15

        return max(score, 0)

    def get_recommendation(self, score):

        if score >= 80:
            return (
                "Healthy blinking pattern detected.\n"
                "Continue current eye-care habits."
            )

        elif score >= 60:
            return (
                "Remember to blink regularly.\n"
                "Follow the 20-20-20 rule."
            )

        elif score >= 40:
            return (
                "Signs of eye fatigue detected.\n"
                "Take regular breaks from screens."
            )

        elif score >= 20:
            return (
                "Reduced blink activity detected.\n"
                "Increase blinking frequency.\n"
                "Stay hydrated."
            )

        return (
            "Possible dry-eye risk.\n"
            "Consider consulting an eye-care professional."
        )

        