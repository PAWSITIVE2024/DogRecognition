import cv2
from pyzbar import pyzbar

class GetName():
    def __init__(self):
        self.user_id = None
        self.Done = False

    def decode_qr_code(self, frame):
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            self.user_id = obj.data.decode("utf-8")
            print(f"User ID: {self.user_id}")
            self.Done = True
        return frame

    def main(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = self.decode_qr_code(frame)
            cv2.imshow("QR Code Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if self.user_id:
                break

        cap.release()
        cv2.destroyAllWindows()
        return self.user_id

def main():
    receiving = GetName()
    user_id = receiving.main()

if __name__ == "__main__":
    main()