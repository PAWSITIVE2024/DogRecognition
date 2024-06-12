import smbus2
import time
import struct
import subprocess

I2C_ADDRESS = 0x08
bus = smbus2.SMBus(1)

# 가상환경 경로 설정
venv_path = '/home/ahnselim/myenv/bin/activate'
script_path = '/home/ahnselim/DogRecognition/final_IoT.py'

def read_i2c():
    try:
        # 4바이트 데이터 읽기
        data = bus.read_i2c_block_data(I2C_ADDRESS, 0, 4)
        # float으로 변환
        weight = struct.unpack('f', bytes(data[:4]))[0]
        
        return weight
    except OSError as e:
        print(f"Error reading from I2C: {e}")
        return None

while True:
    weight = read_i2c()
    if weight is not None:
        print(f"Received weight: {weight}")
        
        if weight == 5000.0:
            print("Button is pressed, starting....")
            try:
                result = subprocess.run(['bash', '-c', f'source {venv_path} && python {script_path}'], check=True, capture_output=True, text=True)
                print("Button pressed! Activating virtual environment and executing script...")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                print(f"Command output: {e.output}")
                print(f"Return code: {e.returncode}")
            break
    time.sleep(1)
