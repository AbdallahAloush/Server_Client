from ast import Pass
from calendar import c
from http import server
import socket
import selectors
import sys
import threading
from urllib import request
from xml.etree.ElementTree import TreeBuilder

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

def extract_message_code(server_response):
    message_code = server_response[9:12]
    return message_code

def handle_successful_GET(server_response,filename): #HTTP/1.0 200 OK\r\n\r\ndatadatadata\r\n
    temp = server_response.partition()
    received_data = temp[2]
    output_file = open(f'{filename}','w')
    output_file.write(received_data)
    output_file.close()



def main():
    operations_list = generate_operations_list("input_file.txt")
    for i in range (0,len(operations_list)):
        conn_id = i+1                                                    #assigning an id to each operation to access an individual operation for later usage
        an_operation = operations_list[conn_id]
        method, file, host, port = extract_operation_elements(an_operation)
        #Composing the request packet
        http_request = construct_http_request(method,file,host,port)
        http_request_in_bytes = convert_request_bytes(http_request)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host,port))
        client.sendall(http_request_in_bytes)
        while True:
            server_response_inBytes = client.recv(1024)
            server_response = server_response_inBytes.decode('ascii')        #keep the decoded recieved data from server in a variable for later use if needed
            print("From Server:" ,server_response)
            if method == "GET" and extract_message_code(server_response) =="404":         #HTTP/1.0 404 Not Found\r\n
                break
            elif method =="GET" and extract_message_code(server_response) == "200":      #HTTP/1.0 200 OK\r\n\r\ndatadatadata\r\n
                handle_successful_GET(server_response,file)
            else:                                              #method is POST and the client does nothing on both OK snd Forbidden responses
                if extract_message_code(server_response) == "403":
                    print("Post Request forbidden \n")
                else: 
                    print("Post Request accepted \n")
                break
            client.close()
        
    
if __name__ =="__main__":
        main()


#generate_operations_list("input_file.txt")

# post ->HTTP/1.0 200 OK\r\n nag7a 
        #HTTP/1.0 403 Forbidden\r\n

# GET ->HTTP/1.0 200 OK\r\n\r\ndatadatadata\r\n
        #HTTP/1.0 404 Not Found\r\n


