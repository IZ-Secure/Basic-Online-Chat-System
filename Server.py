import socket
import threading
import json


class ClassChatServer:
    def __init__(self, host="0.0.0.0", port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print("Server is running and listening for connections...") # Sever started 

        #  to store connected clients 
        self.clients = {}

    def log_clients(self):
        """Log connected clients in a readable format."""
        readable_clients = {user: "<Connected>" for user in self.clients}
        print(readable_clients)

    def handle_client(self, client_socket):
        """Handle messages from a single client."""
        username = None
        try:
            # Register username
            client_socket.send("Input your username: ".encode())
            username = client_socket.recv(1024).decode().strip()

            if not username:
                raise ValueError("Username cannot be empty.")

            if username in self.clients:
                client_socket.send(json.dumps({"status": "0", "error": "Username already taken"}).encode())
                client_socket.close()
                return

            # Add client 
            self.clients[username] = client_socket
            print(f"Add new client: {username}")
            self.log_clients()

            client_socket.send(json.dumps({"status": "1", "message": f"Welcome to ClassChat, {username}!"}).encode())

            # Handle incoming messages
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break

                try:
                    data = json.loads(message)
                    sender = data.get("sender")
                    receiver = data.get("receiver")
                    text = data.get("text")

                    if receiver in self.clients:
                        # Forward message to the receiver
                        forward_message = json.dumps({
                            "status": "1",
                            "sender": sender,
                            "text": text
                        })
                        self.clients[receiver].send(forward_message.encode())
                        print(f"Send from: {sender} to: {receiver}")
                    else:
                        # Notify sender that the receiver is not available
                        error_message = json.dumps({
                            "status": "0",
                            "error": f"User {receiver} is not connected."
                        })
                        client_socket.send(error_message.encode())
                except json.JSONDecodeError:
                    error_message = json.dumps({
                        "status": "0",
                        "error": "Invalid message format."
                    })
                    client_socket.send(error_message.encode())

        except (ValueError, ConnectionError, json.JSONDecodeError) as e:
            print(f"Error with client {username or client_socket}: {e}")
        finally:
            # Remove client from the client list if they disconnect
            if username and username in self.clients:
                del self.clients[username]
                print(f"User {username} disconnected.")
                self.log_clients()
            client_socket.close()

    def run(self):
        """Main server loop to accept connections."""
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")

            # Start a thread for the client
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()


if __name__ == "__main__":
    server = ClassChatServer()
    server.run()
