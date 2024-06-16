import cv2

# Open the video capture device (default camera)
cap = cv2.VideoCapture(0)  # 0 for default camera, 1 for second camera, etc.

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# Define the codec and create VideoWriter object
# FourCC is a 4-byte code used to specify the video codec
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for .mp4 format
out = cv2.VideoWriter('output1.mp4', fourcc, 20.0, (640, 480))  # Adjust frame size and FPS as needed

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Write the frame into the file 'output.mp4'
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
