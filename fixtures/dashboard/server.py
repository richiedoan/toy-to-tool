"""Loopback-only deterministic metrics service with bounded fault injection."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit, parse_qs
import uuid

ASSETS = Path(__file__).resolve().parent
METRICS = [{'title': 'Revenue', 'value': '$24,500'}, {'title': 'Orders', 'value': '182'},
           {'title': 'Customers', 'value': '96'}, {'title': 'Conversion', 'value': '4.2%'}]


def create_server(port, fail_on=0):
    class Handler(BaseHTTPRequestHandler):
        calls = 0

        def log_message(self, *_):
            pass

        def do_GET(self):
            path = urlsplit(self.path)
            if path.path == '/api/metrics':
                Handler.calls += 1
                failed = 'unavailable' in parse_qs(path.query) or Handler.calls == fail_on
                request_id = str(uuid.uuid4())
                self.send_response(503 if failed else 200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Cache-Control', 'no-store')
                self.send_header('X-Request-ID', request_id)
                self.end_headers()
                if failed:
                    print(json.dumps({'event': 'metrics_unavailable', 'request_id': request_id, 'status': 503}), file=sys.stderr, flush=True)
                self.wfile.write(json.dumps({'error': 'Metrics temporarily unavailable'} if failed else METRICS).encode())
                return
            assets = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'), '/style.css': ('style.css', 'text/css')}
            if path.path not in assets:
                self.send_error(404)
                return
            name, content_type = assets[path.path]
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write((ASSETS / name).read_bytes())
    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8767)
    parser.add_argument('--fail-on', type=int, default=0)
    args = parser.parse_args()
    server = create_server(args.port, args.fail_on)
    print(json.dumps({'event': 'started', 'port': server.server_port}), flush=True)
    server.serve_forever()
