# Lightweight Object Detection API for PythonAnywhere

This is a lightweight version of the Object Detection API designed to work within PythonAnywhere's free tier disk quota limitations. Instead of running heavy ML models locally, this version simulates object detection results to demonstrate the API structure.

## Features

- Simulated object detection with realistic bounding boxes
- Same API endpoints as the full version
- Works within PythonAnywhere's free tier disk quota
- Simple web interface

## Deployment on PythonAnywhere

Follow these steps to deploy this lightweight version on PythonAnywhere:

### 1. Log in to PythonAnywhere

Go to https://www.pythonanywhere.com/ and log in to your account.

### 2. Clone Your Repository

1. Go to the "Consoles" tab and start a new Bash console
2. Clone your repository:
   ```bash
   git clone https://github.com/ShahdMohamed10/object-detection-depth-estimation.git
   cd object-detection-depth-estimation
   ```

### 3. Set Up a Virtual Environment

1. Create a virtual environment:
   ```bash
   mkvirtualenv --python=python3.9 object_detection_env
   ```

2. Install the minimal requirements:
   ```bash
   pip install -r requirements_minimal.txt
   ```

### 4. Configure a Web App

1. Go to the "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.9
5. Enter the path to your project (e.g., `/home/yourusername/object-detection-depth-estimation`)

### 5. Configure the WSGI File

1. Click on the WSGI configuration file link
2. Replace the contents with:
   ```python
   import sys
   import os
   
   path = '/home/yourusername/object-detection-depth-estimation'
   if path not in sys.path:
       sys.path.append(path)
   
   from cloud_wsgi import application
   ```
3. Replace `yourusername` with your PythonAnywhere username
4. Save the file

### 6. Set the Virtual Environment Path

1. In the "Virtualenv" section, enter: `/home/yourusername/.virtualenvs/object_detection_env`
2. Replace `yourusername` with your PythonAnywhere username

### 7. Restart Your Web App

Click the "Reload" button for your web app.

### 8. Test Your API

Your API should now be accessible at:
```
https://yourusername.pythonanywhere.com/
```

## API Endpoints

### Web Interface
```
GET /
```
A simple web interface that explains the available endpoints.

### Health Check
```
GET /api/health
```
Returns the status of the API.

### Detect Objects in Uploaded Image
```
POST /api/detect
```
Upload an image file to simulate object detection.

Example using curl:
```bash
curl -X POST -F "image=@/path/to/your/image.jpg" https://yourusername.pythonanywhere.com/api/detect
```

### Detect Objects from Image URL
```
POST /api/detect_url
```
Provide an image URL to simulate object detection.

Example using curl:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://example.com/image.jpg"}' https://yourusername.pythonanywhere.com/api/detect_url
```

## Response Format

The API returns JSON responses with the following structure:

```json
{
  "success": true,
  "detections": [
    {
      "class": "person",
      "confidence": 0.92,
      "bbox": [100, 200, 300, 400]
    },
    ...
  ],
  "processed_image": "base64_encoded_image_string",
  "note": "This is a simulated result due to PythonAnywhere disk quota limitations"
}
```

## Upgrading to the Full Version

If you need the full functionality with actual object detection and depth estimation:

1. Upgrade your PythonAnywhere account to a paid plan with more disk space
2. Use the original `api.py` and `wsgi.py` files instead of the cloud versions
3. Install the full requirements from `requirements.txt`

## Troubleshooting

- If you encounter any issues, check the error logs in the "Web" tab
- Make sure all required packages are installed in your virtual environment
- If you're still having disk quota issues, try removing unnecessary files from your account 