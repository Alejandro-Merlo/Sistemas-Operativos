'''
Created on 21/10/2013

@author: Alejandro
'''
from threading import Thread
from time import sleep

class CPU(Thread):
    
    def __init__(self, kernel, semaphore = None):
        Thread.__init__(self)
        self.pcb       = None
        self.kernel    = kernel
        self.semaphore = semaphore
        
    def set_pcb(self, pcb):
        self.pcb = pcb

    def process_pcb(self):
        next_instruction = self.pcb.program.instructions[self.pcb.pc]
        if next_instruction.is_cpu():
            print self.pcb.program.name + ' ejecutando en CPU'
            next_instruction.execute()
            if self.pcb.pc == len(self.pcb.program.instructions) - 1:
                print self.pcb.program.name + ' ha terminado su ejecucion'
                self.kernel.kill_signal(self.pcb)
                self.pcb = None
            else:
                self.pcb.pc = self.pcb.pc + 1 # En memoria
        else:
            self.kernel.io_signal(self.pcb)
            self.pcb = None
            
            
    def run(self):
        while True:
            if self.pcb is not None:
                self.process_pcb()
            sleep(2)