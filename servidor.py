# -*- coding: utf-8 -*-
# Uso: sudo python3 servidor.py  (macOS requiere sudo para acceso USB)
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from escpos.printer import Usb

SEP = '================================'


class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, {})

    def do_POST(self):
        if self.path != '/imprimir':
            return self._send(404, {'ok': False, 'error': 'ruta no encontrada'})
        p = None
        try:
            data = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            p = Usb(0x0416, 0x5011, profile='TM-T88II')
            for ln in data['lines']:
                t = ln.get('t')
                if t == 'sep':
                    p.set(align='left', bold=False)
                    p.text(SEP + '\n')
                else:
                    p.set(align='center' if t == 'c' else 'left', bold=bool(ln.get('bold')))
                    p.text(str(ln.get('txt', ''))[:32] + '\n')
            p.ln(3)
            p.cut()
            self._send(200, {'ok': True})
        except Exception as e:
            self._send(500, {'ok': False, 'error': str(e)})
        finally:
            if p:
                try:
                    p.close()
                except Exception:
                    pass


if __name__ == '__main__':
    print('Escuchando en http://localhost:8765')
    HTTPServer(('localhost', 8765), H).serve_forever()
