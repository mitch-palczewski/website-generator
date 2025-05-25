import http.server
import socketserver
import threading
import webbrowser
import time
import os

PORT = 8000
HTML_FILE = "index.html"
server_thread = None

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

def open_browser():
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}/{HTML_FILE}", new=0, autoraise=True)

def start_http_server():
    threading.Thread(target=open_browser).start()
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        httpd.serve_forever()

def start_server():
    """
    Starts or opens a http server 
    """
    global server_thread
    if server_thread is None or not server_thread.is_alive():
        server_thread = threading.Thread(target=start_http_server, daemon=True)
        server_thread.start()
    threading.Thread(target=open_browser).start()

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        httpd.serve_forever()