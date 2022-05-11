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
    operations_elements = operation.split(' ')
    request_method = operations_elements[0]
    file_name = operations_elements[1]
    host_name = operations_elements[2]
    if len(operations_elements) == 4:
        port_number = operations_elements[3]
    else:
        port_number = "80"
    #print(operations_elements)


construct_http_request("GET /hypertext/WWW/TheProject.html info.cern.ch 80")

 
    




    

   

#generate_operations_list("input_file.txt")