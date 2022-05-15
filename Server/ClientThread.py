import threading
from time import sleep
import HttpRequest

mutex = threading.Lock()

recv_buffer_size = 10000
# we can have an index for each class


class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_addr = client_address
        self.next_request_index = 0
        self.response_index = 0
        self.threads_list = []
        print(f'Listening for client{client_address}')
    
    def heuristic_timeout(self):            
        no_of_active_threads = threading.active_count()
        timeout_period = (100/no_of_active_threads) * 2
        return timeout_period    
    
    def run(self):
        while True:
            self.client_socket.settimeout(self.heuristic_timeout()) 
            message = self.client_socket.recv(recv_buffer_size)
            if message:
                mutex.acquire()
                request_thread = HttpRequest.Request(message.decode('ascii'), self.next_request_index)
                self.threads_list.append(request_thread)
                self.next_request_index += 1
                print(f'{self.next_request_index}\n\n')
                request_thread.start()
                print ('threadstarted')
                mutex.release()

            else:
                pass

            for i in range(self.next_request_index) :
                if self.response_index == self.threads_list[i].index and self.threads_list[i].response:
                    
                    #print(f'Server response of request: {threads_list[i].index}\n{threads_list[i].response}')
                    self.client_socket.sendall(self.threads_list[i].response.encode('ascii'))
                    self.response_index +=1
                    print (f'request sent')
                else:
                    sleep(0.0001)

            