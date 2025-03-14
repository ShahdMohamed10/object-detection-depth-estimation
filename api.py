from flask import Flask, request, jsonify, send_file
import os
import cv2
import numpy as np
import base64
import io
from PIL import Image
from app.camera import Camera

# Initialize Flask app
app = Flask(__name__)

# Initialize camera with models
camera = Camera()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Object Detection and Depth Estimation API is running'
    })

@app.route('/api/detect', methods=['POST'])
def detect_objects():
    """API endpoint to detect objects and estimate depth in an uploaded image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Read and process the image
    img_bytes = file.read()
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return jsonify({'error': 'Invalid image format'}), 400
    
    try:
        # Process the image (object detection + depth estimation)
        processed_img = camera.process_frame(img)
        
        # Convert the processed image to base64 for response
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_str = base64.b64encode(buffer).decode('utf-8')
        
        # Get raw detection results
        detections = camera.detect_objects(img)
        detection_results = []
        
        for detection in detections:
            x1, y1, x2, y2, conf, cls = detection
            class_name = camera.yolo_model.names[int(cls)]
            detection_results.append({
                'class': class_name,
                'confidence': float(conf),
                'bbox': [int(x1), int(y1), int(x2), int(y2)]
            })
        
        return jsonify({
            'success': True,
            'detections': detection_results,
            'processed_image': img_str
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/detect_url', methods=['POST'])
def detect_from_url():
    """API endpoint to detect objects and estimate depth from an image URL"""
    import requests
    
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No image URL provided'}), 400
    
    image_url = data['url']
    
    try:
        # Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            return jsonify({'error': f'Failed to download image, status code: {response.status_code}'}), 400
        
        # Convert to OpenCV format
        img_bytes = response.content
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Process the image
        processed_img = camera.process_frame(img)
        
        # Convert the processed image to base64 for response
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_str = base64.b64encode(buffer).decode('utf-8')
        
        # Get raw detection results
        detections = camera.detect_objects(img)
        detection_results = []
        
        for detection in detections:
            x1, y1, x2, y2, conf, cls = detection
            class_name = camera.yolo_model.names[int(cls)]
            detection_results.append({
                'class': class_name,
                'confidence': float(conf),
                'bbox': [int(x1), int(y1), int(x2), int(y2)]
            })
        
        return jsonify({
            'success': True,
            'detections': detection_results,
            'processed_image': img_str
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 