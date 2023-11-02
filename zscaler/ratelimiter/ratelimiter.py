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
