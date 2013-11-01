'''
Created on 31/10/2013

@author: Alejandro
'''
from block_selection_strategy import BlockSelectionStrategy

class BestFit(BlockSelectionStrategy):
    
    def select_for(self, mvt, pcb):
        # Si la lista estuviese ordenada por tamanios seria mas performante
        best_fit = (None, None)
        for block in mvt.empty:
            if self._is_suitable(pcb, block):
                if best_fit[0] is None:
                    best_fit = (block.size(), block)
                elif block.size() < best_fit[0]:
                    best_fit = (block.size(), block)
        return best_fit[1]