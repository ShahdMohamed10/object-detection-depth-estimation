# Real-time Object Detection and Depth Estimation

Flask application for real-time object detection using YOLOv8s and depth estimation using MiDaS.

## Features

- Real-time object detection using YOLOv8s
- Depth estimation using MiDaS Small
- Web interface for camera streaming
- REST API for image processing

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Run the web application:
```bash
python run.py
```

3. Run the API server:
```bash
python api.py
```

## Web Interface

Access the web interface at http://localhost:5000 to use your camera for real-time object detection and depth estimation.

## API Usage

The project now includes a REST API that can be used to process images:

### API Endpoints

- `GET /api/health` - Check if the API is running
- `POST /api/detect` - Upload an image for object detection and depth estimation
- `POST /api/detect_url` - Process an image from a URL

### Testing the API

Use the included test script to verify the API is working:

```bash
python test_api.py --image path/to/test/image.jpg
```

## PythonAnywhere Deployment

For instructions on deploying this project to PythonAnywhere, see [README_PYTHONANYWHERE.md](README_PYTHONANYWHERE.md).

## Models

- Object Detection: YOLOv8s
- Depth Estimation: MiDaS Small

## Requirements

See requirements.txt for the full list of dependencies.

