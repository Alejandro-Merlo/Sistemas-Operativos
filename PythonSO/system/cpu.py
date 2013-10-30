'''
Created on 21/10/2013

@author: Alejandro
'''
from memory import MMU
from threading import Thread
from time import sleep

class CPU(Thread):
    
    def __init__(self, kernel, semaphore = None, algorithm):
        Thread.__init__(self)
        self.assigned_pcb = None
        self.kernel       = kernel
        self.semaphore    = semaphore
        self.memory       = MMU(algorithm)
        
    def set_pcb(self, pcb):
        self.assigned_pcb = pcb
            
    def run(self):
        while True:
            if self.assigned_pcb is not None:
                self.process_pcb()
            sleep(2)

    def process_pcb(self):
        next_instruction = self.assigned_pcb.program.instructions[self.assigned_pcb.pc]
        if next_instruction.is_cpu():
            if self.assigned_pcb.quantum is None:
                self.execute_instruction(next_instruction)
            else:
                if self.assigned_pcb.quantum == 0:
                    print self.assigned_pcb.program.name + ' ha terminado su quantum, cede la CPU'
                    self.kernel.ready_signal(self.assigned_pcb)
                    self.assigned_pcb = None
                else:
                    self.assigned_pcb.quantum -= 1
                    self.execute_instruction(next_instruction)
        else:
            self.kernel.io_signal(self.assigned_pcb)
            self.assigned_pcb = None

    def execute_instruction(self, next_instruction):
        print self.assigned_pcb.program.name + ' de prioridad ' + str(self.assigned_pcb.priority) + ' ejecutando en CPU'
        next_instruction.execute()
        if self.assigned_pcb.pc == len(self.assigned_pcb.program.instructions) - 1:
            print self.assigned_pcb.program.name + ' ha terminado su ejecucion'
            self.kernel.kill_signal(self.assigned_pcb)
            self.assigned_pcb = None
        else:
            self.assigned_pcb.pc = self.assigned_pcb.pc + 1 # En memoria
            
