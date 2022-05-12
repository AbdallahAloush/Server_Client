recv_buffer_size = 10000

class Request:
    def __init__(self, decoded_message):
        #
        header, garbage, body = decoded_message.partition('\r\n\r\n')
        request_line_temp = header.split('\r\n')[0]
        request_line_attributes = request_line_temp.split(' ') 
        self.request_line = {
            'method': request_line_attributes[0],
            'url': request_line_attributes[1][1:],
            'version': request_line_attributes[2]     
        }
        if body is not None:
            self.body = body         # total size of the request in bytes
        else:
            self.body = ''
    def processRequest(self):  
        method = self.request_line['method']
        filepath = self.request_line['url']
        if method == 'GET':
            self.GET(filepath)
        if method == 'POST':
            self.POST(filepath)

    def GET(self, filename):
        try:
            retrived_file = open(filename, "r")
            self.body = retrived_file.read()
            # create ok message
            response = self.createResponse(200, 'OK')
        except:
            self.body = ''
            response = self.createResponse(404, 'Not Found')
        return response

    def POST(self, filename):
        try:
            new_file = open(filename, 'w')
            print(self.body)
            new_file.write(self.body)
            new_file.close()
            print('done')
            response = self.createResponse(200, 'OK')
        except:
            response = self.createResponse(403, 'Forbidden')
            
        return response
    
    def createResponse (self, response_code, response_message):
        version = self.request_line['version']
        print(version)
        status_line = f'{version} {response_code} {response_message}\r\n'
        print(status_line)
        if self.body is not None:
            data = f'\r\n{self.body}\r\n'
            response = f'{status_line} + {data}'
        else:
            response = f'{status_line}'
        print(self.body)
        return response