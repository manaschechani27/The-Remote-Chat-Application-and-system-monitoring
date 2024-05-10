import socket
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import platform

SERVER_HOST = "localhost"
SERVER_PORT = 54321
BUFFER_SIZE = 2048


def get_system_report():
    system_info = platform.uname()
    report = f"System: {system_info.system}\nNode Name: {system_info.node}\nRelease: {system_info.release}\nVersion: {system_info.version}\nMachine: {system_info.machine}\nProcessor: {system_info.processor}"
    return report


def create_client_folder(adr):
    # Extract IP address from address tuple
    client_ip = adr[0]
    # Create folder with client's IP address
    folder_name = client_ip.replace(
        ".", "_"
    ) 
    folder_path = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created for client {client_ip}")
    else:
        print(f"Folder '{folder_name}' already exists for client {client_ip}")


def handle_client(client_socket, adr, sender_email, sender_password, receiver_email):
    try:
        print(f"Accepted connection from {adr}.")
        print(f"Sender's email: {sender_email}")
        print(f"Receiver's email: {receiver_email}")

        while True:
            # Receive message from client
            data = client_socket.recv(BUFFER_SIZE).decode()

            if not data:
                break

            print(f"Message from {adr}: {data}")

            # Check for special commands
            if data.strip().lower() == "/quit":
                send_message_to_client(client_socket, "Goodbye!")
                break
            elif data.strip().lower() == "/email":
                # Generate system report
                system_report = get_system_report()

                # Send system report via email
                send_email(
                    sender_email,
                    sender_password,
                    receiver_email,
                    "System Report",
                    system_report,
                )
                send_message_to_client(client_socket, "System report sent via email.")
            elif data.strip().lower() == "/create":
                create_client_folder(adr)
                send_message_to_client(client_socket, "Folder created.")
            else:
                # Send response to the client
                response = input("Enter your response: ")
                send_message_to_client(client_socket, response)

    except ConnectionResetError:
        print(f"Connection with {adr} reset by peer.")
    except socket.error as se:
        print(f"Socket error occurred with {adr}: {se}")
    except Exception as e:
        print(f"Error handling client {adr}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {adr} closed.")


def send_message_to_client(client_socket, message):
    try:
        client_socket.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message to client: {e}")


def send_email(sender_email, sender_password, receiver_email, subject, message):
    try:
        # Set up the SMTP server
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)

        # Create a MIME multipart message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        smtp_server.send_message(msg)

        # Close the SMTP server connection
        smtp_server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


def main():
    # Get sender's email and password
    sender_email = input("Enter sender's email address: ")
    sender_password = input("Enter sender's password: ")

    # Get receiver's email address
    receiver_email = input("Enter receiver's email address: ")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            client_socket, adr = server_socket.accept()
            client_handler = threading.Thread(
                target=handle_client,
                args=(
                    client_socket,
                    adr,
                    sender_email,
                    sender_password,
                    receiver_email,
                ),
            )
            client_handler.start()

            # Send initial message to the client
            initial_message = "Hello from the server! You can start chatting. Type '/quit' to exit or '/email <message>' to send an email."
            send_message_to_client(client_socket, initial_message)
    except KeyboardInterrupt:
        print("Server shutting down.")
    except socket.error as se:
        print(f"Socket error occurred: {se}")
    except Exception as e:
        print(f"Server error occurred: {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
