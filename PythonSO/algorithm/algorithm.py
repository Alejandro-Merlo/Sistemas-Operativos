'''
Created on 19/10/2013

@author: Alejandro
'''
from abc import ABCMeta, abstractmethod

class Algorithm():
    __metaclass__ = ABCMeta
    
    def __init__(self, structure):
        self.structure = structure
        
    @abstractmethod    
    def add(self, process, ready_queue):
        pass
    
    @abstractmethod    
    def get(self, ready_queue):
        pass