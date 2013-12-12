'''
Created on 19/10/2013

@author: Alejandro
'''
from cpu import CPU
from io_handler import IOHandler
from long_term_scheduler import LongTermScheduler
from time import sleep
from irq import IRQ

class Kernel():
    
    def __init__(self, dispatcher = None, memory = None, hdd = None):
        self.scheduler           = dispatcher
        self.long_term_scheduler = LongTermScheduler(memory)
        self.hdd                 = hdd
        self.cpu                 = CPU(self, memory)
        self.io_handler          = IOHandler(self)
        self.irq                 = IRQ()
        
        self.cpu.start()
        self.io_handler.start()
    
        
    def load(self, program):
        self.long_term_scheduler.create(program, self)

    def run_next_process(self):
        process = self.scheduler.choose_next()
        while process is None:
            sleep(3)
            process = self.scheduler.choose_next()
        
        self.cpu.assigned_pcb = process        
        
    
    ###################
    # INTERRUPCIONES
    ###################
    def new_signal(self, process):
        self.irq.new_signal(self, process)

    def io_signal(self, pcb, io_instruction):
        self.irq.io_signal(self, pcb, io_instruction)
    
    def suspend_signal(self, pcb):
        self.irq.suspend_signal(self, pcb)
        
    def kill_signal(self, pcb):
        self.irq.kill_signal(self, pcb)