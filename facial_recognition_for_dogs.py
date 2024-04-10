# 영상에서 강아지 구분하기
import cv2
import dlib
import face_recognition
import numpy as np
from find_dog_face import Find_dog_face

video_path = 'images/song2.mp4'
output_path = 'results/song2.mp4'

face_landmark_detector_path = 'library/dogHeadDetector.dat'
face_landmark_predictor_path = 'library/landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(face_landmark_detector_path)
predictor = dlib.shape_predictor(face_landmark_predictor_path)

class Dog_facial_recognition:
    def __init__(self, known_face_encodings, known_face_names):
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names
        self.current_name = None
        self.possible_names = set(self.known_face_names)
        self.counts = {name : 0 for name in self.possible_names}
        self.detected_name = None
    
    def detection(self, video_path, output_path):
        finding = Find_dog_face()
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Couldn't open the video.")
            return
        
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            processed_frame = self.process_frame(frame)
            out.write(processed_frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def process_frame(self, frame):
        dets_locations = self.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, dets_locations)
        
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)
            if name in self.counts:
                self.counts[name] += 1
                if self.counts[name] > 30:
                    print(f"{name} 카운트가 넘었습니다.")
                    self.counts = {name : 0 for name in self.possible_names}
                    self.detected_name = name
                    
        # for name, count in self.counts.items():
        #     print(f"{name}: {count}")

        for (top, right, bottom, left), name in zip(dets_locations, face_names):
            if name != "Unknown":
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 1)
            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 3, bottom - 3), font, 2, (0, 0, 0), 1)

        return frame

    def face_locations(self, img, number_of_times_to_upsample=1):
        def _trim_css_to_bounds(css, image_shape):
            return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)

        def _rect_to_css(rect):
            return rect.top(), rect.right(), rect.bottom(), rect.left()

        def _raw_face_locations(img, number_of_times_to_upsample=1):
            return detector(img, number_of_times_to_upsample)

        raw_locations = _raw_face_locations(img, number_of_times_to_upsample)
        return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape) for face in raw_locations]

def main():
    known_face_encodings = np.load('numpy/known_faces.npy')
    known_face_names = np.load('numpy/known_names.npy')
    detect = Dog_facial_recognition(known_face_encodings, known_face_names)
    detect.detection(video_path, output_path)

if __name__ == '__main__':
    main()
