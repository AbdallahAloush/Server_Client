from ast import Pass
from calendar import c
import socket
import selectors
import sys
import HttpRequestClient
from urllib import request

#This function generates the operations list from the input file
def generate_operations_list(filename):
    operations =[]
    with open(f'{filename}','rt') as inputFile:
        for anOperation in inputFile:
            operations.append(anOperation)
    for anOperation in operations:
            print(anOperation, end='')  
    return operations #returns lsit of operations


#This functions extracts the main elements of http request from operation
def extract_operation_elements(operation):
    operations_elements = operation.split(' ')
    request_method = operations_elements[0]
    requested_file_name = operations_elements[1]
    host_name = operations_elements[2]
    if len(operations_elements) == 4:
        port_number = operations_elements[3]
    else:
        port_number = "80"
    #print(operations_elements)
    return request_method, requested_file_name, host_name, port_number

#This function constructs the http request in the right format
def construct_http_request(method,file,host,port):
    whitespace =' '
    if method == "GET":
        http_request = method+whitespace+file+whitespace+"HTTP/1.0\r\nHost:"+host+':'+port+"\r\n\r\n"
    else:   #method = "POST"
        fileCotents = open(f'{file}','r')
        http_request = method+whitespace+file+whitespace+"HTTP/1.0\r\nHost:"+host+':'+port+"\r\n\r\n"+fileCotents+"\r\n"
    return http_request
    
def convert_request_bytes(http_request):
    http_request_inBytes = http_request.encode('ascii')
    return http_request_inBytes


def main():
    sel = selectors.DefaultSelector()
    operations_list = generate_operations_list("input_file.txt")
    for i in range (0,len(operations_list)):
        conn_id = i+1                                                    #assigning an id to each connection
        an_operation = operations_list[conn_id]
        method, file, host, port = extract_operation_elements(an_operation)
        server_address = (host,port)
        print(f"Starting connection {conn_id} to {server_address}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #creating a TCP connection
        sock.setblocking(False)
        sock.connect_ex(server_address)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = HttpRequestClient.Message(sel,sock,address,request)
        sel.register(sock,events, data=message)

        #Composing the request packet
        http_request = construct_http_request(method,file,host,port)
        http_request_in_bytes = convert_request_bytes(http_request)
        try:
            while True:
                events = sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except KeyboardInterrupt:
                        sys.exit()
        finally:
            sel.close()                   


    
if __name__ =="__main__":
    main()
   

#generate_operations_list("input_file.txt")