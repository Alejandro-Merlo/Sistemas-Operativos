'''
Created on 19/10/2013

@author: Alejandro
'''
from program import Program
from instruction_io import InstructionIO
from instruction_cpu import InstructionCPU
from scheduler.fifo import FIFO
from scheduler.prioritary_round_robin import PrioritaryRoundRobin
from cpu import CPU
from io_handler import IOHandler
from pcb import PCB
from scheduler.scheduler import Scheduler
from time import sleep
from threading import Semaphore
from memory.mmu import MMU
from memory.mvt import MVT

class Kernel():
    
    def __init__(self, scheduler_algorithm, memory_algorithm , cpu_semaphore):
        self.ready_list    = []
        self.scheduler     = Scheduler(scheduler_algorithm)
        self.cpu_semaphore = cpu_semaphore
        self.memory        = MMU(memory_algorithm)
        self.cpu           = CPU(self, self.memory, cpu_semaphore)
        self.io_handler    = IOHandler(self)
        self.global_id     = 0
        
        self.cpu.start()
        self.io_handler.start()
    
    def load(self, program):
        process        = PCB(program, self.global_id)
        self.global_id = self.global_id + 1
        process.state  = "Ready"
        self.ready_list.append(process)
        self.scheduler.add_element(process)
        self.memory.load(process)
        
    #TODO: Hacer IRQ
    def io_signal(self, pcb, io_instruction):
        self.io_handler.add(pcb, io_instruction)
        self.cpu_semaphore.release()
        
    def io_kill_signal(self, pcb):
        self.memory.unload(pcb)
        pcb.state = 'Terminated'
    
    def io_ready_signal(self, pcb):
        self.ready_list.append(pcb)
        self.scheduler.add_element(pcb)
        
    def kill_signal(self, pcb):
        self.memory.unload(pcb)
        pcb.state = 'Terminated'
        self.cpu_semaphore.release()
        
    def ready_signal(self, pcb):
        self.ready_list.append(pcb)
        self.scheduler.add_element(pcb)
        self.cpu_semaphore.release()

    def run_next_process(self):
        process = self.scheduler.choose_next()
        while process is None:
            print 'Kernel esperando procesos...'
            sleep(5)
            process = self.scheduler.choose_next()
        
        self.ready_list.remove(process)
        self.cpu.set_pcb(process)
        
def main():
    kernel = Kernel(PrioritaryRoundRobin(3, 5, 3), MVT(16) , Semaphore())
    program1 = Program('Wine', [InstructionCPU('CPU1'), InstructionIO('IO1'), InstructionCPU('CPU2')])
    program2 = Program('Eclipse', [InstructionIO('IO1'), InstructionCPU('CPU1'), InstructionCPU('CPU2')])
    program3 = Program('Thor', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionIO('IO1')])
    program4 = Program('Firefox', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionCPU('CPU3'), InstructionCPU('CPU4'), InstructionIO('IO1')])
    #program5 = Program('Chrome', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionCPU('CPU3'), InstructionCPU('CPU4'), InstructionCPU('CPU5'), InstructionIO('IO1')])
    #program6 = Program('Rythmbox', [InstructionIO('IO1'), InstructionIO('IO2'), InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionCPU('CPU3'), InstructionIO('IO3')])
    kernel.load(program1)
    kernel.load(program2)
    kernel.load(program3)
    kernel.load(program4)
    #kernel.load(program5)
    #kernel.load(program6)
    
    while True:
        kernel.cpu_semaphore.acquire()
        kernel.run_next_process()

if __name__ == '__main__':
    main()