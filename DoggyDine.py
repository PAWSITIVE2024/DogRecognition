import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
import cv2

class Worker(QThread):
    output = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.process = None

    def run(self):
        self.process = subprocess.Popen(['python3', 'run.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in iter(self.process.stdout.readline, ''):
            self.output.emit(line.strip())
        self.process.stdout.close()
        self.process.wait()

class VideoPlayer(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    video_finished = pyqtSignal(QImage)  # Emit the last frame when video finishes

    def __init__(self, video_path, label_size):
        super().__init__()
        self._run_flag = True
        self.video_path = video_path
        self.label_size = label_size

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        last_frame = None
        while self._run_flag:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, self.label_size)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            last_frame = rgb_image
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.change_pixmap_signal.emit(convert_to_qt_format)
            QThread.msleep(33)  # approximately 30 frames per second
        cap.release()
        if last_frame is not None:
            h, w, ch = last_frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(last_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_finished.emit(convert_to_qt_format)  # Emit the last frame

    def stop(self):
        self._run_flag = False
        self.wait()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.step = -1

    def initUI(self):
        self.setWindowTitle('Doggy Dine')
        self.setGeometry(300, 300, 800, 600)

        vbox = QVBoxLayout()

        self.label = QLabel(self)
        self.default_pixmap = QPixmap('/home/yunjijeong/DogRecognition/images/final_icon.png')
        self.label.setPixmap(self.default_pixmap.scaled(400, 300, Qt.KeepAspectRatio))
        vbox.addWidget(self.label, alignment=Qt.AlignCenter)

        self.run_button = QPushButton('연결하기', self)
        self.run_button.clicked.connect(self.run_script)
        vbox.addWidget(self.run_button, alignment=Qt.AlignCenter)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFixedHeight(self.height() // 2)
        vbox.addWidget(self.text_edit)

        self.setLayout(vbox)
        self.show()

        self.video_player = None

        # Setup timers
        self.timers = {
            'step1': QTimer(self),
            'step2': QTimer(self),
            'step3': QTimer(self),
            'step4': QTimer(self),
            'step5': QTimer(self),
            'step6': QTimer(self),
            'step7': QTimer(self)
        }

        self.timers['step1'].timeout.connect(self.start_step2)
        self.timers['step2'].timeout.connect(self.start_step3)
        self.timers['step3'].timeout.connect(self.start_step4)
        self.timers['step4'].timeout.connect(self.step4_update)
        self.timers['step5'].timeout.connect(self.start_step6)
        self.timers['step6'].timeout.connect(self.step4_update)
        self.timers['step7'].timeout.connect(self.restart_cycle)

    def run_script(self):
        self.step = 0
        self.clear_output()
        self.append_output("시작")
        self.play_video('/home/yunjijeong/DogRecognition/results/qr.mp4')

    def play_video(self, video_path):
        if self.video_player is not None and self.video_player.isRunning():
            self.video_player.stop()
        self.video_player = VideoPlayer(video_path, (self.label.width(), self.label.height()))
        self.video_player.change_pixmap_signal.connect(self.update_image)
        self.video_player.video_finished.connect(self.video_finished)
        self.video_player.start()

    def video_finished(self, last_frame):
        self.update_image(last_frame)  # Display the last frame
        if self.step == 0:
            self.start_step1()
        elif self.step == 4:
            self.start_step5()
        elif self.step == 6:
            self.start_step7()

    def start_step1(self):
        self.step = 1
        self.clear_output()
        self.label.setPixmap(self.default_pixmap.scaled(400, 300, Qt.KeepAspectRatio))
        self.append_output("user_id : Fm8Ff8EdZcSVeNDzLEVWpnxFdJZ2")
        self.append_output("user name : 동욱")
        self.append_output("데이터 다운로드 중")
        self.timers['step1'].start(3000)  # 3초 대기

    def start_step2(self):
        self.step = 2
        self.clear_output()
        self.append_output("얼굴 학습 중")
        self.timers['step1'].stop()
        self.timers['step2'].start(3000)  # 30초 대기

    def start_step3(self):
        self.step = 3
        self.clear_output()
        self.append_output("대기 중")
        self.timers['step2'].stop()
        self.timers['step3'].start(3000)  # 30초 대기

    def start_step4(self):
        self.step = 4
        self.clear_output()
        self.play_video('/home/yunjijeong/DogRecognition/results/coco.mp4')
        self.timers['step3'].stop()
        self.timers['step4'].start(3000)

    def start_step5(self):
        if self.step == 4:
            self.step = 5
            self.label.setPixmap(QPixmap('/home/yunjijeong/DogRecognition/images/result1.jpg').scaled(400, 300, Qt.KeepAspectRatio))
            self.clear_output()
            self.append_output("코코가 인식되었습니다")
            self.timers['step4'].stop()
            self.timers['step5'].start(2000)

    def start_step6(self):
        if self.step == 5:
            self.step = 6
            self.clear_output()
            self.play_video('/home/yunjijeong/DogRecognition/results/song.mp4')
            self.timers['step5'].stop()
            self.timers['step6'].start(3000)

    def start_step7(self):
        if self.step == 6:
            self.step = 7
            self.label.setPixmap(QPixmap('/home/yunjijeong/DogRecognition/images/result0.jpg').scaled(400, 300, Qt.KeepAspectRatio))
            self.clear_output()
            self.append_output("송이가 인식되었습니다")
            self.timers['step6'].stop()
            self.timers['step7'].start(5000)  # Adjust the duration as needed

    def final_step(self):
        if self.step == 7:
            self.restart_cycle()

    def restart_cycle(self):
        self.step = 3
        self.clear_output()
        self.label.setPixmap(self.default_pixmap.scaled(400, 300, Qt.KeepAspectRatio))
        self.append_output("사료 급여가 완료돠었습니다")
        self.timers['step7'].stop()
        self.timers['step3'].start(3000)

    def step4_update(self):
        if self.step == 4:
            self.append_output("coco 카운트 완료")
        elif self.step == 6:
            self.append_output("song 카운트 완료")

    def append_output(self, text):
        self.text_edit.append(text)

    def clear_output(self):
        self.text_edit.clear()

    def update_image(self, qt_image):
        self.label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        if self.video_player is not None and self.video_player.isRunning():
            self.video_player.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
