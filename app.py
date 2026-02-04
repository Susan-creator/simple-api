from http.server import BaseHTTPRequestHandler, HTTPServer
import time

LATENCY_BUCKETS = [0.05, 0.1, 0.2, 0.5, 1, 2]
LATENCY_COUNTS = {b: 0 for b in LATENCY_BUCKETS}
LATENCY_COUNTS["+Inf"] = 0

LATENCY_SUM = 0.0
REQUEST_COUNT = 0

def observe_latency(duration):
    global LATENCY_SUM
    LATENCY_SUM += duration

    for b in LATENCY_BUCKETS:
        if duration <= b:
            LATENCY_COUNTS[b] += 1
            break
    LATENCY_COUNTS["+Inf"] += 1


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global REQUEST_COUNT
        start = time.time()

        if self.path == "/health":
            time.sleep(0.05)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Ok")

        elif self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            metrics = ""
            cumulative = 0

            for b in LATENCY_BUCKETS + ["+Inf"]:
                cumulative += LATENCY_COUNTS[b]
                metrics += (
                    f'http_request_duration_seconds_bucket{{le="{b}"}} '
                    f'{cumulative}\n'
                )

            metrics += f"http_request_duration_seconds_count {REQUEST_COUNT}\n"
            metrics += f"http_request_duration_seconds_sum {LATENCY_SUM}\n"

            self.wfile.write(metrics.encode())
            return

        else:
            self.send_response(404)
            self.end_headers()

        duration = time.time() - start
        REQUEST_COUNT += 1
        observe_latency(duration)


server = HTTPServer(("0.0.0.0", 3000), Handler)
server.serve_forever()
