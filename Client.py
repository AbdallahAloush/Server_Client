from ast import Pass
from calendar import c
from http import server
import socket
import selectors
import sys
import os
import threading
from urllib import request
from xml.etree.ElementTree import TreeBuilder


#This function generates the operations list from the input file
def generate_operations_list(filename):
    operations =[]
    with open(f'{filename}','rt') as inputFile:
        for anOperation in inputFile:
            operations.append(anOperation)
    return operations                                       #returns list of operations


#This functions extracts the main elements of http request from operation
def extract_operation_elements(operation):
    operations_elements = operation.split(' ')
    request_method = operations_elements[0]
    requested_file_name = operations_elements[1]
    if len(operations_elements)== 4:
        host_name = operations_elements[2]
        port_number = int(operations_elements[3][:-1])
    elif len(operations_elements)==3:
        host_name = operations_elements[2][:-1]
        port_number = 80
    return request_method, requested_file_name, host_name, port_number


#This function constructs the http request in the right format
def construct_http_request(method,fileName,host,port):
    if method == "GET":
        http_request = f'{method} {fileName} HTTP/1.0\r\nHost:{host}:{port}\r\n\r\n' 
    else:   #method = "POST"
        with open(f'{fileName}','r') as file_object:
            fileCotents = file_object.read()
        http_request = f'{method} /{fileName} HTTP/1.0\r\nHost:{host}:{port}\r\n\r\n{fileCotents}\r\n'
    return http_request
    
def convert_request_bytes(http_request):
    http_request_inBytes = http_request.encode('ascii')
    return http_request_inBytes

def extract_message_code(server_response):
    message_code = server_response[9:12]
    return message_code

def handle_successful_GET(server_response,filename): #HTTP/1.0 200 OK\r\n\r\ndatadatadata\r\n
    temp = server_response.partition('\r\n\r\n')
    received_data = temp[2]
    cache_path = 'Cached'
    cached_file_name = cache_path+filename
    #File object to write the file contents in the cache
    output_file_cache = open(cached_file_name, "w")
    output_file_cache.write(received_data)
    output_file_cache.close()
    #File object to write the file contents in the normal directory
    output_file = open(filename,'w')
    output_file.write(received_data)
    output_file.close()

def handle_successful_cache_hit(cached_file_path,original_file_name):  #Cached\Mazen.txt
    cached_file_read = open(cached_file_path, "r")
    cached_file_contents = cached_file_read.read()
    #!print("_____________________________________\n"+cached_file_contents+"________________________________________\n")
    cached_file_write = open(original_file_name,'w')
    cached_file_write.write(cached_file_contents)
    cached_file_read.close()
    cached_file_write.close()

def isCached(requests_list,http_request):
    if http_request in requests_list:
        return 1
    else:
        return 0

def main():
    operations_list = generate_operations_list("input_file.txt")
    cached_requests_list = []
    for i in range (0,len(operations_list)):
        conn_id = i                                                    #assigning an id to each operation
        an_operation = operations_list[conn_id]
        method, fileName, host, port = extract_operation_elements(an_operation)
        #Composing the request packet
        http_request = construct_http_request(method,fileName,host,port)
        print("Http Request--->"+http_request+'\n')
        if isCached(cached_requests_list,http_request) ==1:             #Check if  http request is cached(no need to connect to server)
            print("Cache hit successful!\n")
            handle_successful_cache_hit(f'Cached{fileName}',fileName)
        else:                                                           #Request is not cached, proceed to connect to server
            if method =="GET":
                print("Cache hit not successful , connecting to server!\n")  
            http_request_in_bytes = convert_request_bytes(http_request)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host,port))
            client.sendall(http_request_in_bytes)
            while True:                        #event loop waiting for the server's response
                server_response_inBytes = client.recv(1024)
                server_response = server_response_inBytes.decode('ascii')      #keep the decoded recieved data from server in a variable for later use if needed
                print("Server Response:\n" ,server_response)
                if method == "GET" and extract_message_code(server_response) =="404":         
                    break
                elif method =="GET" and extract_message_code(server_response) == "200":      
                    handle_successful_GET(server_response,fileName)
                    cached_requests_list.append(http_request)                   #A list to keep track of cached requests that have been fullfilled before
                    break
                else:                               #method is POST and the client does nothing on both OK snd Forbidden responses
                    if extract_message_code(server_response) == "403":
                        print("Status of Post Request------> Forbidden \n")
                    else: 
                        print("Status of Post Request ------> accepted \n")
                    break
            print("______________________________________________________________________________________________________________________")
            client.close()
        
    
if __name__ =="__main__":
        main()





