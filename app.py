# app.py
from flask import Flask, jsonify, render_template, request
import os
import socket
from datetime import datetime

app = Flask(__name__)

# Sample data - in a real app, you'd likely use a database
items = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"},
    {"id": 3, "name": "Item 3", "description": "This is item 3"}
]

@app.route('/')
def index():
    """Home page route"""
    hostname = socket.gethostname()
    return render_template('index.html', 
                           hostname=hostname,
                           container_id=os.environ.get('HOSTNAME', 'local'),
                           current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/health')
def health():
    """Health check endpoint for the load balancer"""
    return jsonify({"status": "healthy"})

@app.route('/api/items', methods=['GET'])
def get_items():
    """API endpoint to get all items"""
    return jsonify(items)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """API endpoint to get a specific item by ID"""
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/items', methods=['POST'])
def create_item():
    """API endpoint to create a new item"""
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Invalid request"}), 400
    
    new_id = max(item["id"] for item in items) + 1 if items else 1
    new_item = {
        "id": new_id,
        "name": request.json["name"],
        "description": request.json.get("description", "")
    }
    items.append(new_item)
    return jsonify(new_item), 201

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/env')
def environment():
    """Display environment variables (useful for debugging)"""
    env_vars = {key: value for key, value in os.environ.items()}
    return jsonify(env_vars)

if __name__ == '__main__':
    # For local development only
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)