import cv2
import dlib
import imutils
from imutils import face_utils
import numpy as np
import matplotlib.pyplot as plt
import face_recognition
from find_dog_face import Find_dog_face
import time

face_landmark_detector_path = 'dogHeadDetector.dat'
face_landmark_predictor_path = 'landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(face_landmark_detector_path)
predictor = dlib.shape_predictor(face_landmark_predictor_path)

first_face = ("images/coco1.jpg", "coco")
second_face = ("images/song5.jpg", "song")

class Add_dog_face:
    def __init__(self):
        self.known_face_encodings = []   
        self.known_face_names = []
    
    def add_known_face(self, face_image_path, name):
        Finding = Find_dog_face()
        target_width = 200
        image = Finding.resize_image(face_image_path, target_width)
        dets_locations = face_locations(image, 1)
        face_encodings = face_recognition.face_encodings(image, dets_locations)

        for face_encoding, location in zip(face_encodings, dets_locations):
            detected_face_image = draw_label(image, location, name)
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(name)
        
        np.save('known_faces.npy', self.known_face_encodings)
        np.save('known_names.npy', self.known_face_names)
            
        Finding.plt_imshow(["Input Image", "Detected Face"], [image, detected_face_image], result_name='known_face.jpg')

def _trim_css_to_bounds(css, image_shape):
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)

def _rect_to_css(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()

def _raw_face_locations(img, number_of_times_to_upsample=1):
    return detector(img, number_of_times_to_upsample)

def face_locations(img, number_of_times_to_upsample=1):
    return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape) for face in _raw_face_locations(img, number_of_times_to_upsample)]    

def draw_label(input_image, coordinates, label):
    image = input_image.copy()
    (top, right, bottom, left) = coordinates
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 5)
    cv2.putText(image, label, (left - 10, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 3)
    return image

def main():
    # finding = Find_dog_face(target_image)
    adding = Add_dog_face()
    # finding.finding(debug=True)
    adding.add_known_face(first_face[0], first_face[1])
    adding.add_known_face(second_face[0], second_face[1])
    
if __name__ == '__main__':
    main()