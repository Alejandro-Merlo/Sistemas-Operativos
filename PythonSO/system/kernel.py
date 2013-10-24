'''
Created on 19/10/2013

@author: Alejandro
'''
from program import Program
from instruction_io import InstructionIO
from instruction_cpu import InstructionCPU
from algorithm.fifo import FIFO
from cpu import CPU
from io_handler import IOHandler
from pcb import PCB
from scheduler import Scheduler
from time import sleep
from threading import Semaphore
import random

class Kernel():
    
    def __init__(self, algorithm, cpu_semaphore):
        self.ready_list     = []
        self.scheduler      = Scheduler(algorithm)
        self.cpu_semaphore  = cpu_semaphore
        self.cpu            = CPU(self, cpu_semaphore)
        self.io_handler     = IOHandler(self)
        self.global_id      = 0
        
        self.cpu.start()
        self.io_handler.start()
    
    def load(self, program):
        process                = PCB(program, self.global_id, random.randint(0, 9))
        self.global_id         = self.global_id + 1
        process.state          = "Ready"
        self.ready_list.append(process)
        self.scheduler.add_element(process)
        
        
    def io_signal(self, pcb):
        self.io_handler.add(pcb)
        self.cpu_semaphore.release()
        
    def kill_signal(self, pcb):
        pcb.state = 'Terminated'
        self.cpu_semaphore.release()
    
    def ready_signal(self, pcb):
        self.ready_list.append(pcb)
        self.scheduler.add_element(pcb)

    def run_next_process(self):
        process = self.scheduler.choose_next()
        while process is None:
            print 'Kernel esperando mas procesos...'
            sleep(5)
            process = self.scheduler.choose_next()
        
        self.ready_list.remove(process)
        self.cpu.set_pcb(process)
                    
#     def aging_processes(self):
#         self.scheduler.aging(self.ready_list)
#     
#     def update_processes(self):
#         self.scheduler.update(self.ready_list)
        
def main():
    kernel = Kernel(FIFO(), Semaphore())
    program1 = Program('Wine', [InstructionCPU('CPU1'), InstructionIO('IO1'), InstructionCPU('CPU2')])
    program2 = Program('Eclipse', [InstructionIO('IO1'), InstructionCPU('CPU1'), InstructionCPU('CPU2')])
    program3 = Program('Thor', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionIO('IO1')])
    kernel.load(program1)
    kernel.load(program2)
    kernel.load(program3)
    
    while True:
        kernel.cpu_semaphore.acquire()
#         kernel.update_processes()
        kernel.run_next_process()
#         kernel.aging_processes()

if __name__ == '__main__':
    main()