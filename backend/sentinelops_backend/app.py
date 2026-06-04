import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .services.audit_ingest import build_audit_record


class SentinelOpsHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/api/audits":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        try:
            audit = build_audit_record(payload)
        except ValueError as error:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(error)}).encode("utf-8"))
            return
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(audit).encode("utf-8"))


def run(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = HTTPServer((host, port), SentinelOpsHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()

