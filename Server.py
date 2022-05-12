import socket
import selectors
import sys
import HttpRequest

localhost = '127.0.0.1'
port = 8080
selector = selectors.DefaultSelector()
listening_address = (localhost, port)

def accept_wrapper(sock):
    server_socket, client_address = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {client_address}")
    server_socket.setblocking(False)
    message = HttpRequest.request(server_socket, selector, client_address)
    selector.register(server_socket, selectors.EVENT_READ, data=message)

def eventLoop():
    try:
        while True:
            events = selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    print('initiate connection')
                    accept_wrapper(key.fileobj)
                else:
                    key.data.process_events(mask)
    except KeyboardInterrupt:
        sys.exit()

# Entry point of the program
def main():
    # Initiating the listening socket
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind(listening_address)
    lsock.listen()
    print(f"Server started listening on localhost:{listening_address[1]}")
    lsock.setblocking(False)
    # Registering the listening socket on the selector
    selector.register(lsock, selectors.EVENT_READ, data=None)
    eventLoop()

# Starting the main function of the program
if __name__ == "__main__":
    main()
