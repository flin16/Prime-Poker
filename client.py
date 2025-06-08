import socket

PORT = 8888
HOST = "127.0.0.1"


def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            message = input("Enter message to send to server: ")
            if message.lower() == "exit":
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f"Received from server: {data.decode()}")


if __name__ == "__main__":
    connect_to_server()
