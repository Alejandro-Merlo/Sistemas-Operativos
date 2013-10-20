'''
Created on 19/10/2013

@author: Alejandro
'''
from program import Program
from process import Process
from scheduler import Scheduler
from algorithm.prioritary_round_robin import PrioritaryRoundRobin
from threading import Semaphore
import time
import random

class Kernel():
    
    def __init__(self):
        self.ready_list      = []
        self.ready_io        = []
        self.scheduler       = Scheduler(PrioritaryRoundRobin(3))
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
        
        self.ready_list.append(process)
        self.scheduler.add_element(process)

    def check_last_running(self):
        if self.process_running is not None:
            process = self.process_running
            if process.state is 'Ready':
                self.ready_list.append(process)
                self.scheduler.add_element(process)
            if process.state is 'Ready I/O':
                self.ready_io.append(process)

    def run_next_process(self):        
        self.check_last_running()
        process = self.scheduler.choose_next()
        
        while process is None:
            print 'Esperando mas procesos...'
            time.sleep(10)
            process = self.scheduler.choose_next()
            
        self.ready_list.remove(process)
        self.process_running = process
        
        if process.isAlive():
            process.semaphore.release()
        else:
            process.start()
        
def main():
    program1 = Program("Program1", ['instruction1', 'instruction2', 'instruction3', 'instruction4'])
    program2 = Program("Program2", ['instruction1', 'instruction2', 'instruction3'])
    program3 = Program("Program3", ['instruction1', 'instruction2'])
    program4 = Program("Program4", ['instruction1', 'instruction2', 'instruction3', 'instruction4', 'instruction5', 'instruction6', 'instruction7', 'instruction8'])
    program5 = Program("Program5", ['instruction1', 'instruction2', 'instruction3', 'instruction4', 'instruction5', 'instruction6'])
    program6 = Program("Program6", ['instruction1', 'instruction2', 'instruction3', 'instruction4'])
    program7 = Program("Program7", ['instruction1', 'instruction2', 'instruction3', 'instruction4', 'instruction5', 'instruction6', 'instruction7', 'instruction8', 'instruction9', 'instruction10'])
    
    kernel = Kernel()
    kernel.load_program(program1)
    kernel.load_program(program2)
    kernel.load_program(program3)
    kernel.load_program(program4)
    kernel.load_program(program5)
    kernel.load_program(program6)
    kernel.load_program(program7)
    
    while True:
        kernel.main_semaphore.acquire()            
        kernel.run_next_process()
        time.sleep(5)

if __name__ == '__main__':
    main()