'''
Created on 30/10/2013

@author: Alejandro
'''
from algorithm import Algorithm
from block import Block

class MVT(Algorithm):
    
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.full        = {} # Mapeo de bloques llenos: PCB -> Bloque
        self.empty       = [Block(0, memory_size - 1)]

    def load(self, pcb, physical_memory):
        
        block_to_delete = None
        #free_space      = 0
        for block in self.empty:
            #free_space += block.size
            if self.is_available(pcb, block):
                block_to_delete    = block
                pcb.base_direction = block.start
                self.load_physical(pcb, physical_memory)
                self.divide(pcb, block)
                break
        
        if block_to_delete is not None:
            self.empty.remove(block_to_delete)
        else:
            print 'No hay espacio en memoria'
            # Aca va el corrimiento de huecos libres (Strategy pattern de cada ajuste)
                
    def load_physical(self, pcb, physical_memory):
        direction = pcb.base_direction
        for instruction in pcb.program.instructions:
            physical_memory[direction] = instruction
            direction += 1

    def is_available(self, pcb, block):
        return block.size >= len(pcb.program.instructions)

    def divide(self, pcb, block):
        new_full_block  = Block(block.start, block.start + len(pcb.program.instructions) - 1)
        new_empty_block = Block(block.start + len(pcb.program.instructions), block.end)
        self.full[pcb]  = new_full_block
        self.empty.append(new_empty_block)
        
    def unload(self, pcb, physical_memory):
        block = self.full[pcb]
        del self.full[pcb]
        self.free(block)
        self.unload_physical(pcb, physical_memory)
        pcb.base_direction = None
            
    def unload_physical(self, pcb, physical_memory):
        for direction in range(0, len(pcb.program.instructions)):
            del physical_memory[pcb.base_direction + direction]
            
    def free(self, block):
        linked = False
        for e_block in self.empty:
            if e_block.start == block.end:
                linked = True
                e_block.start = block.start
                break
            elif e_block.end == block.start:
                linked = True
                e_block.end = block.end
                break
        
        if not linked:
            block.shift = 0
            self.empty.append(block)
        
    def fetch(self, pcb, physical_memory):
        block  = self.full[pcb]
        result = physical_memory[pcb.compute_pc(block.shift)]
        block.shift += 1
        return result