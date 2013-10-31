'''
Created on 21/10/2013

@author: Alejandro
'''
from threading import Thread
from time import sleep

class CPU(Thread):
    
    def __init__(self, kernel, memory, semaphore = None):
        Thread.__init__(self)
        self.assigned_pcb       = None
        self.kernel             = kernel
        self.kernel_waiting_cpu = semaphore
        self.memory             = memory
        
    def set_pcb(self, pcb):
        self.assigned_pcb = pcb
            
    def run(self):
        while True:
            if self.assigned_pcb is not None:
                self.process_pcb()
            sleep(3)

    def process_pcb(self):
        next_instruction = self.memory.fetch(self.assigned_pcb)
        if next_instruction.is_cpu():
            # Chequeo para FIFO
            if self.assigned_pcb.quantum is None:
                self.execute_instruction(next_instruction)
            # Chequeo para Round Robin
            elif self.assigned_pcb.quantum == 0:
                print self.assigned_pcb.program.name + ' ha terminado su quantum, cede la CPU'
                self.kernel.cpu_ready_signal(self.assigned_pcb)
                self.assigned_pcb = None
            else:
                self.assigned_pcb.quantum -= 1
                self.execute_instruction(next_instruction)
        else:
            self.kernel.io_signal(self.assigned_pcb, next_instruction)
            self.assigned_pcb = None

    def execute_instruction(self, next_instruction):
        print self.assigned_pcb.program.name + ' de prioridad ' + str(self.assigned_pcb.priority) + ' ejecutando en CPU'
        next_instruction.execute()
        if self.is_the_last(next_instruction):
            print self.assigned_pcb.program.name + ' ha terminado su ejecucion'
            self.kernel.cpu_kill_signal(self.assigned_pcb)
            self.assigned_pcb = None
            
    # Buscar una mejor manera de hacer esto
    def is_the_last(self, instruction):
        # Temporal
        return self.assigned_pcb.program.instructions[len(self.assigned_pcb.program.instructions) - 1] == instruction
