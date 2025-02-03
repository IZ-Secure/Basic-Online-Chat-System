import socket
import threading
import json


def listen_for_messages(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Disconnected from server")
                break

            #  display the received JSON message
            try:
                data = json.loads(message)
                if data.get("status") == "1":
                    sender = data.get("sender")
                    text = data.get("text")
                    if sender != username:
                        # Message from other user
                        print(f"<{sender}>: {text}")
                elif data.get("status") == "0":
                    # Error message from the server
                    error = data.get("error")
                    print(f"Error: {error}")
            except json.JSONDecodeError:
                # If the message is not JSON , just show as is 
                print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def client_program():
    host = "127.0.0.1"  
    port = 12345        

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Receive  username 
    print(client_socket.recv(1024).decode(), end="")
    username = input().strip()
    client_socket.send(username.encode())

    # Receive the welcome message from server
    welcome_message = client_socket.recv(1024).decode()
    try:
        data = json.loads(welcome_message)
        if data.get("status") == "1":
            print(data.get("message"))
    except json.JSONDecodeError:
        print(welcome_message)

    # Start listening for messages in a different  thread
    threading.Thread(target=listen_for_messages, args=(client_socket, username), daemon=True).start()

    while True:
        try:
            # Ask for the recipient's username
            receiver = input().strip()
            if not receiver:
                print("Receiver name cannot be empty.")
                continue

            # Ask for the message text
            text = input(f"<{username}>: ").strip()
            if not text:
                print("Message cannot be empty.")
                continue

            # Send the message in JSON format
            message = json.dumps({
                "sender": username,
                "receiver": receiver,
                "text": text
            })
            client_socket.send(message.encode())

            # Format the sent message for display
            print(f"<{username}>: {receiver}: {text}")
        except Exception as e:
            print(f"Error sending message: {e}")
            break


if __name__ == "__main__":
    client_program()
