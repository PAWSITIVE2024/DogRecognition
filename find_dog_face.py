import cv2
import dlib
import imutils
from imutils import face_utils
import numpy as np
import matplotlib.pyplot as plt
import face_recognition
import time

face_landmark_detector_path = 'library/dogHeadDetector.dat'
face_landmark_predictor_path = 'library/landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(face_landmark_detector_path)
predictor = dlib.shape_predictor(face_landmark_predictor_path)

target_path = 'images/song_coco10.jpg'

class Find_dog_face:
    def __init__(self):
        pass
    
    def finding(self, org_image, debug=False):
        image = self.resize_image(org_image, target_width=200)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dets = detector(gray_image, 1)
        print('Found {} faces.'.format(len(dets)))
        face_images = []
        for (i, det) in enumerate(dets):
            shape = predictor(gray_image, det.rect)
            shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(det.rect)
            face_images.append(image[y:y+h, x:x+w].copy())

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if debug:
                for (i, (x, y)) in enumerate(shape):
                    cv2.circle(image, (x, y), int(image.shape[1]/250), (0, 0, 255), 3)
                    
        self.plt_imshow(["Original", "Find Faces"], [image, image], figsize=(16,10), result_name='find_face.jpg')
        return face_images
    
    def resize_image(self, image_path, target_width=200):
        img = cv2.imread(image_path)
        height, width = img.shape[:2]
        new_height = int((target_width / width) * height)
        resized_img = cv2.resize(img, (target_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_img

    def plt_imshow(self, title='image', img=None, figsize=(8 ,5), result_name='result.jpg'):
        plt.figure(figsize=figsize)

        if type(img) == list:
            if type(title) == list:
                titles = title
            else:
                titles = []

                for i in range(len(img)):
                    titles.append(title)

            for i in range(len(img)):
                plt.subplot(1, len(img), i + 1), plt.imshow(cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB))
                plt.title(titles[i])
                plt.xticks([]), plt.yticks([])

            plt.show()
        else:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.title(title)
            plt.xticks([]), plt.yticks([])
            plt.show()

def main():
    finding = Find_dog_face()
    finding.finding(target_path, debug=True)

if __name__ == '__main__':
    main()