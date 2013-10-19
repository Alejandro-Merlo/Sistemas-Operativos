'''
Created on 19/10/2013

@author: Alejandro
'''
from program import Program
from threading import Thread
from threading import Semaphore
import time

class Process(Thread):
    
    def __init__(self, program, pid, pc, priority):
        Thread.__init__(self)
        self.program        = program # Programa cargado en memoria por el kernel
        self.pid            = pid # ID del proceso
        self.state          = "Ready" # Estado del proceso (Ready, CPU, Ready I/O, I/O, Timeout, Finished)
        self.pc             = pc # Contador de programa en memoria
        self.quantum        = 0 # Se lo asigna el scheduler
        self.priority       = priority
        self.main_semaphore = None # Se lo asigna el kelner
        self.semaphore      = Semaphore(0)
        self.next           = None # Siguiente proceso en la lista de prioridades
        self.previous       = None # Anterior proceso en la lista de prioridades
        

    def run(self):
        self.state = 'Running'
        print self.program.name + ' de prioridad ' + str(self.priority) + ' inicia su ejecucion'
        for instruction in self.program.instructions:
            if self.quantum is not 0:
                self.run_next_instruction(instruction)
            else:
                self.perform_quantum_terminated()
                self.run_next_instruction(instruction)
                
        self.state = 'Terminated'
        print self.program.name + ' ha terminado su ejecucion'
        self.main_semaphore.release()

    def run_next_instruction(self, instruction):
        print self.program.name + ' ejecutando ' + instruction
        self.quantum = self.quantum - 1
        time.sleep(1)

    def perform_quantum_terminated(self):
        print self.program.name + ': quantum terminado, cede la CPU'
        self.state = 'Ready'
        self.main_semaphore.release()
        self.semaphore.acquire()
        print self.program.name + ' continua con su ejecucion'
        time.sleep(1)