import socket
import selectors
import types
import sys

from requests import request
import HttpRequest

localhost = '127.0.0.1'
port = 8080

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = HttpRequest.request(conn, sel, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)

sel = selectors.DefaultSelector(    )
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((localhost, port))
lsock.listen()
print(f"Listening on {(localhost, port)}")
lsock.setblocking(False)
events = selectors.EVENT_READ
sel.register(lsock,events, data=None)

# event loop 
try:
    while True:
        events = sel.select(timeout= None)
        for key, mask in events:
            if key.data is None:
                print('initiate connection')
                accept_wrapper(key.fileobj)
            else:
                key.data.process_events(mask)

except KeyboardInterrupt:
    sys.exit()
