import csv
import json
from urllib.parse import parse_qs

def handler(request, response):
    # Enable CORS
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"

    # Parse names from query string
    query = parse_qs(request.query_string.decode())
    names = query.get("name", [])

    # Load data from CSV
    marks_data = {}
    with open("marks.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            marks_data[row["name"]] = int(row["marks"])

    # Get marks in the requested order
    marks_result = [marks_data.get(name, None) for name in names]

    response.body = json.dumps({ "marks": marks_result })
    return response
