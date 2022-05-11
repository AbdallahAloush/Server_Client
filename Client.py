from calendar import c
import socket
import selectors
import sys

def generate_operations_list(filename):
    operations =[]
    with open(f'{filename}','rt') as inputFile:
        for anOperation in inputFile:
            operations.append(anOperation)
    for anOperation in operations:
            print(anOperation, end='')  
    return operations

def  
   

#generate_operations_list("input_file.txt")