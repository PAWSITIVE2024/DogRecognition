import os
import numpy as np
from link_with_firebase import Link_firebase
from add_dog_face import Add_dog_face
from facial_recognition_for_dogs import Dog_facial_recognition
from bluetooth import Bluetooth
from Sending import Sending

class Run:
    def __init__(self):
        self.step = 0
        self.POWER_OFF = False
        self.Process_Done = False
        self.user_id = None
    
    def run(self):
        if self.step == 0: # 블루투스 연결하기
            bluetooth = Bluetooth()
            self.user_id = bluetooth.main()
            if self.user_id is not None:
                self.step += 1
        elif self.step == 1: # 이미지 저장하기
            link_firebase = Link_firebase(user_id)
            link_firebase.save_image()
            if link_firebase.Done:
                link_firebase.Done == False
                self.step += 1
        elif self.step == 2: # 학습하기
            adding = Add_dog_face(user_id)
            adding.add_known_face()
            if adding.DONE:
                self.step += 1
        elif self.step == 3: # 기다리기
            link_firebase.waiting()
            if link_firebase.Done():
                self.step += 1
        elif self.step == 4: # 얼굴 찾기
            detection = Dog_facial_recognition()
            detection.detection()
            detected_name = detection.detected_name
            if detection.Done == True:
                self.step +=1 
        elif self.step == 5: # 결과 보내기
            sending = Sending(user_id)
            sending.sending(detected_name)
            if sending.process_done == True:
                self.step == 3
        
def main():
    run = Run()
    while run.POWER_OFF == False:
        run.run()
    
if __name__ == '__main__':
    main()