'''
Created on 20/10/2013

@author: Alejandro
'''
from threading import Thread
from program import Program
import random
from time import sleep

class Shell(Thread):
    
    def __init__(self, kernel):
        Thread.__init__(self)
        self.kernel = kernel
        
    def run(self):
        #number = 1
        #while True:
        for e in range(1, 20):
            instructions = []
            
            for i in range(1, random.randint(3, 10)):
                instructions.append('instruction' + str(i))
                
            new_program = Program("Program" + str(e), instructions)
            self.kernel.load_program(new_program)
            #number = number + 1
            sleep(random.randint(3, 10))