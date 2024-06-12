import serial
import subprocess

# 시리얼 포트 설정 (아두이노가 연결된 포트를 사용)
ser = serial.Serial('/dev/ttyACM0', 9600)

# 가상환경 경로 설정
script_path = '/home/pi/final_IoT.py'

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if line == "ButtonPressed":
            print("Button pressed! Executing script in virtual environment...")
            subprocess.run(['python3', script_path])