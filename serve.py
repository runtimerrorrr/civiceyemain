import http.server
import socketserver
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, 'dist')
DIRECTORY = DIST_DIR if os.path.exists(DIST_DIR) else BASE_DIR

PORT = 5173

class CivicEyeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_GET(self):
        # Fallback to index.html for SPA routing
        path = self.translate_path(self.path)
        if not os.path.exists(path) and not '.' in os.path.basename(self.path):
            self.path = '/index.html'
        return super().do_GET()

def run_server():
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CivicEyeHandler) as httpd:
        print("============================================================")
        print("  CivicEye Web Application Server (Visakhapatnam)")
        print(f"  Local URL: http://localhost:{PORT}")
        print(f"  Serving Directory: {DIRECTORY}")
        print("============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down CivicEye server...")
            httpd.shutdown()

if __name__ == '__main__':
    run_server()
