<div align=center>
  

# 🐶강아지 얼굴 인식 및 구별

**강아지 얼굴에서 특징점을 찾고 이를 기억해서 누가 누구인지 판단하는 알고리즘**

필요 라이브러리 설치

    pip install -r requirements.txt

원본 사진으로 진행시 GPU 8GB이상 필요

사진을 resize해서 GPU 0.2GB까지 줄이기 성공 target_width으로 조절 가능

known_face에 넣을 사진은 되도록이면 표정이 없는 정면 사진. 옆면은 인지불가.

    python find_dog_face.py 

실행시 강아지 얼굴 찾는 기능만 지원
  
![image](https://github.com/PAWSITIVE2024/DogRecognition/assets/123616936/e30ff46d-7964-48d7-90d4-3e692b1df088)



    python add_dog_face.py

실행시, 내가 넣어준 사진과 이름을 기억하고 이 특징점을 npy파일로 저장

    python dog_facial_recognition.py

실행시 저장했던 npy에서 특징점 불러와서 현재 사진과 비교 후, 판단.
  
![image](https://github.com/yunjiJ00/dog_face_recognition/assets/123616936/e7d7584d-d56c-45b9-a99e-fa861dd1420f)

같은 종, 같은 색의 강아지라도 구별 가능.

![image](https://github.com/PAWSITIVE2024/DogRecognition/assets/123616936/6e2e3205-0956-4eed-b73e-2b7cc8259f51)


    python run.py

실행시 인식한 안드로이드 통신부터 학습, 인지판단, 결과 송신까지 자동으로 진행

전체적인 Flow Chart

![통신 (1)](https://github.com/yunjiJ00/dog_face_recognition/assets/123616936/4f89391e-0f0e-4d09-afb0-de9125fea470)




