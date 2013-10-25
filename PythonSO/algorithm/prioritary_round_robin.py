'''
Created on 19/10/2013

@author: Alejandro
'''
from algorithm import Algorithm
from priority_map import PriorityMap

class PrioritaryRoundRobin(Algorithm):
    
    def __init__(self, quantum, priorities_quant, aging_quant):
        Algorithm.__init__(self, PriorityMap(priorities_quant, aging_quant))
        self.quantum        = quantum
    
    def add(self, process):
        self.structure.add(process)
        process.quantum = self.quantum
                
    def get(self):
        pcb = self.structure.pop_next_to_execute()
        self.structure.age_all()
        return pcb
