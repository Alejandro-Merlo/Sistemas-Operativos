'''
Created on 22/10/2013

@author: Alejandro
'''
from algorithm import Algorithm

class FIFO(Algorithm):
    
    def __init__(self):
        Algorithm.__init__(self, [])
        
    def add(self, process):
        process.set_priority(0)
        self.structure.append(process)
        
    def get(self):
        if self.structure == []:
            return None
        return self.structure.pop(0)