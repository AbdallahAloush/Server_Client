import socket, threading
import ClientThread


localhost = '127.0.0.1'
port = 80

listen_addr = (localhost, port)


def main():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind(listen_addr)
    print(f'Started listening for requests on localhost:{listen_addr[1]}')
    while True:
        lsock.listen(1)
        client_sock, client_address = lsock.accept()
        new_thread = ClientThread.ClientThread(client_address, client_sock)
        new_thread.start()
        
# Starting the main function of the program
if __name__ == "__main__":
    main()