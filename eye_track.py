import cv2
import time
import numpy as np

# Set up the webcam capture
cap = cv2.VideoCapture(0)

# Define the output file path and frame rate
out_path = 'output/'
fps = 1000

# Initialize frame count and loop indefinitely
frame_count = 0
start_time = time.time()
while frame_count < 60:
    # Read in the next frame
    ret, frame = cap.read()
    
    # Stop the loop if there are no more frames
    if not ret:
        print("problem in reading frame")
        break

    elapsed_time = time.time() - start_time
    
    if elapsed_time >= 1.0/fps:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
            # Detect faces in the grayscale image
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Check if any faces were detected
            if len(faces) > 0:
                # Get the first face detected (assuming only one face is in the frame)
                (x, y, w, h) = faces[0]
                
                # Crop the frame to focus on the eye region
                eye_width = int(0.5 * w)
                eye_height = int(0.37 * h)
                eye_x = x + int(0.4 * w)
                eye_y = y + int(0.25 * h)
                eye_frame = frame[eye_y:eye_y+eye_height, eye_x:eye_x+eye_width]
                # Increment the frame count
                frame_count += 1
                start_time = time.time()
                
                # Write the current frame to a file
                file_eye_name = out_path + 'eyes/frame_' + str(frame_count) + '.jpg'
                filename = out_path + 'face/frame_' + str(frame_count) + '.jpg'
                cv2.imwrite(file_eye_name, eye_frame)
                cv2.imwrite(filename, frame)
                
                # Display the current frame
                cv2.imshow("window", frame)
                # Display the current frame
                # cv2.imshow('window',eye_frame)
    
    # Wait for a key press and check if it's the escape key (ASCII code 27)
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release the webcam and close the output window
cap.release()
cv2.destroyAllWindows()