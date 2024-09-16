import socket
import inputFunctions
import threadFunctions
from threading import Thread
from datetime import datetime

def main():
    #get server IP address and port
    serverHostIP, serverPort = inputFunctions.socketDetails()
    # prompt the client for a name
    name = input("Enter your name: ")

    # initialize TCP socket
    s = socket.socket()
    print(f"[*] Connecting to {serverHostIP}:{serverPort}...")
    # connect to the server
    s.connect((serverHostIP, serverPort))
    print("[+] Connected.")

    # make a thread that listens for messages to this client & print them
    t = Thread(target=threadFunctions.listenForMessages, args=(s,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

    while True:
        # input message we want to send to the server
        toSend =  input()
        # a way to exit the program
        if toSend.lower() == 'q':
            break
        # add the datetime & name
        dateNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        toSend = f"[{dateNow}] {name}: {toSend}"
        # finally, send the message
        s.send(toSend.encode())

    s.close()

if __name__ == "__main__":
    main()