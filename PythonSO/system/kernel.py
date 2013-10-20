'''
Created on 19/10/2013

@author: Alejandro
'''
from program import Program
from process import Process
from shell import Shell
from scheduler import Scheduler
from algorithm.prioritary_round_robin import PrioritaryRoundRobin
from threading import Semaphore
from time import sleep
import random

class Kernel():
    
    def __init__(self):
        self.ready_list      = []
        self.ready_io        = []
        self.scheduler       = Scheduler(PrioritaryRoundRobin(3, 5))
        self.process_running = None
        self.main_semaphore  = Semaphore()
        
        self.global_id = 0
        self.global_pc = 0
    
    def load_program(self, program):
        process                = Process(program, self.global_id, self.global_pc, random.randint(0, 9))
        self.global_id         = self.global_id + 1
        self.global_pc         = self.global_pc + process.program.instructions.__len__()
        process.state          = "Ready"
        process.main_semaphore = self.main_semaphore
        
        self.scheduler.add_element(process, self.ready_io)

    def check_last_running(self):
        if self.process_running is not None:
            process = self.process_running
            if process.state is 'Ready':
                self.scheduler.add_element(process, self.ready_io)
            if process.state is 'Ready I/O':
                self.ready_io.append(process)

    def run_next_process(self):        
        self.check_last_running()
        process = self.scheduler.choose_next(self.ready_io)
        
        while process is None:
            print 'Esperando mas procesos...'
            sleep(10)
            process = self.scheduler.choose_next(self.ready_io)
            
        self.process_running = process
        
        if process.isAlive():
            process.semaphore.release()
        else:
            process.start()
            
    def aging_processes(self):
        self.scheduler.aging(self.ready_io)
    
    def update_processes(self):
        self.scheduler.update(self.ready_io)
        
def main():
    kernel = Kernel()
    shell = Shell(kernel)
    shell.start()
    
    while True:
        kernel.update_processes()
        kernel.main_semaphore.acquire()            
        kernel.run_next_process()
        kernel.aging_processes()
        sleep(5)

if __name__ == '__main__':
    main()