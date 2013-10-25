'''
Created on 19/10/2013

@author: Alejandro
'''
class PCB():
    
    def __init__(self, program, pid):
        self.program  = program # Programa cargado en memoria por el kernel
        self.pid      = pid # ID del proceso
        self.state    = "New" # Estado del proceso (Ready, CPU, Ready I/O, I/O, Timeout, Finished)
        self.pc       = 0
        self.quantum  = None # Se lo asigna el scheduler en caso de ser Round Robin
        #self.priority = priority