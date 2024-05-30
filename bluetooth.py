import bluetooth

class BluetoothServer:
    def __init__(self, uuid, port=1):
        self.uuid = uuid
        self.port = port
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_sock = None
        self.client_info = None

    def start_server(self):
        self.server_sock.bind(("", self.port))
        self.server_sock.listen(1)
        bluetooth.advertise_service(self.server_sock, "BluetoothServer",
                                    service_id=self.uuid,
                                    service_classes=[self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
        print("Waiting for connection...")
        self.client_sock, self.client_info = self.server_sock.accept()
        print(f"Accepted connection from {self.client_info}")

    def stop_server(self):
        if self.client_sock:
            self.client_sock.close()
        self.server_sock.close()
        print("Server stopped.")

    def receive_user_id(self):
        try:
            data = self.client_sock.recv(1024).decode('utf-8')
            print(f"Received user_id: {data}")
            return data
        except OSError as e:
            print(f"Error receiving data: {e}")
            return None

    def send_data(self, weight):
        try:
            self.client_sock.send(str(weight).encode('utf-8'))
            print(f"Sent weight: {weight}")
        except OSError as e:
            print(f"Error sending data: {e}")

if __name__ == "__main__":
    server_uuid = "00001101-0000-1000-8000-00805F9B34FB"
    server = BluetoothServer(uuid=server_uuid)
    server.start_server()

    user_id = server.receive_user_id()
    if user_id:
        # 여기서 그릇 무게 받아오는 거 필요함
        weight = 70  # 예씨
        server.send_data(weight)

    server.stop_server()
