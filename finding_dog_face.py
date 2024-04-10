# 영상에서 강아지 얼굴찾기

import cv2
import dlib
from imutils import face_utils

face_landmark_detector_path = 'dogHeadDetector.dat'
face_landmark_predictor_path = 'landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(face_landmark_detector_path)
predictor = dlib.shape_predictor(face_landmark_predictor_path)

video_path = 'images/coco_song1.mp4'
output_path = 'results/coco_song1.mp4'

class Find_dog_face:
    def __init__(self):
        pass
    
    def finding(self, video_path, output_path, debug=False):
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
            
            faces = self.find_faces(frame, debug=debug)

            out.write(frame)

            if debug:
                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def find_faces(self, frame, debug=False):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dets = detector(gray_frame, 1)
        print('Found {} faces.'.format(len(dets)))

        for (i, det) in enumerate(dets):
            shape = predictor(gray_frame, det.rect)
            shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(det.rect)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if debug:
                for (i, (x, y)) in enumerate(shape):
                    cv2.circle(frame, (x, y), int(frame.shape[1]/250), (0, 0, 255), -1)
        
        return frame

def main():
    finder = Find_dog_face()
    finder.finding(video_path, output_path, debug=True)

if __name__ == '__main__':
    main()


import cv2
import dlib
from imutils import face_utils
from google.colab.patches import cv2_imshow

face_landmark_detector_path = 'library/dogHeadDetector.dat'
face_landmark_predictor_path = 'libaraylandmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(face_landmark_detector_path)
predictor = dlib.shape_predictor(face_landmark_predictor_path)

video_path = 'images/coco_song1.mp4'
output_path = 'results/coco_song1.mp4'

class Find_dog_face:
    def __init__(self):
        pass
    
    def finding(self, video_path, output_path, debug=False):
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
            
            frame = self.find_faces(frame, debug=debug)

            out.write(frame)

            if debug:
                cv2_imshow(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        out.release()

    def find_faces(self, frame, debug=False):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dets = detector(gray_frame, 1)
        print('Found {} faces.'.format(len(dets)))

        for (i, det) in enumerate(dets):
            shape = predictor(gray_frame, det.rect)
            shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(det.rect)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if debug:
                for (i, (x, y)) in enumerate(shape):
                    cv2.circle(frame, (x, y), int(frame.shape[1]/250), (0, 0, 255), -1)
        
        return frame

def main():
    finder = Find_dog_face()
    finder.finding(video_path, output_path, debug=True)

if __name__ == '__main__':
    main()