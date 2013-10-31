'''
Created on 30/10/2013

@author: Alejandro
'''
from abc import ABCMeta, abstractmethod

class Algorithm():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def load(self, pcb, physical_memory):
        pass
    
    @abstractmethod
    def unload(self, pcb, physical_memory):
        pass
    
    @abstractmethod
    def fetch(self, program_direction):
        pass