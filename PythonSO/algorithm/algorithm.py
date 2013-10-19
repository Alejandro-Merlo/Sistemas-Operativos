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
    def add(self, process):
        pass
    
    @abstractmethod    
    def get(self):
        pass