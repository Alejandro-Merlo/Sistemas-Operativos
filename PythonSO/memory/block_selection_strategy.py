'''
Created on 31/10/2013

@author: Alejandro
'''
from abc import ABCMeta, abstractmethod

class BlockSelectionStrategy():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def select_for(self, mvt, pcb):
        pass
    
    def is_suitable(self, pcb, block):
        return block.size() >= len(pcb.program.instructions)