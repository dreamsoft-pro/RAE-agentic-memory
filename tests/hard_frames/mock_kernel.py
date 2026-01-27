import random
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockKernelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_POST(self):
        # Simulate realistic RAE processing time (DB writes, Embedding generation)
        # 50ms to 300ms latency
        time.sleep(random.uniform(0.05, 0.3))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"success": true}')


if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("0.0.0.0", port), MockKernelHandler)
    print(f"Mock Kernel listening on {port}...")
    sys.stdout.flush()
    server.serve_forever()
