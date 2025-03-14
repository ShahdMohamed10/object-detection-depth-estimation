from flask import Flask, request, jsonify, render_template_string
import os
import requests
import base64
import io
from PIL import Image
import numpy as np
import json
import time

# Initialize Flask app
app = Flask(__name__)

# Simple in-memory cache for demo purposes
DEMO_OBJECTS = {
    "person": {"name": "person", "confidence": 0.92},
    "car": {"name": "car", "confidence": 0.89},
    "dog": {"name": "dog", "confidence": 0.85},
    "cat": {"name": "cat", "confidence": 0.87},
    "bicycle": {"name": "bicycle", "confidence": 0.82},
}

@app.route('/')
def index():
    """Simple web interface"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Object Detection API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            .endpoint {
                background-color: #f5f5f5;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 5px;
            }
            code {
                background-color: #eee;
                padding: 2px 5px;
                border-radius: 3px;
            }
            .note {
                color: #666;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <h1>Object Detection API</h1>
        <p>This is a lightweight API for object detection. Due to PythonAnywhere disk quota limitations, 
        this version provides simulated detection results.</p>
        
        <div class="endpoint">
            <h2>Health Check</h2>
            <p><code>GET /api/health</code></p>
            <p>Check if the API is running.</p>
            <p>Example: <a href="/api/health" target="_blank">/api/health</a></p>
        </div>
        
        <div class="endpoint">
            <h2>Detect Objects</h2>
            <p><code>POST /api/detect</code></p>
            <p>Upload an image to detect objects.</p>
            <p class="note">Note: In this lightweight version, detection is simulated.</p>
        </div>
        
        <div class="endpoint">
            <h2>Detect from URL</h2>
            <p><code>POST /api/detect_url</code></p>
            <p>Provide an image URL to detect objects.</p>
            <p class="note">Note: In this lightweight version, detection is simulated.</p>
        </div>
        
        <p>For full documentation, see the <a href="https://github.com/ShahdMohamed10/object-detection-depth-estimation" target="_blank">GitHub repository</a>.</p>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Object Detection API is running (Lightweight Version)',
        'note': 'This is a lightweight version that simulates detection results due to PythonAnywhere disk quota limitations'
    })

def _simulate_detection(image):
    """Simulate object detection on an image
    
    This function doesn't actually perform detection but returns simulated results
    to demonstrate the API structure without requiring heavy ML libraries.
    """
    # Get image dimensions
    width, height = image.size
    
    # Simulate 1-3 random detections
    num_detections = np.random.randint(1, 4)
    detections = []
    
    for _ in range(num_detections):
        # Pick a random object type
        obj_type = np.random.choice(list(DEMO_OBJECTS.keys()))
        obj_info = DEMO_OBJECTS[obj_type]
        
        # Create a random bounding box
        x1 = np.random.randint(0, width - width//3)
        y1 = np.random.randint(0, height - height//3)
        w = np.random.randint(width//5, width//2)
        h = np.random.randint(height//5, height//2)
        
        # Ensure box stays within image
        x2 = min(x1 + w, width)
        y2 = min(y1 + h, height)
        
        # Add slight randomness to confidence
        confidence = obj_info["confidence"] * np.random.uniform(0.9, 1.1)
        confidence = min(max(confidence, 0.7), 0.98)  # Keep between 0.7 and 0.98
        
        detections.append({
            "class": obj_info["name"],
            "confidence": round(confidence, 2),
            "bbox": [int(x1), int(y1), int(x2), int(y2)]
        })
    
    return detections

def _process_image_for_display(image, detections):
    """Add bounding boxes to the image based on detections"""
    from PIL import ImageDraw, ImageFont
    
    # Create a copy of the image to draw on
    img_draw = image.copy()
    draw = ImageDraw.Draw(img_draw)
    
    # Draw each detection
    for detection in detections:
        x1, y1, x2, y2 = detection["bbox"]
        label = f"{detection['class']}: {detection['confidence']:.2f}"
        
        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline="green", width=3)
        
        # Draw label background
        text_size = draw.textsize(label)
        draw.rectangle([x1, y1-text_size[1]-5, x1+text_size[0], y1], fill="green")
        
        # Draw label text
        draw.text([x1, y1-text_size[1]-5], label, fill="white")
    
    # Convert to bytes for response
    buffer = io.BytesIO()
    img_draw.save(buffer, format="JPEG")
    img_bytes = buffer.getvalue()
    
    return base64.b64encode(img_bytes).decode('utf-8')

@app.route('/api/detect', methods=['POST'])
def detect_objects():
    """API endpoint to simulate object detection in an uploaded image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    try:
        # Process the image
        img = Image.open(file.stream)
        
        # Simulate processing time
        time.sleep(1)
        
        # Get simulated detections
        detections = _simulate_detection(img)
        
        # Process image for display
        processed_image = _process_image_for_display(img, detections)
        
        return jsonify({
            'success': True,
            'detections': detections,
            'processed_image': processed_image,
            'note': 'This is a simulated result due to PythonAnywhere disk quota limitations'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/detect_url', methods=['POST'])
def detect_from_url():
    """API endpoint to simulate object detection from an image URL"""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No image URL provided'}), 400
    
    image_url = data['url']
    
    try:
        # Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            return jsonify({'error': f'Failed to download image, status code: {response.status_code}'}), 400
        
        # Process the image
        img = Image.open(io.BytesIO(response.content))
        
        # Simulate processing time
        time.sleep(1)
        
        # Get simulated detections
        detections = _simulate_detection(img)
        
        # Process image for display
        processed_image = _process_image_for_display(img, detections)
        
        return jsonify({
            'success': True,
            'detections': detections,
            'processed_image': processed_image,
            'note': 'This is a simulated result due to PythonAnywhere disk quota limitations'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 