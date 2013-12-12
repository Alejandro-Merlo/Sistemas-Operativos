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
        #self.kernel.hdd.show_programs()
        while True:
            try:
                #program_name = raw_input('Escriba el nombre del programa a ejecutar: ')
                program_name = 'Programa' + str(random.randint(0, self.kernel.hdd.programs_saved() - 1))
                self.kernel.load(program_name)
                sleep(random.randint(2, 6))
            except:
                print 'Nombre de programa invalido'