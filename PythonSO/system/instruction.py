'''
Created on 21/10/2013

@author: Alejandro
'''
from abc import ABCMeta, abstractmethod

class Instruction:
    __metaclass__ = ABCMeta
    
    def __init__(self, value):
        self.value = value
        
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def is_cpu(self):
        pass