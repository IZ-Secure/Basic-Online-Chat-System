# Basic-Online-Chat-System

Instructions to Test the Online Chat System
as
1. Prerequisites  
Make sure you have Python installed. 

2. Navigate to the Project Directory
Open a terminal and navigate to the directory containing Server.py and Client.py files.
Example:
cd /path/to/project/

3. Start the Server
To start the server, type: python Server.py
The server will start listening for connections and display logs for any connected clients.

4. Run the Clients
Open two or more terminal tabs to simulate multiple clients (2–5 clients). In each tab, navigate to the project directory (same as step 2).
Start the client by typing: python Client.py 
A prompt will ask you for the username for each client. Enter a unique name for each one.

5. Check Server Logs for Connected Clients
After each client connects, the server will log their IP address and port number.

6. Enter Username for Each Client
Each client will be prompted to enter a unique username. The server will display a log message indicating that the user has been added to the chat.

7. Exchange Messages Between Clients
To send a message:

On one client tab, type the username of the recipient and press Enter.

Then type the message you want to send.
The server will forward the message to the recipient client. You should see the message in the recipient's tab.

8.  Add or Remove Clients

Remove a client: Simply close the terminal tab for that client. The server will log that the client has disconnected.
Add a new client: Repeat step 4 to add more clients.
