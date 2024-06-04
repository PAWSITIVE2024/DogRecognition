import os
import numpy as np
from link_with_firebase import Link_firebase
from add_dog_face import Add_dog_face
from facial_recognition_for_dogs import Dog_facial_recognition
from bluetooth import BluetoothServer

class Run:
    def __init__(self):
        self.step = 0
        self.POWER_OFF = False
        self.Process_Done = False
        self.user_id = None
    
    def run(self):
        if self.step == 0:
            # 여기서 안드로이드랑 블루투스로 연결하는 코드 계속 돌림..
            # 연결되면 그거 user_id로 선언하고 loop 종료 후 step1으로 넘어감.
            # get userID from android
            # user_id = '9OccDgcNSbcOl2limdvnFtcAb4E2'
            server = BluetoothServer(self.data_received)
            while self.user_id is None:
                time.sleep(1)
            self.step += 1
        elif self.step == 1:
            # user_id랑 맞는 firebase에 연결..
            # 폴더 자동 생성 및 이미지 저장
            link_firebase = Link_firebase(user_id)
            link_firebase.save_image()
            dog_name = link_firebase.get_name()
            if link_firebase.downloading_done:
                self.step += 1
        elif self.step == 2:
            # 이 부분 구상 다시 하기... 지금은 머리가 안돌아감...
            # 저장된 이미지 폴더에서 사진 찾아서 학습돌리기.
            image_folder = os.path.join(user_id, "images")
            face_paths = []
            for filename in os.listdir(image_folder):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    face_paths.append(os.path.join(image_folder, filename))
            adding = Add_dog_face()
            for face_path in face_paths:
                adding.add_known_face(face_path)
            if adding.DONE == True:
                self.step += 1
            # 여기까지가 사전작업
            
        elif self.step == 3:
            # firebase에서 DoggyDine/UserAccount/../Detected/Start 값이 True가 되면 step 4로 넘어가기.
            # 버튼 눌릴때까지 대기하기.
            # self.step += 1
            link_firebase = Link_firebase(self.user_id)
            if link_firebase.is_start_detection():
                self.step += 1
                
        elif self.step == 4:
            # 알고 있는 얼굴 찾기
            known_face_encodings = np.load('numpy/known_faces.npy')
            known_face_names = np.load('numpy/known_names.npy')
            detection = Dog_facial_recognition()
            if detection.detected_name != None:
                detected_name = detection.detected_name
                # 안드로이드로 보내기.
                # firebase에서 DoggyDine/UserAccount/../Detected/Detected_name에 detected_name 저장하기
                # firebase에서 DoggyDine/UserAccount/../Detected/Start 값을 다시 False로 바꿔주기
                link_firebase = Link_firebase(self.user_id)
                link_firebase.send_detected_name(detected_name)
                link_firebase.reset_start_detection()
                self.Process_Done = True

            if self.Process_Done == True:
                self.step == 3
                self.Process_Done == False

    def data_received(self, data):
        # 블루투스를 통해 데이터 수신
        self.user_id = data
                
        
def main():
    run = Run()
    while run.POWER_OFF == False:
        run.run()
    
if __name__ == '__main__':
    main()