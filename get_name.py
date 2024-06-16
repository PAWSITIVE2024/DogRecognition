import cv2
import numpy as np
from pyzbar import pyzbar
import firebase_admin
from firebase_admin import credentials, db

class GetName():
    def __init__(self):
        self.user_id = None
        self.Done = False
        self.capture = cv2.VideoCapture(0)

    def decode_qr_code(self, frame):
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            self.user_id = obj.data.decode("utf-8")
            print(f"User ID: {self.user_id}")
            self.Done = True
            # Draw a red rectangle around the QR code
            points = obj.polygon
            if len(points) == 4:
                cv2.line(frame, tuple(points[0]), tuple(points[1]), (0, 0, 255), 2)
                cv2.line(frame, tuple(points[1]), tuple(points[2]), (0, 0, 255), 2)
                cv2.line(frame, tuple(points[2]), tuple(points[3]), (0, 0, 255), 2)
                cv2.line(frame, tuple(points[3]), tuple(points[0]), (0, 0, 255), 2)
        return frame

    def capture_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            print("Failed to capture image")
            return None
        return frame

    def main(self):
        print('starting')
        while True:
            frame = self.capture_frame()
            if frame is None:
                break

            frame = self.decode_qr_code(frame)
            cv2.imshow("QR Code Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if self.user_id:
                break

        self.capture.release()
        cv2.destroyAllWindows()
        if self.user_id is not None:
            if not firebase_admin._apps:
                self.cred = credentials.Certificate('library/doggy-dine-firebase-adminsdk-6tcsx-e66d564d1b.json')
                firebase_admin.initialize_app(self.cred, {'databaseURL': "https://doggy-dine-default-rtdb.firebaseio.com/"})
            self.doggydine_ref = db.reference('/DoggyDine/UserAccount')
            self.doggydine_ref.child(f'{self.user_id}').update({'QR': True})
        return self.user_id

def main():
    receiving = GetName()
    user_id = receiving.main()

if __name__ == "__main__":
    main()
