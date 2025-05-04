# Handle data processing separately
from http.server import BaseHTTPRequestHandler
import json

# Create a smaller dataset or use a more efficient data structure
def create_sample_hr_data():
    # Simplified data generation
    return {
        "departments": ["HR", "Finance", "Engineering", "Marketing", "Sales"],
        "counts": [20, 15, 30, 10, 25]
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = create_sample_hr_data()
        self.wfile.write(json.dumps(data).encode())
        return
