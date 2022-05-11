import selectors

class Message:
    def __init__(self, selector, server_socket, client_socket):
        self.selector = selector
        self.server_socket = server_socket
        self.client_socket = client_socket
        self.receive_buffer = b''
        self.send_buffer = b''
        self.response_created = False
        self.request_type = None        # GET or POST request

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        read_data = self.server_socket.recv()
        receive_buffer += read_data
        