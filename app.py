from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime

REQUEST_COUNT = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global REQUEST_COUNT
        REQUEST_COUNT += 1

        now = datetime.datetime.now().isoformat()
        print(f"[{now}] Request received: {self.path}")

        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

        elif self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            metrics = f"""# HELP requests_total Total HTTP requests
# TYPE requests_total counter
requests_total {REQUEST_COUNT}
"""
            self.wfile.write(metrics.encode())

        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(("0.0.0.0", 3000), Handler)
server.serve_forever()
