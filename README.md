The Remote Chat Application is a simple chat platform that enables users to communicate with each other over a network. It utilizes socket programming and threading in Python to establish connections and handle multiple clients concurrently.

Usage:
1. Server:
   - Run the `server.py` script to start the server.
   - The server will listen for incoming client connections on a specified port.

2. Client:
   - Run the `client.py` script to start the client.
   - Upon execution, the client will prompt you to enter your username.
   - Once connected to the server, you can send messages by typing them into the command line interface.
   - Received messages from other clients will be displayed in real-time.


Features:
- Real-time messaging: Send and receive messages instantly within the chat environment.
- Multi-client support: The server can handle multiple client connections concurrently.
- Simple interface: User-friendly command line interface for easy interaction.

Instructions:
1. Run the server:
python server.py

2. Run the client:
python client.py
