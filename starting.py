import serial
import subprocess

# 시리얼 포트 설정 (아두이노가 연결된 포트를 사용)
ser = serial.Serial('/dev/ttyACM0', 9600)

# 가상환경 경로 설정
venv_path = '/home/ahnselim/myenv/bin/activate'
script_path = '/home/ahnselim/DogRecognition/final_IoT.py'

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if line == "ButtonPressed":
            print("Button pressed! Activating virtual environment and executing script...")
            subprocess.run(['bash', '-c', f'source {venv_path} && python {script_path}'])
            break