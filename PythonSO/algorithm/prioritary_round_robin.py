'''
Created on 19/10/2013

@author: Alejandro
'''
from algorithm import Algorithm
from priority_map import PriorityMap

class PrioritaryRoundRobin(Algorithm):
    
    def __init__(self, quantum, aging):
        Algorithm.__init__(self, PriorityMap())
        self.structure      = PriorityMap() # Lo agrego porque no me deja usar el constructor del padre
        self.next_to_choose = None # Proximo proceso a ejecutar
        self.quantum        = quantum
        self.aging          = aging
    
    def add(self, process, ready_queue):
        self.structure.add(process)
        self.sort(process, ready_queue)
        
        process.quantum = self.quantum
        process.aging   = self.aging
        
    def sort(self, process, ready_queue):
        
        if ready_queue == []:
            self.next_to_choose = process
            
        for current in ready_queue:
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
                    
        ready_queue.append(process)
        
    def get(self, ready_queue):
        if self.next_to_choose is not None:
            process             = self.next_to_choose
            self.next_to_choose = process.next
            
            if process.next is not None:
                self.next_to_choose.previous = None
                
            process.next  = None
            process.aging = self.aging
            
            ready_queue.remove(process)
            self.structure.remove(process)
            return process
        return None
    
    def boost_priority(self, process):
        if process.priority != 0:
            print process.program.name + ' aumenta su prioridad por envejecimiento de ' + str(process.priority) + ' a ' + str(process.priority - 1)
            self.structure.remove(process)
            process.priority = process.priority -1
            process.aging    = self.aging
            self.structure.add(process)
