import subprocess
import cv2
import numpy as np
from pyzbar import pyzbar

class GetName():
    def __init__(self):
        self.user_id = None
        self.Done = False
    def waiting(self):


    def decode_qr_code(self, frame):
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            self.user_id = obj.data.decode("utf-8")
            print(f"User ID: {self.user_id}")
            self.Done = True
        return frame

    def capture_frame(self):
        # libcamera-jpeg를 사용하여 이미지를 캡처하고 메모리로 읽음
        result = subprocess.run(['libcamera-jpeg', '-o', '-', '--width', '640', '--height', '480'], capture_output=True)
        if result.returncode == 0:
            # 바이트 데이터를 numpy 배열로 변환
            np_arr = np.frombuffer(result.stdout, np.uint8)
            # OpenCV를 사용하여 이미지 디코딩
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            return frame
        else:
            print(f"이미지 캡처 실패: {result.stderr}")
            return None

    def main(self):
        print('starting')
        while True:
            frame = self.capture_frame()
            if frame is None:
                break

            frame = self.decode_qr_code(frame)
            # cv2.imshow("QR Code Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if self.user_id:
                break

        cv2.destroyAllWindows()
        if self.user_id is not None:
            if not firebase_admin._apps:
                self.cred = credentials.Certificate('library/doggy-dine-firebase-adminsdk-6tcsx-e66d564d1b.json')
                firebase_admin.initialize_app(self.cred, {'databaseURL' : "https://doggy-dine-default-rtdb.firebaseio.com/"})
                self.doggydine_ref = db.reference('/DoggyDine/UserAccount')
                self.doggydine_ref.child(f'{self.user_id}').update({'QR' : True})
        return self.user_id

def main():
    receiving = GetName()
    user_id = receiving.main()

if __name__ == "__main__":
    main()
