import socket
import inputFunctions
import threadFunctions
from threading import Thread

def main():
    #get server IP address and port
    serverHostIP, serverPort = inputFunctions.socketDetails()

    # initialize list/set of all connected client's sockets
    clientSockets = set()
    # create a TCP socket
    s = socket.socket()
    # make the port as reusable port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind the socket to the address we specified
    s.bind((serverHostIP, serverPort))
    # listen for upcoming connections
    s.listen(5)
    print(f"[*] Listening as {serverHostIP}:{serverPort}")

    close = [False]
    # make a thread that listens for messages to this client & print them
    t = Thread(target=threadFunctions.serverInput, args=(close, clientSockets, serverHostIP, serverPort,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()
    while not close[0]:
        # we keep listening for new connections all the time
        clientSocket, client_address = s.accept()
        print(f"[+] {client_address} connected.")
        # add the new connected client to connected sockets
        clientSockets.add(clientSocket)
        # start a new thread that listens for each client's messages
        t = Thread(target=threadFunctions.listenForClient, args=(clientSocket, clientSockets,))
        # make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
        # start the thread
        t.start()

    # close client sockets
    for cs in clientSockets:
        cs.close()
    # close server socket
    s.close()

if __name__ == "__main__":
    main()