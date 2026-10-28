"""Local two-user note service; public demo accounts and disposable records only."""
import argparse
import hashlib
import hmac
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import sqlite3
import time
import uuid

ASSETS = Path(__file__).resolve().parent
USERS = {name: hashlib.pbkdf2_hmac('sha256', (name + '-demo').encode(), (name + '-fixture-salt').encode(), 600000)
         for name in ('alice', 'bob')}


def create_server(port, data_dir, session_seconds=1800):
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    database = data_dir / 'notes.sqlite'
    with sqlite3.connect(database) as db:
        db.execute('CREATE TABLE IF NOT EXISTS notes (id TEXT PRIMARY KEY, owner TEXT NOT NULL, text TEXT NOT NULL)')
        db.executemany('INSERT OR IGNORE INTO notes VALUES (?, ?, ?)',
                       [('note-a', 'alice', 'Alice working note'), ('note-b', 'bob', 'Bob working note')])
    sessions = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def reply(self, status, payload, cookie=None):
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            if cookie:
                self.send_header('Set-Cookie', cookie)
            self.end_headers()
            self.wfile.write(body)

        def identity(self):
            cookie = SimpleCookie()
            try:
                cookie.load(self.headers.get('Cookie', ''))
                token = cookie['session'].value if 'session' in cookie else ''
            except Exception:
                token = ''
            session = sessions.get(token)
            if not session or session[1] <= time.monotonic():
                sessions.pop(token, None)
                return None, token
            return session[0], token

        def payload(self):
            length = int(self.headers.get('Content-Length', '0'))
            if length > 4096 or length < 0:
                raise ValueError('Invalid length')
            if self.headers.get_content_type() != 'application/json':
                raise ValueError('JSON required')
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError('Object required')
            return data

        def do_POST(self):
            if self.path == '/api/logout':
                _, token = self.identity()
                sessions.pop(token, None)
                self.reply(200, {'ok': True}, 'session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0')
                return
            if self.path != '/api/login':
                self.reply(404, {'error': 'Not found'})
                return
            try:
                data = self.payload()
                name, password = data.get('username'), data.get('password')
                if not isinstance(name, str) or not isinstance(password, str) or name not in USERS:
                    raise ValueError('Invalid credentials')
                digest = hashlib.pbkdf2_hmac('sha256', password.encode(), (name + '-fixture-salt').encode(), 600000)
                if not hmac.compare_digest(digest, USERS[name]):
                    raise ValueError('Invalid credentials')
            except (ValueError, json.JSONDecodeError):
                self.reply(401, {'error': 'Invalid credentials'})
                return
            token = secrets.token_urlsafe(32)
            sessions[token] = (name, time.monotonic() + session_seconds)
            self.reply(200, {'username': name}, f'session={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age={session_seconds}')

        def do_GET(self):
            static = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'), '/style.css': ('style.css', 'text/css')}
            if self.path in static:
                name, content_type = static[self.path]
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.end_headers()
                self.wfile.write((ASSETS / name).read_bytes())
                return
            user, _ = self.identity()
            if not user:
                self.reply(401, {'error': 'Sign in required'})
                return
            with sqlite3.connect(database) as db:
                db.row_factory = sqlite3.Row
                if self.path == '/api/notes':
                    rows = db.execute('SELECT id, owner, text FROM notes WHERE owner = ?', (user,)).fetchall()
                    self.reply(200, [dict(row) for row in rows])
                    return
                if self.path.startswith('/api/notes/'):
                    note_id = self.path.removeprefix('/api/notes/')
                    row = db.execute('SELECT id, owner, text FROM notes WHERE id = ? AND owner = ?', (note_id, user)).fetchone()
                    self.reply(200, dict(row)) if row else self.reply(404, {'error': 'Not found'})
                    return
            self.reply(404, {'error': 'Not found'})

        def do_PATCH(self):
            user, _ = self.identity()
            if not user:
                self.reply(401, {'error': 'Sign in required'})
                return
            if not self.path.startswith('/api/notes/'):
                self.reply(404, {'error': 'Not found'})
                return
            try:
                data = self.payload()
                text = data.get('text')
                if set(data) != {'text'} or not isinstance(text, str) or len(text) > 1000:
                    raise ValueError('Invalid note')
            except (ValueError, json.JSONDecodeError):
                self.reply(422, {'error': 'Use plain text up to 1000 characters'})
                return
            note_id = self.path.removeprefix('/api/notes/')
            with sqlite3.connect(database) as db:
                changed = db.execute('UPDATE notes SET text = ? WHERE id = ? AND owner = ?', (text, note_id, user)).rowcount
            self.reply(200, {'ok': True}) if changed else self.reply(404, {'error': 'Not found'})

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8766)
    parser.add_argument('--data-dir', type=Path, required=True)
    parser.add_argument('--session-seconds', type=int, default=1800)
    args = parser.parse_args()
    server = create_server(args.port, args.data_dir, args.session_seconds)
    print(json.dumps({'event': 'started', 'port': server.server_port}), flush=True)
    server.serve_forever()
