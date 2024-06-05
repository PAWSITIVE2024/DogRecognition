# 🐶강아지 얼굴 인식 및 구별

**강아지 얼굴에서 특징점을 찾고 이를 기억해서 누가 누구인지 판단하는 알고리즘**

원본 사진으로 진행시 GPU 8GB이상 필요

사진을 resize해서 GPU 0.2GB까지 줄이기 성공 target_width으로 조절 가능

known_face에 넣을 사진은 되도록이면 표정이 없는 정면 사진. 옆면은 인지불가.

    python find_dog_face.py 

실행시 강아지 얼굴 찾는 기능만 지원
![image](https://github.com/yunjiJ00/dog_face_recognition/assets/123616936/ddcae758-76a9-4500-b410-9183ed921f57)


    python add_dog_face.py

실행시, 내가 넣어준 사진과 이름을 기억하고 이 특징점을 npy파일로 저장

    python dog_facial_recognition.py

실행시 저장했던 npy에서 특징점 불러와서 현재 사진과 비교 후, 판단.
![image](https://github.com/yunjiJ00/dog_face_recognition/assets/123616936/e7d7584d-d56c-45b9-a99e-fa861dd1420f)


전체적인 Flow Chart
![통신 (1)](https://github.com/yunjiJ00/dog_face_recognition/assets/123616936/4f89391e-0f0e-4d09-afb0-de9125fea470)

