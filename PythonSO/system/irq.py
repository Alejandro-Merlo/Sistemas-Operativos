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
        kernel.long_term_scheduler.load_process(kernel, process)
        self.kernel_mode.release()
    
    def io_signal(self, kernel, pcb, io_instruction):
        self.kernel_mode.acquire()
        kernel.io_handler.add(pcb, io_instruction)
        self.kernel_mode.release()
        
    def kill_signal(self, kernel, pcb):
        self.kernel_mode.acquire()
        kernel.long_term_scheduler.kill(kernel, pcb)
        self.kernel_mode.release()
        
    def suspend_signal(self, kernel, pcb):
        self.kernel_mode.acquire()
        print 'Proceso' + str(pcb.pid) + ' vuelve a la cola de listos'
        kernel.scheduler.add_element(pcb)
        self.kernel_mode.release()