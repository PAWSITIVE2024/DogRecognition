import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
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

    def update_step(self):
        if self.process is not None:
            self.process.stdin.write('step 1\n')
            self.process.stdin.flush()

class CameraFeed(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.capture = cv2.VideoCapture(0)

    def run(self):
        while self._run_flag:
            ret, frame = self.capture.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.change_pixmap_signal.emit(convert_to_qt_format)
        self.capture.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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
        self.text_edit.setFixedHeight(self.height() // 2)  # 텍스트 박스 높이를 창 높이의 50%로 설정
        vbox.addWidget(self.text_edit)

        self.update_button = QPushButton('업데이트하기', self)
        self.update_button.clicked.connect(self.update_script)
        self.update_button.setVisible(False)  # 초기에는 보이지 않게 설정
        vbox.addWidget(self.update_button)

        self.setLayout(vbox)
        self.show()

        self.camera_feed = CameraFeed()
        self.camera_feed.change_pixmap_signal.connect(self.update_image)

    def run_script(self):
        self.worker = Worker()
        self.worker.output.connect(self.append_output)
        self.worker.start()
        self.run_button.setEnabled(False)

    def update_script(self):
        self.worker.update_step()

    def append_output(self, text):
        self.text_edit.append(text)
        if "Camera started" in text:  # 특정 출력에 따라 카메라 피드 시작
            self.camera_feed.start()
        elif "Camera stopped" in text:  # 특정 출력에 따라 카메라 피드 중지
            self.camera_feed.stop()
            self.label.setPixmap(self.default_pixmap.scaled(400, 300, Qt.KeepAspectRatio))

        if "step =" in text and "0" not in text:  # step이 0이 아니면 업데이트 버튼 표시
            self.update_button.setVisible(True)

    def update_image(self, qt_image):
        self.label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.camera_feed.stop()
        if hasattr(self, 'worker'):
            self.worker.terminate()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
