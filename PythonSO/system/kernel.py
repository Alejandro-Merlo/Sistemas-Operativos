'''
Created on 19/10/2013

@author: Alejandro
'''
from cpu import CPU
from io_handler import IOHandler
from scheduler.scheduler import Scheduler
from long_term_scheduler import LongTermScheduler
from shell import Shell
from time import sleep
from memory.mmu import MMU
from memory.mvt import MVT
from irq import IRQ
from scheduler.prioritary_round_robin import PrioritaryRoundRobin
from memory.first_fit import FirstFit
#from scheduler.fifo import FIFO
#from memory.best_fit import BestFit
#from memory.worst_fit import WorstFit

class Kernel():
    
    def __init__(self, scheduler_algorithm, memory):
        self.ready_list          = [] # Procesos listos para competir por la CPU
        self.scheduler           = Scheduler(scheduler_algorithm)
        self.long_term_scheduler = LongTermScheduler(memory)
        self.cpu                 = CPU(self, memory)
        self.io_handler          = IOHandler(self)
        self.irq                 = IRQ() # Se encarga de manejar las interrupciones
        
        self.cpu.start()
        self.io_handler.start()
    
    
    def load(self, program):
        self.long_term_scheduler.create(program, self)

    def run_next_process(self):
        process = self.scheduler.choose_next()
        while process is None:
            sleep(5)
            process = self.scheduler.choose_next()
        
        self.ready_list.remove(process)
        self.cpu.assigned_pcb = process        
        
    
    ###################
    # INTERRUPCIONES
    ###################
    def io_signal(self, pcb, io_instruction):
        self.irq.io_signal(self, pcb, io_instruction)
    
    def suspend_signal(self, pcb):
        self.irq.suspend_signal(self, pcb)
        
    def kill_signal(self, pcb):
        self.irq.kill_signal(self, pcb)
        
        
        
def main():
    kernel = Kernel(PrioritaryRoundRobin(3, 5, 3), MMU(MVT(32, FirstFit()), 32))
    shell  = Shell(kernel)
    shell.start()
    
    while True:
        if kernel.cpu.assigned_pcb is None:
            kernel.run_next_process()
            sleep(1)

if __name__ == '__main__':
    main()