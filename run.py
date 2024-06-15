import os
import numpy as np
from link_with_firebase import Link_firebase
from add_dog_face import Add_dog_face
from facial_recognition_for_dogs import Dog_facial_recognition
from bluetooth import Bluetooth
from sending import Sending
from get_name import GetName
from final_IoT import Final

class Run:
    def __init__(self):
        self.step = 0
        self.POWER_OFF = False
        self.Process_Done = False
        self.user_id = None
        self.detected_name = None
        self.DONE = False
    
    def run(self):
        if self.step == 0: # 블루투스 연결하기
            print("Camera started")
            receiving = GetName()
            self.user_id = receiving.main()
            print("getting name")
            # bluetooth = Bluetooth()
            # self.user_id = bluetooth.main()
            if self.user_id is not None:
                self.step += 1
                print("Camera stopped")
        elif self.step == 1: # 이미지 저장하기
            print("Step updated to 1")
            print("Downloading Data...")
            link_firebase = Link_firebase(self.user_id)
            link_firebase.save_images()
            if link_firebase.Done:
                link_firebase.Done = False
                self.step += 1
        elif self.step == 2: # 학습하기
            print("Training...")
            adding = Add_dog_face(self.user_id)
            adding.add_known_face()
            if adding.DONE:
                self.step += 1
        elif self.step == 3: # 기다리기
            print("Waiting...")
            link_firebase = Link_firebase(self.user_id)
            link_firebase.waiting()
            if link_firebase.Done:
                self.step += 1
        elif self.step == 4: # 얼굴 찾기
            print("Detecting Face...")
            print("Camera started")
            detection = Dog_facial_recognition()
            detection.detection()
            self.detected_name = detection.detected_name
            if detection.Done:
                self.step +=1 
                print("Camera stopped")
        elif self.step == 5: # 결과 보내기
            print("Sending Results...")
            sending = Sending(self.user_id)
            sending.sending(self.detected_name)
            if sending.process_done:
                self.step += 1
        elif self.step == 6:
            print("Feeding... ")
            final = Final(self.user_id)
            final.run()
            if final.Done:
                self.DONE = True
                print("Feeding Done!!")
                self.step = 3
        
def main():
    run = Run()
    while not run.POWER_OFF:
        run.run()
    
if __name__ == '__main__':
    main()
