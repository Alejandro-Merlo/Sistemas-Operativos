'''
Created on 31/10/2013

@author: Alejandro
'''
from block_selection_strategy import BlockSelectionStrategy

class WorstFit(BlockSelectionStrategy):
    
    def select_for(self, mvt, pcb):
        # Si la lista estuviese ordenada por tamanios seria mas performante
        worst_fit = (None, None)
        for block in mvt.empty:
            if self._is_suitable(pcb, block):
                if worst_fit[0] is None:
                    worst_fit = (block.size(), block)
                elif block.size() > worst_fit[0]:
                    worst_fit = (block.size(), block)
        return worst_fit[1]