'''
Created on 19/10/2013

@author: Alejandro
'''
from algorithm import Algorithm
from priority_map import PriorityMap

class PrioritaryRoundRobin(Algorithm):
    
    def __init__(self, quantum):
        Algorithm.__init__(self, PriorityMap())
        self.structure      = PriorityMap() # Lo agrego porque no me deja usar el constructor del padre
        self.processes      = [] # Lista de procesos
        self.next_to_choose = None # Proximo proceso a ejecutar
        self.quantum        = quantum
    
    def add(self, process):
        self.structure.add(process)
        self.sort(process)
        process.quantum = self.quantum
        
    def sort(self, process):
        
        if self.processes == []:
            self.next_to_choose = process
            
        for current in self.processes:
            if current.previous is None:
                if current.priority > process.priority:
                    current.previous    = process
                    process.next        = current
                    self.next_to_choose = process
            else:
                previous = current.previous
                if current.priority > process.priority and previous.priority <= process.priority:
                    current.previous = process
                    previous.next    = process
                    process.previous = previous
                    process.next     = current
                    
            if current.next is None:
                if current.priority <= process.priority:
                    current.next     = process
                    process.previous = current
            else:
                nextt = current.next
                if current.priority <= process.priority and nextt.priority > process.priority:
                    current.next     = process
                    nextt.previous   = process
                    process.previous = current
                    process.next     = nextt
                    
        self.processes.append(process)
        
    def get(self):
        if self.next_to_choose is not None:
            process = self.next_to_choose
            self.next_to_choose = process.next
            if process.next is not None:
                self.next_to_choose.previous = None
            process.next = None
            self.processes.remove(process)
            self.structure.remove(process)
            return process
        return None
