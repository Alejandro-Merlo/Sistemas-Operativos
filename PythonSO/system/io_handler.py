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
        
    def add(self, pcb):
        pcb.state = 'Ready I/O'
        print pcb.program.name + ' esperando I/O'
        self.ready_io.append(pcb)
        
    def run(self):
        while True:
            if self.ready_io != []:
                pcb       = self.ready_io.pop(0)
                pcb.state = 'Running I/O'
                print pcb.program.name + ' ejecutando I/O'
                instruction = pcb.program.instructions[pcb.pc]
                instruction.execute()
                sleep(2)
                if pcb.pc == len(pcb.program.instructions) - 1:
                    print pcb.program.name + ' ha terminado su ejecucion'
                    self.kernel.io_kill_signal(pcb)
                else:
                    pcb.pc = pcb.pc + 1
                    self.kernel.io_ready_signal(pcb)
            sleep(3)