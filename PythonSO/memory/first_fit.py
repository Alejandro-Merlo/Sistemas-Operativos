'''
Created on 31/10/2013

@author: Alejandro
'''
from block_selection_strategy import BlockSelectionStrategy

class FirstFit(BlockSelectionStrategy):
    
    def select(self, mvt, pcb):
        for block in mvt.empty:
            if self.is_suitable(pcb, block):
                return block
        return None