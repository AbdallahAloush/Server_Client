recv_buffer_size = 10000

class Request:
    def __init__(self, decoded_message):
        self.header, self.garbage, self.body = decoded_message.partition('\r\n\r\n')
        self.request_line_temp = self.header.split('\r\n')[0]
        self.request_line_attributes = self.request_line_temp.split(' ') 
        self.request_line = {
            'method': self.request_line_attributes[0],
            'url': self.request_line_attributes[1],
            'version': self.request_line_attributes[2]     
        }
        if len(self.body) == 0:
            self.body = ''    
            
    def processRequest(self):  
        method = self.request_line['method']        # GET or POST
        filepath = self.request_line['url']      
        filepath = filepath[1:]
        if method == 'GET':
            response = self.GET(filepath)
        if method == 'POST':
            response = self.POST(filepath)
        return response

    def GET(self, filename):
        try:
            retrived_file = open(filename, "r")
            self.body = retrived_file.read()
            retrived_file.close()
            response = self.createResponse(200, 'OK')
        except:
            self.body = ''
            response = self.createResponse(404, 'Not Found')
        return response

    def POST(self, filename):
        try:
            new_file = open(filename, 'w')
            new_file.write(self.body)
            new_file.close()
            self.body = ''
            print('Wrote file Successfully\n')
            response = self.createResponse(200, 'OK')
        except:
            response = self.createResponse(403, 'Forbidden')
        return response
    
    def createResponse (self, response_code, response_message):
        version = self.request_line['version']              
        status_line = f'{version} {response_code} {response_message}\r\n'
        if self.body == '':         # No file is being sent
            response = f'{status_line}\r\n'
        else:                       # Sending a file
            data = f'{self.body}'
            response = f'{status_line}\r\n{data}\r\n'
        return response