import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def load_marks(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')) as f:
                return json.load(f)
        except:
            return {"Alice": 10, "Bob": 20}  # Fallback data

    def do_GET(self):
        # Load marks data
        marks_data = self.load_marks()
        
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get('name', [])
        
        # Get marks in order
        marks = [marks_data.get(name, 0) for name in names]
        
        # Prepare response
        response = {"marks": marks}
        
        # Set headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.end_headers()
        
        # Send response
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()