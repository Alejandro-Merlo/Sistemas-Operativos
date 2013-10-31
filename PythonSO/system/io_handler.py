'''
Created on 23/10/2013

@author: Alejandro
'''
from threading import Thread
from time import sleep

class IOHandler(Thread):
    
    def __init__(self, kernel):
        Thread.__init__(self)
        self.kernel   = kernel
        self.ready_io = []
        
    def add(self, pcb, instruction):
        pcb.state = 'Ready I/O'
        print pcb.program.name + ' esperando I/O'
        self.ready_io.append((pcb, instruction))
        
    def run(self):
        while True:
            if self.ready_io != []:
                next_pair          = self.ready_io.pop(0)
                next_pair[0].state = 'Running I/O'
                print next_pair[0].program.name + ' ejecutando I/O'
                next_pair[1].execute()
                sleep(2)
                if self.is_the_last(next_pair):
                    print next_pair[0].program.name + ' ha terminado su ejecucion'
                    self.kernel.io_kill_signal(next_pair[0])
                else:
                    self.kernel.io_ready_signal(next_pair[0])
            sleep(3)
            
    def is_the_last(self, pair):
        return pair[0].program.instructions[len(pair[0].program.instructions) - 1] == pair[1]