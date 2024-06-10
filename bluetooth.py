import bluetooth

class Bluetooth:
    def __init__(self, port=1):
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.port = port
        self.client_socket = None
        self.address = None

    def start_server(self):
        self.server_socket.bind(("", self.port))
        self.server_socket.listen(1)
        print("Waiting for connection...")

    def accept_connection(self):
        self.client_socket, self.address = self.server_socket.accept()
        print(f"Accepted connection from {self.address}")

    def receive_data(self):
        try:
            data = self.client_socket.recv(1024)
            if data:
                return data.decode('utf-8')
        except OSError:
            pass
        return None

    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()
        print("Disconnected")

    def main():
        bluetooth_server = Bluetooth()
        bluetooth_server.start_server()
        bluetooth_server.accept_connection()
        user_id = bluetooth_server.receive_data()
        bluetooth_server.close_connection()
        return user_id

if __name__ == "__main__":
    bluetooth = Bluetooth()
    bluetooth.main()
    