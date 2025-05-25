import http.server
import socketserver
import threading
import webbrowser
import time
import os

PORT = 8000
HTML_FILE = "index.html"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

def open_browser():
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}/{HTML_FILE}")

def serve_localhost():
    threading.Thread(target=open_browser).start()
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        httpd.serve_forever()