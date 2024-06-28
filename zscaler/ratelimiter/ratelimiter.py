import threading
import time


class RateLimiter:
    def __init__(self, get_limit, post_put_delete_limit, get_freq, post_put_delete_freq):
        self.lock = threading.Lock()
        self.get_requests = []
        self.post_put_delete_requests = []
        self.get_limit = get_limit
        self.post_put_delete_limit = post_put_delete_limit
        self.get_freq = get_freq
        self.post_put_delete_freq = post_put_delete_freq

    def wait(self, method):
        with self.lock:
            now = time.time()

            if method == "GET":
                if len(self.get_requests) >= self.get_limit:
                    oldest_request = self.get_requests[0]
                    if now - oldest_request < self.get_freq:
                        d = self.get_freq - (now - oldest_request)
                        return True, d
                    self.get_requests.pop(0)
                self.get_requests.append(now)

            elif method in ["POST", "PUT", "DELETE"]:
                if len(self.post_put_delete_requests) >= self.post_put_delete_limit:
                    oldest_request = self.post_put_delete_requests[0]
                    if now - oldest_request < self.post_put_delete_freq:
                        d = self.post_put_delete_freq - (now - oldest_request)
                        return True, d
                    self.post_put_delete_requests.pop(0)
                self.post_put_delete_requests.append(now)

            return False, 0

    def update_limits(self, headers):
        if "X-Ratelimit-Limit-Second" in headers:
            self.get_limit = int(headers["X-Ratelimit-Limit-Second"])
            self.post_put_delete_limit = int(headers["X-Ratelimit-Limit-Second"])
        if "X-Ratelimit-Reset" in headers:
            self.get_freq = int(headers["X-Ratelimit-Reset"])
            self.post_put_delete_freq = int(headers["X-Ratelimit-Reset"])

        # Handle minute, hour, and day limits
        if "X-RateLimit-Limit-Minute" in headers:
            self.minute_limit = int(headers["X-RateLimit-Limit-Minute"])
        if "X-RateLimit-Limit-Hour" in headers:
            self.hour_limit = int(headers["X-RateLimit-Limit-Hour"])
        if "X-RateLimit-Limit-Day" in headers:
            self.day_limit = int(headers["X-RateLimit-Limit-Day"])

        if "X-RateLimit-Remaining-Minute" in headers:
            self.remaining_minute = int(headers["X-RateLimit-Remaining-Minute"])
        if "X-RateLimit-Remaining-Hour" in headers:
            self.remaining_hour = int(headers["X-RateLimit-Remaining-Hour"])
        if "X-RateLimit-Remaining-Day" in headers:
            self.remaining_day = int(headers["X-RateLimit-Remaining-Day"])
