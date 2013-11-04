'''
Created on 30/10/2013

@author: Alejandro
'''
from abc import ABCMeta, abstractmethod

class Algorithm():
    __metaclass__ = ABCMeta
    
    def __init__(self, memory_size):
        self.memory_size = memory_size
    
    @abstractmethod
    def can_load(self, pcb):
        pass
    
    @abstractmethod
    def load(self, pcb, physical_memory):
        pass
    
    @abstractmethod
    def unload(self, pcb, physical_memory):
        pass
    
    @abstractmethod
    def fetch(self, program_direction):
        pass