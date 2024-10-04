import os
import cv2
import base64
from django.shortcuts import render
from django.http import JsonResponse
from ultralytics import YOLO
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image

# Load the pre-trained YOLOv8 model
model = YOLO(r'C:\Users\priya\Desktop\GeoLearn\yolov8n.pt')  # Update this path

def detect_input_type_and_process(input_path):
    file_ext = os.path.splitext(input_path)[1].lower()
    if file_ext in ['.jpg', '.jpeg', '.png']:
        return process_image(input_path, file_ext)
    elif file_ext in ['.mp4', '.avi', '.mov']:
        return process_video(input_path)
    else:
        return "Unsupported file type."

def process_image(image_path, file_ext):
    image_format = "JPEG" if file_ext in ['.jpg', '.jpeg'] else "PNG"
    
    image = cv2.imread(image_path)
    results = model(image)  # Perform inference with YOLOv8

    identified_objects = []

    for result in results:
        for bbox in result.boxes.data:
            x1, y1, x2, y2 = map(int, bbox[:4].tolist())
            confidence = float(bbox[4])
            class_id = int(bbox[5])
            class_name = model.names[class_id]

            identified_objects.append({
                'class_name': class_name,
                'confidence': confidence,
                'bbox': [x1, y1, x2, y2]
            })

            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Convert image to PIL format
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    buffer = BytesIO()
    pil_img.save(buffer, format=image_format)
    img_str = base64.b64encode(buffer.getvalue()).decode()

    img_data_url = f"data:image/{image_format.lower()};base64,{img_str}"

    return identified_objects, img_data_url


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    identified_objects = []
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)  # Perform inference with YOLOv8

        for result in results:
            for bbox in result.boxes.data:
                x1, y1, x2, y2 = map(int, bbox[:4].tolist())  # Convert tensor to list and then to int
                confidence = float(bbox[4])  # Convert tensor to float
                class_id = int(bbox[5])  # Convert tensor to int
                class_name = model.names[class_id]

                identified_objects.append({
                    'class_name': class_name,
                    'confidence': confidence,
                    'bbox': [x1, y1, x2, y2]
                })

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert frame to base64
        _, buffer = cv2.imencode('.jpeg', frame)
        frame_str = base64.b64encode(buffer).decode('utf-8')
        frames.append(frame_str)

    cap.release()

    return identified_objects, frames

def predict(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_path = default_storage.save(file.name, file)

        full_file_path = os.path.join(default_storage.location, file_path)
        identified_objects, output_path = detect_input_type_and_process(full_file_path)

        return render(request, 'pre/result.html', {
            'identified_objects': identified_objects,
            'output_image_path': output_path
        })

    return render(request, 'pre/upload.html')