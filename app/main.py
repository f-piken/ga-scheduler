import json
from http.server import BaseHTTPRequestHandler

from app.services.scheduler import SchedulerService


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:
            content_length = int(
                self.headers.get('Content-Length', 0)
            )

            body = self.rfile.read(content_length)

            data = json.loads(body)

            result = SchedulerService.generate(
                jamaahs=data["jamaahs"],
                team_leaders=data["team_leaders"],
                muthowifs=data["muthowifs"],
                departures=data["departures"]
            )

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps(result).encode("utf-8")
            )

        except Exception as e:

            self.send_response(500)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "success": False,
                    "error": str(e)
                }).encode("utf-8")
            )