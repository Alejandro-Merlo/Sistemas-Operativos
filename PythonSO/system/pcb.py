'''
Created on 19/10/2013

@author: Alejandro
'''
class PCB():
    
    def __init__(self, program, pid):
        self.program        = program # Programa cargado en memoria por el kernel
        self.pid            = pid # ID del proceso
        self.state          = "New" # Estado del proceso (Ready, CPU, Ready I/O, I/O, Timeout, Finished)
        self.base_direction = None # Se asigna cuando se carga a memoria
        self.quantum        = None # Se lo asigna el scheduler en caso de ser Round Robin
        self.priority       = None # Se lo asigna el scheduler en caso de ser por prioridad
        
    def set_priority(self, priority):
        self.priority = priority
        
    def set_quantum(self, quantum):
        self.quantum = quantum
        
    def compute_pc(self, shift):
        return self.base_direction + shift