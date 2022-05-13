import threading
from time import sleep
import HttpRequest

recv_buffer_size = 10000

class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_addr = client_address
        print(f'Listening for client{client_address}')
    
    def run(self):
        while True:
            message = self.client_socket.recv(recv_buffer_size)
            if message:
                request = HttpRequest.Request(message.decode('ascii'))
                response = request.processRequest()
                self.client_socket.sendall(response.encode('ascii') )
                print(f'Server response\n{response}')
            else:
                sleep(100)
            