import socket, sys
import ClientThread
# sys module is used for handling bash arguments
# ClientThread is a module responsible for making a thread for each new connection

def bashArguments():            # A function that handles bash arguments 
    arg_count = len(sys.argv)
    
    if arg_count == 1:          # No arguments
        localhost = '127.0.0.1'
        port = 80
    elif arg_count == 2:        # Entered only the port number
        localhost = '127.0.0.1'
        port = int(sys.argv[1])
    else:                       # Entered the IP and port number
        localhost = sys.argv[1]
        port = int(sys.argv[2])

    return (localhost, port)

def main():
    listen_addr = bashArguments()
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