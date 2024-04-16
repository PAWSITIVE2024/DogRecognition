import os
import numpy as np
from link_with_firebase import Link_firebase
from add_dog_face import Add_dog_face
from facial_recognition_for_dogs import Dog_facial_recognition

class Run:
    def __init__(self):
        self.step = 0
        self.POWER_OFF = False
    
    def run(self):
        if self.step == 0:
            # get userID from android
            user_id = '9OccDgcNSbcOl2limdvnFtcAb4E2'
            self.step += 1
        elif self.step == 1:
            link_firebase = Link_firebase(user_id)
            link_firebase.save_image()
            dog_name = link_firebase.get_name()
            if link_firebase.downloading_done == True:
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
            # 알고 있는 얼굴 찾기
            known_face_encodings = np.load('numpy/known_faces.npy')
            known_face_names = np.load('numpy/known_names.npy')
            detection = Dog_facial_recognition()
            if detection.detected_name != None:
                detected_name = detection.detected_name
            # 안드로이드로 보내기.
                
        
def main():
    run = Run()
    while run.POWER_OFF == False:
        run.run()
    
if __name__ == '__main__':
    main()