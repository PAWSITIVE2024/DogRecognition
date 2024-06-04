import os
import cv2
import dlib
import imutils
from imutils import face_utils
import numpy as np
import matplotlib.pyplot as plt
import face_recognition
from find_dog_face import Find_dog_face
import time

face_landmark_detector_path = 'library/dogHeadDetector.dat'
face_landmark_predictor_path = 'library/landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(face_landmark_detector_path)
predictor = dlib.shape_predictor(face_landmark_predictor_path)

known_face = [(("images/coco1.jpg", "images/coco2.jpeg", "images/coco6.jpg", "images/coco12.jpg", "images/coco7.jpg"), "coco"),
              (("images/song2.jpg", "images/song4.jpg", "images/song5.jpg", "images/song7.jpg", "images/song9.jpg"), "song")]
class Add_dog_face:
    def __init__(self, user_id):
        self.user_id = user_id
        self.known_face_encodings = []   
        self.known_face_names = []
        self.face_specifics = []
        self.DONE = False
    
    def get_images(self):
        user_folder = os.path.join('firebase', self.user_id)
        known_faces = []
        
        if os.path.exists(user_folder):
            pets = os.listdir(user_folder)
            for pet in pets:
                pet_folder = os.path.join(user_folder, pet)
                if os.path.isdir(pet_folder):
                    images = [os.path.join(pet_folder, file) for file in os.listdir(pet_folder) if file.endswith(('.jpg', '.jpeg', '.png'))]
                    if images:
                        known_faces.append((tuple(images), pet))
        print(known_faces)
        return known_faces
    
    def add_known_face(self):
        known_face = self.get_images()
        Finding = Find_dog_face()
        target_width = 200
        name_len = len(known_face)
        
        for i in range(name_len):
            face_image_paths = []
            name = None
            face_image_paths, name = known_face[i]
            face_specific = []
            
            for face_image_path in face_image_paths:
                print(face_image_path)
                image = Finding.resize_image(face_image_path, target_width)
                dets_locations = face_locations(image, 1)
                face_encodings = face_recognition.face_encodings(image, dets_locations)
                print('face_encodings', face_encodings)

                for face_encoding, location in zip(face_encodings, dets_locations):
                    detected_face_image = draw_label(image, location, name)
                    face_specific.append(face_encoding)
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(name)
            self.face_specifics.append(face_specific)
            
        np.save('library/known_faces.npy', self.known_face_encodings)
        np.save('library/known_names.npy', self.known_face_names)
        np.save('library/face_specifics.npy', self.face_specifics)

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
    user_id = 'TDQvhGXWwQcsFWrJ0wmnTS38d602'
    adding = Add_dog_face(user_id)
    adding.add_known_face()
    
if __name__ == '__main__':
    main()