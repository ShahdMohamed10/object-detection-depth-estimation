# Object Detection and Depth Estimation API

This project provides an API for object detection and depth estimation using YOLOv8 and MiDaS models.

## Deployment on PythonAnywhere

Follow these steps to deploy this project on PythonAnywhere:

### 1. Create a PythonAnywhere Account

If you don't already have one, sign up for a PythonAnywhere account at [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/).

### 2. Upload Your Project

1. Log in to your PythonAnywhere account
2. Go to the "Files" tab
3. Create a new directory for your project (e.g., `object_detection_api`)
4. Upload all your project files to this directory:
   - You can use the "Upload a file" button in the PythonAnywhere Files interface
   - Or use Git to clone your repository if it's hosted online

### 3. Set Up a Virtual Environment

1. Go to the "Consoles" tab and start a new Bash console
2. Navigate to your project directory:
   ```bash
   cd object_detection_api
   ```
3. Create a virtual environment:
   ```bash
   mkvirtualenv --python=python3.9 object_detection_env
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Configure a Web App

1. Go to the "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.9
5. Set the path to your project directory (e.g., `/home/yourusername/object_detection_api`)
6. Configure the WSGI file:
   - Click on the WSGI configuration file link
   - Replace the contents with the following:
   ```python
   import sys
   import os
   
   path = '/home/yourusername/object_detection_api'
   if path not in sys.path:
       sys.path.append(path)
   
   from wsgi import application
   ```
   - Replace `yourusername` with your PythonAnywhere username
   - Save the file

7. Set the virtual environment path:
   - In the "Virtualenv" section, enter: `/home/yourusername/.virtualenvs/object_detection_env`
   - Replace `yourusername` with your PythonAnywhere username

8. Configure static files (if needed):
   - In the "Static files" section, add:
     - URL: `/static/`
     - Directory: `/home/yourusername/object_detection_api/static`

### 5. Download the YOLOv8 Model

1. Go back to the Bash console
2. Make sure your virtual environment is activated:
   ```bash
   workon object_detection_env
   ```
3. Navigate to your project directory:
   ```bash
   cd object_detection_api
   ```
4. Download the YOLOv8s model if it's not already included:
   ```bash
   python -c "from ultralytics import YOLO; YOLO('yolov8s.pt')"
   ```

### 6. Restart Your Web App

1. Go back to the "Web" tab
2. Click the "Reload" button for your web app

### 7. Test Your API

Your API should now be accessible at:
```
https://yourusername.pythonanywhere.com/api/health
```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns the status of the API.

### Detect Objects in Uploaded Image
```
POST /api/detect
```
Upload an image file to detect objects and estimate depth.

Example using curl:
```bash
curl -X POST -F "image=@/path/to/your/image.jpg" https://yourusername.pythonanywhere.com/api/detect
```

### Detect Objects from Image URL
```
POST /api/detect_url
```
Provide an image URL to detect objects and estimate depth.

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
      "confidence": 0.95,
      "bbox": [100, 200, 300, 400]
    },
    ...
  ],
  "processed_image": "base64_encoded_image_string"
}
```

## Troubleshooting

- If you encounter memory issues, consider upgrading your PythonAnywhere account or optimizing your models
- Check the error logs in the "Web" tab for debugging information
- Make sure all required packages are installed in your virtual environment
- Ensure the YOLOv8 model file is correctly located in your project directory 