import selectors

recv_buffer_size = 10000

class request:
    
    def __init__(self, socket, selector, address):
        # ! socket is the server socket responsible for this client
        # ! selector is the selector of this object
        # ! address is the address of the client that we will response to

        self.selector = selector
        self.socket = socket
        self.address = address
        self.message = ''           # ASCII decoded message
        self.recv_buffer = b''
        self.send_buffer = b''
        self.requestSize = 0            # total size of the request in bytes
        self.header_fields = dict()
        self.body = ''


    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.readRequest()
        if mask & selectors.EVENT_WRITE:
            # self.writeResponse
            pass
    
    def readRequest(self):
        self.recv_buffer = self.socket.recv(recv_buffer_size)
        self.requestSize = len(self.recv_buffer)     # will use this to check that we have the complete message by comparing it to conten length in post requests
        self.message += self.recv_buffer.decode('ascii')   
        print(self.message)
        header = self.message.partition('\r\n\r\n')[0]
        print(header)
        print(self.message)
        self.body += self.message.partition('\r\n\r\n')[2]
        requestLine = self.message.partition('\r\n')[0]
        method = requestLine.split(' ')[0]
        URL = requestLine.split(' ')[1][1:]
        version = requestLine.split(' ')[2]        #HTTP version
        
        for header_line in header.split('\r\n')[1:]:
            line_list = header_line.split(': ')

            self.header_fields[line_list[0]] = line_list[1]

        if method == 'GET':
            self.processGET(URL)
        if method == 'POST':
            self.processPOST(URL)
        self.selector.modify(self.socket, selectors.EVENT_WRITE, data=self)


    def processGET(self, filename):
        f = open(filename, "r")
        print(f.read())
        # Generate response message


    def processPOST(self, filename):
        print(filename)
        new_file = open(filename, 'w')
        print(self.body)
        new_file.write(self.body)
        new_file.close()
        print('done')
    
