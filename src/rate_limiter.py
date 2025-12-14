import time
import random

class AdaptiveRateLimiter:
    def __init__(self, min_sleep=1.0, max_sleep=10.0):
        self.min_sleep = min_sleep
        self.max_sleep = max_sleep
        self.current_sleep = min_sleep

    def success(self):
        self.current_sleep = max(self.min_sleep, self.current_sleep * 0.9)

    def failure(self):
        self.current_sleep = min(self.max_sleep, self.current_sleep * 1.5)

    def wait(self):
        jitter = random.uniform(0, 0.5)
        time.sleep(self.current_sleep + jitter)
