import time
from collections import deque


class RateLimiter:
    def __init__(self, get_limit, post_put_delete_limit, get_freq, post_put_delete_freq):
        self.get_limit = get_limit
        self.post_put_delete_limit = post_put_delete_limit
        self.get_freq = get_freq
        self.post_put_delete_freq = post_put_delete_freq

        self.get_timestamps = deque(maxlen=self.get_limit)
        self.post_put_delete_timestamps = deque(maxlen=self.post_put_delete_limit)

    def _should_wait(self, method):
        current_time = time.time()

        if method == "GET":
            timestamps = self.get_timestamps
            limit = self.get_limit
            freq = self.get_freq
        else:
            timestamps = self.post_put_delete_timestamps
            limit = self.post_put_delete_limit
            freq = self.post_put_delete_freq

        # Check if we've hit the rate limit
        if len(timestamps) < limit:
            return False

        time_elapsed = current_time - timestamps[0]
        if time_elapsed < freq:
            return True
        return False

    def wait(self, method):
        if self._should_wait(method):
            if method == "GET":
                sleep_duration = self.get_freq - (time.time() - self.get_timestamps[0])
            else:
                sleep_duration = self.post_put_delete_freq - (time.time() - self.post_put_delete_timestamps[0])
                return True, sleep_duration
            return False, 0

    def record_request(self, method):
        current_time = time.time()
        if method == "GET":
            self.get_timestamps.append(current_time)
        else:
            self.post_put_delete_timestamps.append(current_time)
