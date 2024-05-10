import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 54321
BUFFER_SIZE = 2048

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                break
            print("Received:", data)
        except ConnectionResetError:
            print("Server closed the connection.")
            break
        except socket.error as se:
            print(f"Socket error occurred: {se}")
            break

def send_messages(client_socket):
    while True:
        try:
            message = input("Enter your message: ")
            client_socket.sendall(message.encode())
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error sending message: {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    client_socket.close()

if __name__ == "__main__":
    main()
