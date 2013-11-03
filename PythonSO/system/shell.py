'''
Created on 20/10/2013

@author: Alejandro
'''
from threading import Thread
from program import Program
from instruction_cpu import InstructionCPU
from instruction_io import InstructionIO
import random
from time import sleep

class Shell(Thread):
    
    def __init__(self, kernel):
        Thread.__init__(self)
        self.kernel = kernel
        
    def run(self):
        number = 1
        while True:
        #for e in range(1, 20):
            instructions = []
            
            for i in range(1, random.randint(2, 8)):
                instructions.append(InstructionCPU('CPU' + str(i)))
                
            for i in range(1, random.randint(2, 3)):
                instructions.append(InstructionIO('IO' + str(i)))
                
            new_program = Program("Program" + str(number), instructions)
            self.kernel.load(new_program)
            number += 1
            sleep(random.randint(5, 10))