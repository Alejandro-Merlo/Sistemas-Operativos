'''
Created on 19/10/2013

@author: Alejandro
'''
from abc import ABCMeta, abstractmethod

class Algorithm():
    __metaclass__ = ABCMeta
    
    def __init__(self, structure):
        self.ready_list = structure # Procesos listos para competir por la CPU
        
    @abstractmethod    
    def add(self, process):
        pass
    
    @abstractmethod    
    def get(self):
        pass