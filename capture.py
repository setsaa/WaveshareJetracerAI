import cv2
import numpy as np
import socket

# Capture stream from the Jetson Nano
cap = cv2.VideoCapture(
    "udpsrc port=5000 ! application/x-rtp, encoding-name=H264 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink",
    cv2.CAP_GSTREAMER
)

def preprocess_image(image, target_size=(160, 120)):
    image = cv2.resize(image, target_size)
    image = image / 255.0
    return image.transpose(2, 0, 1)  # CHW format

# Set up socket to send preprocessed images to Jetson Nano
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    input_tensor = preprocess_image(frame)
    data = input_tensor.tobytes()

    # Send tensor data to Jetson Nano
    sock.sendto(data, ("<jetson_nano_ip>", 5001))  # Replace with Nano IP
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
sock.close()
