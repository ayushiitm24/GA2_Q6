from http.server import BaseHTTPRequestHandler
from json import dumps, loads
import os
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def _load_marks_data(self):
        try:
            # Get the absolute path to the JSON file
            dir_path = os.path.dirname(os.path.realpath(__file__))
            json_path = os.path.join(dir_path, 'q-vercel-python.json')
            
            with open(json_path) as f:
                return loads(f.read())
        except Exception as e:
            print(f"Error loading marks data: {e}")
            return {}

    def do_GET(self):
        # Load marks data from JSON file
        marks_data = self._load_marks_data()
        
        # Parse query parameters
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        # Get all 'name' parameters
        names = params.get('name', [])
        
        # Get marks for each name (default to 0 if name not found)
        marks = [marks_data.get(name, 0) for name in names]
        
        # Prepare response
        response = {
            "marks": marks
        }
        
        # Set headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Send response
        self.wfile.write(dumps(response).encode('utf-8'))
        return

    def do_OPTIONS(self):
        # Handle OPTIONS method for CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()