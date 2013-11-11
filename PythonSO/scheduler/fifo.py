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
        self.ready_list.append(process)
        
    def get(self):
        if self.ready_list == []:
            return None
        return self.ready_list.pop(0)