import socket, threading
import sys
import HttpRequest

recv_buffer_size = 10000

class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_addr = client_address
        print(f'Listening for client{client_address}')
    
    
    def run(self):
        print (f"Connection from : {self.client_addr}")
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        message = self.client_socket.recv(recv_buffer_size)
        request = HttpRequest.Request(message.decode('ascii'))
        response = request.processRequest()
        #! notice using a loop
        #self.client_socket.sendall(response.encode('ascii'))

        #
        '''
        msg = ''
        try:
            while True:
                data = self.client_socket.recv(2048)
                msg = data.decode()
                if msg=='bye':
                    break
                print ("from client", msg)
                self.client_socket.send(bytes(msg,'UTF-8'))
        except KeyboardInterrupt:
            sys.exit()

        print ("Client at ", self.client_addr , " disconnected...")
        pass
        '''