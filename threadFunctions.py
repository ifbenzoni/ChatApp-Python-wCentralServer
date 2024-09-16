import socket

def listenForMessages(s):
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

def listenForClient(cs, clientSockets):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            clientSockets.remove(cs)
        # iterate over all connected sockets
        for clientSocket in clientSockets:
            # and send the message
            clientSocket.send(msg.encode())

def serverInput(close, clientSockets, serverHostIP, serverPort):
    while True:
        # input message we want to send to the server
        checkExit = input()
        # a way to exit the program
        if checkExit.lower() == 'exit':
            s = socket.socket()
            s.connect((serverHostIP, serverPort))
            # iterate over all connected sockets
            for clientSocket in clientSockets:
                # and send the message
                clientSocket.send("[-] Server Closed".encode())
            close[0] = True