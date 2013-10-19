'''
Created on 19/10/2013

@author: Alejandro
'''
class PriorityMap:
    
    def __init__(self):
        self.priorities = {}
        
    def add(self, process):
        if self.priorities.has_key(process.priority):
            priority_list = self.priorities[process.priority]
            priority_list.append(process)
        else:
            self.priorities[process.priority] = [process]
            
    def remove(self, process):
        priority_list = self.priorities[process.priority]
        priority_list.remove(process)