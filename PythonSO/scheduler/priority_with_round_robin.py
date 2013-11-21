'''
Created on 19/10/2013

@author: Alejandro
'''
from algorithm import Algorithm
from priority_map import PriorityMap

class PriorityWithRoundRobin(Algorithm):
    
    def __init__(self, quantum, priorities_quant, aging_quant):
        Algorithm.__init__(self, PriorityMap(priorities_quant, aging_quant))
        self.quantum = quantum
    
    def add(self, process):
        process.set_quantum(self.quantum)
        self.ready_list.add(process)
                
    def get(self):
        pcb = self.ready_list.pop_next_to_execute()
        self.ready_list.age_all()
        return pcb
