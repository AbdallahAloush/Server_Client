import threading
from time import sleep
import HttpRequest
import concurrent.futures

recv_buffer_size = 10000

class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_addr = client_address
        print(f'Listening for clien t{client_address}')

    def heuristic_timeout(self):            
        no_of_active_threads = threading.active_count()
        timeout_period = (100/no_of_active_threads) * 2
        return timeout_period



    def run(self):
        i = 0 
        executor = concurrent.futures.ThreadPoolExecutor()
        response_pipe = []
        while True:
            self.client_socket.settimeout(self.heuristic_timeout()) 
            message = self.client_socket.recv(recv_buffer_size)
            if message:
                #request = HttpRequest.Request(message.decode('ascii'))
                #thread = threading.Thread(target = request.processRequest())
                #thread.start()
                #with concurrent.futures.ThreadPoolExecutor() as executor:
                request = HttpRequest.Request(message.decode('ascii'),i)
                future = executor.submit(request.processRequest)
                response, response_id = future.result()  
                response_pipe.append((response,response_id))
                i += 1
                #response = request.processRequest()
                for j in range (0,i-1):
                    for a_response in response_pipe:
                        if a_response[j][1] == j:
                            self.client_socket.sendall(response.encode('ascii') )

                            
                print(f'Server response\n{response}')
            else:
                pass
            