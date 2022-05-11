import socket
import selectors
import sys

#TODO: implement this as a bash argument when running the code
listenaddr = ('127.0.0.1', 8080)
sel = selectors.DefaultSelector()

# Initiating the listening socket 
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind(listenaddr)
listen_socket.listen()
print(f'Server started listeninig on {listenaddr[0]}: {listenaddr[1]}')
listen_socket.setblocking(False)
sel.register(listen_socket, selectors.EVENT_READ, data=None)

# The event loop
while True:
    events = sel.select(timeout= None)
    for key, mask in events:
        if key.data is None:
            # accept connection and process it
        else:
            # service the connectoin
    # handle the events at the selector object
    print(events)
