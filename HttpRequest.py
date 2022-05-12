import selectors

class request:
    
    def __init__(self, socket, selector, address):
        # ! socket is the server socket responsible for this client
        # ! selector is the selector of this object
        # ! address is the address of the client that we will response to

        self.selector = selector
        self.socket = socket
        self.address = address
        self.recv_buffer = b''
        self.send_buffer = b''
        self.requestSize = 0            # total size of the request in bytes


    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.readRequest()
        if mask & selectors.EVENT_WRITE:
            # self.writeResponse
            pass
    
    def readRequest(self):
        self.recv_buffer = self.socket.recv(10000)
        self.requestSize = len(self.recv_buffer)
        self.message = self.recv_buffer.decode('ascii')
        self.message.find('GET')
        print('get request')
        self.processGET()
        self.selector.modify(self.socket, selectors.EVENT_WRITE, data=self)
        print('reading now')
    
    def processGET(self):
        temp = self.message.split(' ')
        filename = (temp[1])[1:]
        print(filename)
        f = open(filename, "r")
        print(f.read())
        