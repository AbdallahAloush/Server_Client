import socket
import selectors
import sys
import types
import ServerMessage

#TODO: implement this as a bash argument when running the code
listenaddr = ('127.0.0.1', 8080)
sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    server_socket, client_socket = sock.accept()
    print(f'Accepted request from client {client_socket}\n')
    server_socket.setblocking(False)
    message = ServerMessage.Message(sel, server_socket, client_socket)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(server_socket, events, data=message)

    
# Initiating the listening socket 
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind(listenaddr)
listen_socket.listen()
print(f'Server started listeninig on {listenaddr[0]}: {listenaddr[1]}')
listen_socket.setblocking(False)
sel.register(listen_socket, selectors.EVENT_READ, data=None)


try:
# The event loop
    while True:
        events = sel.select(timeout= None)
        for key, mask in events:
            if key.data is None:
                # accept connection and process it
                accept_wrapper(key.fileobj)
            else:
                # service the connectoi
                message = key.data
                message.process_event(mask)
                print(key.data)
                sys.exit()
        # handle the events at the selector object
except KeyboardInterrupt:
    sys.exit()


