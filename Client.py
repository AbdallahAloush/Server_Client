from calendar import c
import socket
import selectors
import sys
from urllib import request

def generate_operations_list(filename):
    operations =[]
    with open(f'{filename}','rt') as inputFile:
        for anOperation in inputFile:
            operations.append(anOperation)
    for anOperation in operations:
            print(anOperation, end='')  
    return operations
    
def construct_http_request(operation):
    whitespace =' '
    operations_elements = operation.split(' ')
    request_method = operations_elements[0]
    requested_file_name = operations_elements[1]
    host_name = operations_elements[2]
    if len(operations_elements) == 4:
        port_number = operations_elements[3]
    else:
        port_number = "80"
    #print(operations_elements)
    http_request = request_method+whitespace+requested_file_name +whitespace+"HTTP/1.0\r\nHost:"+host_name+':'+port_number+"\r\n\r\n"
    print(http_request)

construct_http_request("POST test.txt 127.0.0.1")

 
    




    

   

#generate_operations_list("input_file.txt")