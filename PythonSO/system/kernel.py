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
from irq import IRQ
from memory.first_fit import FirstFit
from memory.best_fit import BestFit
from memory.worst_fit import WorstFit

class Kernel():
    
    def __init__(self, scheduler_algorithm, memory_algorithm):
        self.ready_list         = []
        self.scheduler          = Scheduler(scheduler_algorithm)
        self.kernel_waiting_cpu = Semaphore()
        self.memory             = MMU(memory_algorithm)
        self.cpu                = CPU(self, self.memory)
        self.io_handler         = IOHandler(self)
        self.irq                = IRQ()
        self.global_id          = 0
        
        self.cpu.start()
        self.io_handler.start()
    
    def load(self, program):
        # Agregar mecanismo que detenga los otros threads?
        process        = PCB(program, self.global_id)
        self.global_id = self.global_id + 1
        if self.memory.can_load(process):
            process.state  = "Ready"
            self.ready_list.append(process)
            self.memory.load(process)
            self.scheduler.add_element(process)
        else:
            print process.program.name + ' no entra en la memoria'

    def run_next_process(self):
        process = self.scheduler.choose_next()
        while process is None:
            print 'Kernel esperando procesos...'
            sleep(5)
            process = self.scheduler.choose_next()
        
        self.ready_list.remove(process)
        self.cpu.set_pcb(process)
        
    def io_signal(self, pcb, io_instruction):
        self.irq.io_signal(self, pcb, io_instruction)
        
    def io_kill_signal(self, pcb):
        self.irq.io_kill_signal(self, pcb)
    
    def io_ready_signal(self, pcb):
        self.irq.io_ready_signal(self, pcb)
        
    def cpu_kill_signal(self, pcb):
        self.irq.cpu_kill_signal(self, pcb)
        
    def cpu_ready_signal(self, pcb):
        self.irq.cpu_ready_signal(self, pcb)
        
def main():
    kernel = Kernel(PrioritaryRoundRobin(3, 5, 3), MVT(16, FirstFit()))
    program1 = Program('Wine', [InstructionCPU('CPU1'), InstructionIO('IO1'), InstructionCPU('CPU2')])
    program2 = Program('Eclipse', [InstructionIO('IO1'), InstructionCPU('CPU1'), InstructionCPU('CPU2')])
    program3 = Program('Thor', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionIO('IO1')])
    program4 = Program('Firefox', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionCPU('CPU3'), InstructionCPU('CPU4'), InstructionIO('IO1')])
    program5 = Program('Chrome', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionCPU('CPU3'), InstructionCPU('CPU4'), InstructionCPU('CPU5'), InstructionIO('IO1')])
    program6 = Program('Rythmbox', [InstructionIO('IO1'), InstructionIO('IO2'), InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionCPU('CPU3'), InstructionIO('IO3')])
    kernel.load(program1)
    kernel.load(program2)
    kernel.load(program3)
    kernel.load(program4)
    kernel.load(program5)
    kernel.load(program6)
    
    while True:
        kernel.kernel_waiting_cpu.acquire()
        kernel.run_next_process()

if __name__ == '__main__':
    main()