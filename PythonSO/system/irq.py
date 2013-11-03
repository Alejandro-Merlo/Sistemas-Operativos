'''
Created on 31/10/2013

@author: Alejandro
'''
from threading import Semaphore

class IRQ():
    
    def __init__(self):
        self.kernel_mode = Semaphore()
        
    def new_signal(self, kernel, process):
        self.kernel_mode.acquire()
        process.state = "Ready"
        kernel.ready_list.append(process)
        kernel.memory.load(process)
        kernel.scheduler.add_element(process)
        self.kernel_mode.release()
    
    def io_signal(self, kernel, pcb, io_instruction):
        self.kernel_mode.acquire()
        kernel.io_handler.add(pcb, io_instruction)
        self.kernel_mode.release()
        kernel.kernel_waiting_cpu.release()
        
    def io_kill_signal(self, kernel, pcb):
        self.kernel_mode.acquire()
        print pcb.program.name + ' ha terminado su ejecucion'
        kernel.memory.unload(pcb)
        pcb.state = 'Terminated'
        self.kernel_mode.release()
        
    def io_ready_signal(self, kernel, pcb):
        self.kernel_mode.acquire()
        kernel.ready_list.append(pcb)
        kernel.scheduler.add_element(pcb)
        self.kernel_mode.release()
        
    def cpu_kill_signal(self, kernel, pcb):
        self.kernel_mode.acquire()
        print pcb.program.name + ' ha terminado su ejecucion'
        kernel.memory.unload(pcb)
        pcb.state = 'Terminated'
        kernel.kernel_waiting_cpu.release()
        self.kernel_mode.release()
        
    def cpu_ready_signal(self, kernel, pcb):
        self.kernel_mode.acquire()
        print pcb.program.name + ' ha terminado su quantum, cede la CPU'
        kernel.ready_list.append(pcb)
        kernel.scheduler.add_element(pcb)
        self.kernel_mode.release()
        kernel.kernel_waiting_cpu.release()