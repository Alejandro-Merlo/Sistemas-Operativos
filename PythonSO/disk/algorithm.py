'''
Created on 01/12/2013

@author: Alejandro
'''

from abc import ABCMeta, abstractmethod

class Algorithm():
    __metaclass__ = ABCMeta
    
    def __init__(self, size):
        self.size = size
    
    @abstractmethod
    def save(self, program, disk_map):
        pass
    
    @abstractmethod
    def show(self):
        pass
    
    @abstractmethod
    def fetch(self, p_name, disk_map):
        pass
