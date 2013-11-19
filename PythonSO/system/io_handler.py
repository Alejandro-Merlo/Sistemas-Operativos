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
        print 'Proceso' + str(pcb.pid) + ' esperando I/O'
        self.ready_io.append((pcb, instruction))
        
    def run(self):
        while True:
            if self.ready_io != []:
                next_pair          = self.ready_io.pop(0)
                next_pair[0].state = 'Running I/O'
                print 'IO: ' + next_pair[1][1].value
                sleep(2)
                if next_pair[1][0]:
                    self.kernel.kill_signal(next_pair[0])
                else:
                    self.kernel.suspend_signal(next_pair[0])
            sleep(2)