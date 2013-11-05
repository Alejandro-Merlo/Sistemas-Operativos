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
from shell import Shell

class Kernel():
    
    def __init__(self, scheduler_algorithm, memory):
        self.incoming_list      = [] # Procesos esperando para cargarse en memoria - va en el planificador de largo plazo
        self.ready_list         = [] # Procesos listos para competir por la CPU
        self.scheduler          = Scheduler(scheduler_algorithm)
        self.kernel_waiting_cpu = Semaphore() # Sincroniza el kernel con la CPU cuando corre una instruccion
        self.memory             = memory
        self.cpu                = CPU(self, self.memory)
        self.io_handler         = IOHandler(self)
        self.irq                = IRQ() # Se encarga de manejar las interrupciones
        self.global_id          = 0
        
        self.cpu.start()
        self.io_handler.start()
    
    
    def load(self, program):
        process        = PCB(program, self.global_id)
        self.global_id = self.global_id + 1
        self._load_in_memory(process)

    def _load_in_memory(self, process):
        if self.memory.can_load(process):
            self.irq.new_signal(self, process)
        else:
            print 'Proceso' + str(process.pid) + ' esperando espacio en memoria'
            self.incoming_list.append(process)
            
    def look_for_next_to_load(self):
        for pcb in self.incoming_list:
            if self.memory.can_load(pcb):
                return pcb
        return None

    def run_next_process(self):
        process = self.scheduler.choose_next()
        while process is None:
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
    kernel = Kernel(PrioritaryRoundRobin(3, 5, 3), MMU(MVT(32, FirstFit()), 32))
    shell  = Shell(kernel)
    shell.start()
#     program1 = Program('Wine', [InstructionCPU('CPU1'), InstructionIO('IO1'), InstructionCPU('CPU2')])
#     program2 = Program('Eclipse', [InstructionIO('IO1'), InstructionCPU('CPU1'), InstructionCPU('CPU2')])
#     program3 = Program('Thor', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionIO('IO1')])
#     program4 = Program('Firefox', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionCPU('CPU3'), InstructionCPU('CPU4'), InstructionIO('IO1')])
#     program5 = Program('Chrome', [InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionCPU('CPU3'), InstructionCPU('CPU4'), InstructionCPU('CPU5'), InstructionIO('IO1')])
#     program6 = Program('Rythmbox', [InstructionIO('IO1'), InstructionIO('IO2'), InstructionCPU('CPU1'), InstructionCPU('CPU2'), InstructionCPU('CPU3'), InstructionIO('IO3')])
#     kernel.load(program1)
#     kernel.load(program2)
#     kernel.load(program3)
#     kernel.load(program4)
#     kernel.load(program5)
#     kernel.load(program6)
    
    while True:
        kernel.kernel_waiting_cpu.acquire()
        kernel.run_next_process()

if __name__ == '__main__':
    main()