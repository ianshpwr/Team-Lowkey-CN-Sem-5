from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class BackendBHandler(BaseHTTPRequestHandler):

    def send_response_with_body(self, status_code, body, content_type="text/plain"):
        body_bytes = body.encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body_bytes)))
        self.send_header("X-Backend", "B")
        self.send_header("Cache-Control", "public, max-age=30")
        self.end_headers()

        self.wfile.write(body_bytes)

    def do_GET(self):
        if self.path == "/":
            self.send_response_with_body(
                200,
                "Hello from Backend B\n"
            )

        elif self.path == "/api/status":
            data = {
                "backend": "B",
                "status": "healthy",
                "port": 3002
            }

            self.send_response_with_body(
                200,
                json.dumps(data),
                "application/json"
            )

        else:
            self.send_response_with_body(
                404,
                "Not Found\n"
            )


server = HTTPServer(("0.0.0.0", 3002), BackendBHandler)

print("Backend B running on 0.0.0.0:3002")

server.serve_forever()
