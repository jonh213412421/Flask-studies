# amostra de código usando a biblioteca ngrok
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import ngrok
import threading

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = bytes("Hello", "utf-8")
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

def start_ngrok():
    # Set your Ngrok authtoken (replace 'your-authtoken-here' with your actual token)
    ngrok.set_auth_token('2WcMKktzMXxQOeeb1sNMlwqL1c2_5yhzJGp2hQ5LmhEZ6YUJS')  # Insert your Ngrok authtoken here

    # Start the Ngrok tunnel on port 8000
    public_url = ngrok.connect(8000)  # 8000 is the port the HTTP server will listen on
    print(f"Ngrok tunnel established at {public_url}")
    return public_url

def run_server():
    # Start the HTTP server
    logging.basicConfig(level=logging.INFO)
    server = HTTPServer(("localhost", 8000), HelloHandler)
    print("Starting HTTP server on localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    # Start Ngrok in a separate thread
    ngrok_thread = threading.Thread(target=start_ngrok)
    ngrok_thread.daemon = True
    ngrok_thread.start()

    # Start the HTTP server in the main thread
    run_server()
