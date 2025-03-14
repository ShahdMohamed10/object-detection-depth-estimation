import requests
import json
import base64
import cv2
import numpy as np
import argparse
import os
from PIL import Image
import io

def test_health_endpoint(base_url):
    """Test the health check endpoint"""
    url = f"{base_url}/api/health"
    response = requests.get(url)
    print(f"Health Check Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)
    return response.status_code == 200

def test_detect_endpoint(base_url, image_path):
    """Test the detect endpoint with a local image"""
    url = f"{base_url}/api/detect"
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return False
    
    with open(image_path, 'rb') as img_file:
        files = {'image': (os.path.basename(image_path), img_file, 'image/jpeg')}
        response = requests.post(url, files=files)
    
    print(f"Detect Endpoint Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Detected {len(result['detections'])} objects:")
        for detection in result['detections']:
            print(f"  - {detection['class']} (confidence: {detection['confidence']:.2f})")
        
        # Save the processed image
        if 'processed_image' in result:
            img_data = base64.b64decode(result['processed_image'])
            img = Image.open(io.BytesIO(img_data))
            output_path = "api_result.jpg"
            img.save(output_path)
            print(f"Saved processed image to {output_path}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)
    return response.status_code == 200

def test_detect_url_endpoint(base_url, image_url):
    """Test the detect_url endpoint with an image URL"""
    url = f"{base_url}/api/detect_url"
    
    payload = {"url": image_url}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Detect URL Endpoint Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Detected {len(result['detections'])} objects:")
        for detection in result['detections']:
            print(f"  - {detection['class']} (confidence: {detection['confidence']:.2f})")
        
        # Save the processed image
        if 'processed_image' in result:
            img_data = base64.b64decode(result['processed_image'])
            img = Image.open(io.BytesIO(img_data))
            output_path = "api_result_url.jpg"
            img.save(output_path)
            print(f"Saved processed image to {output_path}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)
    return response.status_code == 200

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Object Detection API")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of the API")
    parser.add_argument("--image", default="test.jpg", help="Path to a test image")
    parser.add_argument("--image-url", default="https://ultralytics.com/images/zidane.jpg", 
                        help="URL of a test image")
    
    args = parser.parse_args()
    
    print(f"Testing API at {args.url}")
    print("-" * 50)
    
    # Test all endpoints
    health_ok = test_health_endpoint(args.url)
    detect_ok = test_detect_endpoint(args.url, args.image)
    detect_url_ok = test_detect_url_endpoint(args.url, args.image_url)
    
    # Summary
    print("Test Summary:")
    print(f"Health Endpoint: {'✅ Passed' if health_ok else '❌ Failed'}")
    print(f"Detect Endpoint: {'✅ Passed' if detect_ok else '❌ Failed'}")
    print(f"Detect URL Endpoint: {'✅ Passed' if detect_url_ok else '❌ Failed'}")
    
    if health_ok and detect_ok and detect_url_ok:
        print("\n🎉 All tests passed! The API is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the API configuration.") 