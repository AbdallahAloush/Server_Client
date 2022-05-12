from calendar import c
import socket
import selectors
import sys
from urllib import request

#This function generates the operations list from the input file
def generate_operations_list(filename):
    operations =[]
    with open(f'{filename}','rt') as inputFile:
        for anOperation in inputFile:
            operations.append(anOperation)
    for anOperation in operations:
            print(anOperation, end='')  
    return operations


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
    http_request = method+whitespace+file+whitespace+"HTTP/1.0\r\nHost:"+host+':'+port+"\r\n\r\n"
    return http_request
    
#construct_http_request("POST test.txt 127.0.0.1")

#_______________________________________________________________________________________________________________
def main():
    
    """ operations_list = generate_operations_list("input_file.txt")
    for an_operation in operations_list:
        http
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a TCP connection
        server_address = (f'{an_operation_exists.}') """




    




    
if __name__ =="__main__":
    main()
   

#generate_operations_list("input_file.txt")