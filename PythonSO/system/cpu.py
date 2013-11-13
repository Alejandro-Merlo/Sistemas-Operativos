'''
Created on 21/10/2013

@author: Alejandro
'''
from threading import Thread
from time import sleep

class CPU(Thread):
    
    def __init__(self, kernel, memory):
        Thread.__init__(self)
        self.assigned_pcb = None
        self.kernel       = kernel
        self.memory       = memory
            
    def run(self):
        while True:
            if self.assigned_pcb is not None:
                self.process_pcb()
            sleep(2)

    def process_pcb(self):
        next_instruction = self.memory.fetch(self.assigned_pcb)
        if next_instruction.is_cpu():
            # Chequeo para FIFO
            if self.assigned_pcb.quantum is None:
                self.execute_instruction(next_instruction)
            # Chequeo para Round Robin
            elif self.assigned_pcb.quantum == 0:
                self.kernel.suspend_signal(self.assigned_pcb)
                self.assigned_pcb = None
            else:
                self.assigned_pcb.quantum -= 1
                self.execute_instruction(next_instruction)
        else:
            
            self.kernel.io_signal(self.assigned_pcb, (self._is_the_last(next_instruction), next_instruction))
            self.assigned_pcb = None

    def execute_instruction(self, next_instruction):
        print 'Proceso' + str(self.assigned_pcb.pid) + ' de prioridad ' + str(self.assigned_pcb.priority) + ' ejecutando en CPU'
        next_instruction.execute()
        if self._is_the_last(next_instruction):
            self.kernel.kill_signal(self.assigned_pcb)
            self.assigned_pcb = None

    def _is_the_last(self, instruction):
        return self.assigned_pcb.program.instructions[-1] == instruction