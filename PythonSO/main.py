'''
Created on 14/11/2013

@author: Alejandro
'''
from system.program_loader import ProgramLoader
from system.shell import Shell
from system.kernel import Kernel
from disk.inode import INode
from memory.mmu import MMU
from memory.pagination import Pagination
from scheduler.scheduler import Scheduler
from disk.hdd import HDD
from memory.mvt import MVT
from scheduler.priority_with_round_robin import PriorityWithRoundRobin
from memory.first_fit import FirstFit
from scheduler.fifo import FIFO
from scheduler.sjf import SJF
from memory.best_fit import BestFit
from memory.worst_fit import WorstFit
from time import sleep

def main():
    memory_size = 32
    page_size   = 4
    hdd_size    = 1024
    quantum     = 3
    priorities  = 5
    aging       = 3
    
    # Variantes del kernel:
    # 
    # Planificador: First Come First Serve ; Memoria: Paginacion ; Disco: INodo
    # kernel = Kernel(Scheduler(FIFO()), MMU(Pagination(memory_size, page_size), memory_size), HDD(INode(hdd_size)))
    # 
    # Planificador: Shortest Job First ; Memoria: Paginacion ; Disco: INodo
    # kernel = Kernel(Scheduler(SJF()), MMU(Pagination(memory_size, page_size), memory_size), HDD(INode(hdd_size)))
    # 
    # Planificador: First Come First Serve ; Memoria: Asignacion continua ; Disco: INodo
    # kernel = Kernel(Scheduler(FIFO()), MMU(MVT(memory_size, FirstFit()), memory_size), HDD(INode(hdd_size)))
    # 
    # Planificador: Shortest Job First ; Memoria: Asignacion continua ; Disco: INodo
    # kernel = Kernel(Scheduler(SJF()), MMU(MVT(memory_size, FirstFit()), memory_size), HDD(INode(hdd_size)))
    # 
    # Planificador: Prioridad con Round Robin ; Memoria: Asignacion continua ; Disco: INodo
    # kernel = Kernel(Scheduler(PriorityWithRoundRobin(quantum, priorities, aging)), MMU(MVT(memory_size, BestFit()), memory_size), HDD(INode(hdd_size)))
    # 
    # Planificador: Prioridad con Round Robin ; Memoria: Paginacion ; Disco: INodo
    kernel = Kernel(Scheduler(PriorityWithRoundRobin(quantum, priorities, aging)), MMU(Pagination(memory_size, page_size), memory_size), HDD(INode(hdd_size)))
    
    loader = ProgramLoader(kernel.hdd)
    loader.save_programs()
    shell  = Shell(kernel)
    shell.start()
    
    while True:
        if kernel.cpu.assigned_pcb is None:
            kernel.run_next_process()
            sleep(1)

if __name__ == '__main__':
    main()