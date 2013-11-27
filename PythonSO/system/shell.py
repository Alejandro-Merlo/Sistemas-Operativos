'''
Created on 20/10/2013

@author: Alejandro
'''
from threading import Thread
import random
from time import sleep

class Shell(Thread):
    
    def __init__(self, kernel):
        Thread.__init__(self)
        self.kernel = kernel
        
    def run(self):
        while True:
            #self.kernel.hdd.show_programs()
            #program_name = raw_input('Escriba el nombre del programa a ejecutar: ')
            program = self.kernel.hdd.programs[random.randint(0, len(self.kernel.hdd.programs) - 1)]
            program_name = program.name
            self.kernel.load(program_name)
            sleep(random.randint(2, 6))