import cv2
import dlib
import imutils
from imutils import face_utils
import numpy as np
import matplotlib.pyplot as plt
from find_dog_face import Find_dog_face
from add_dog_face import Add_dog_face
import face_recognition
import time

face_landmark_detector_path = 'dogHeadDetector.dat'
face_landmark_predictor_path = 'landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(face_landmark_detector_path)
predictor = dlib.shape_predictor(face_landmark_predictor_path)

image_path = 'images/song_coco10.jpg'

class Dog_facial_recognition:
    def __init__(self):
        self.known_face_encodings = np.load('known_faces.npy')
        self.known_face_names = np.load('known_names.npy')
    
    def detection(self, image_path, size=None):
        finding = Find_dog_face()
        image = finding.resize_image(image_path, target_width=200)
        dets_locations = face_locations(image)
        face_encodings = face_recognition.face_encodings(image, dets_locations)
        
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)

        for (top, right, bottom, left), name in zip(dets_locations, face_names):
            if name != "Unknown":
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)

            cv2.rectangle(image, (left, top), (right, bottom), color, 1)
            cv2.rectangle(image, (left, bottom - 10), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 3, bottom - 3), font, 0.5, (0, 0, 0), 1)

        finding.plt_imshow("Output", image, figsize=(24, 15), result_name='output.jpg')
        
def _trim_css_to_bounds(css, image_shape):
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)

def _rect_to_css(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()

def _raw_face_locations(img, number_of_times_to_upsample=1):
    return detector(img, number_of_times_to_upsample)

def face_locations(img, number_of_times_to_upsample=1):
    return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape) for face in _raw_face_locations(img, number_of_times_to_upsample)]

def main():
    detect = Dog_facial_recognition()
    detect.detection(image_path)

if __name__ == '__main__':
    main()