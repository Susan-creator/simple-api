from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        now = datetime.datetime.now().isoformat()
        print(f"[{now}] Request received: {self.path}")

        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

server = HTTPServer(("0.0.0.0", 3000), Handler)
print("Server starting on port 3000")
server.serve_forever()
