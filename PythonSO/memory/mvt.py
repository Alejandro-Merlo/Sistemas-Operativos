'''
Created on 30/10/2013

@author: Alejandro
'''
from algorithm import Algorithm
from block import Block

class MVT(Algorithm):
    
    def __init__(self, memory_size, selection_method):
        self.memory_size      = memory_size
        self.selection_method = selection_method
        self.full             = {} # Mapeo de bloques llenos: PCB -> Bloque
        self.empty            = [Block(0, memory_size - 1)] # Lista de bloques vacios ordenada

    def load(self, pcb, physical_memory):
        result = self.selection_method.select_for(self, pcb)
        if result is not None:
            pcb.base_direction = result.start
            self.load_physical(pcb, physical_memory)
            self.divide(pcb, result)
        elif self.free_space() >= len(pcb.program.instructions):
            self.do_shift(self)
        else:
            print 'No hay espacio en memoria'
            # Aca iria roll in roll out?
        
    def unload(self, pcb, physical_memory):
        block = self.full[pcb]
        del self.full[pcb]
        self.free(block)
        self.unload_physical(pcb, physical_memory)
        pcb.base_direction = None        

    def fetch(self, pcb, physical_memory):
        block  = self.full[pcb]
        result = (self._is_the_last_instruction(pcb, block) , physical_memory[pcb.compute_pc(block.shift)])
        block.shift += 1
        return result

    def _is_the_last_instruction(self, pcb, block):
        return block.shift + 1 == len(pcb.program.instructions)
    
    def do_shift(self):
        for e_block in self.empty:
            for f_block in self.full:
                
                None
            
    def free_space(self):
        space = 0
        for block in self.empty:
            space += block.size()
        return space
                
    def load_physical(self, pcb, physical_memory):
        direction = pcb.base_direction
        for instruction in pcb.program.instructions:
            physical_memory[direction] = instruction
            direction += 1

    def divide(self, pcb, block):
        # Contemplo el caso en que el nuevo bloque lleno no alcanza a
        # cubrir todo el bloque vacio y el caso en que si alcanza a cubrirlo.
        # En ambos casos reutilizo la informacion del bloque vacio.
        new_block_size = len(pcb.program.instructions) - 1
        if new_block_size < block.size():
            new_full_block = Block(block.start, block.start + new_block_size, block.previous, block, False)
            if block.previous is not None:
                block.previous.next = new_full_block
            block.start += new_block_size + 1
            block.previous = new_full_block
            self.full[pcb] = new_full_block
        else:
            self.full[pcb] = block
            block.is_empty = False
            self.empty.remove(block)
            
    def unload_physical(self, pcb, physical_memory):
        for direction in range(0, len(pcb.program.instructions)):
            del physical_memory[pcb.base_direction + direction]
            
    def free(self, block):
        if block.next is None or not block.next.is_empty:
            if block.previous is None or not block.previous.is_empty:
                # Ya sea que no tenga ni anterior ni siguiente o que, si los tiene, esten llenos
                # lo agrego directamente a la lista vacia
                block.shift    = 0
                block.is_empty = True
                self.empty.append(block)
            else:
                # En caso de que el siguiente no exista o que este lleno, no importa el caso
                # del anterior lo fusiono con este ultimo
                block.previous.end  = block.end
                block.previous.next = block.next
        elif block.previous is None or not block.previous.is_empty:
            # En caso de que el anterior no exista o que este lleno, no importa el caso
            # del siguiente lo fusiono con este ultimo
            block.next.start    = block.start
            block.next.previous = block.previous
        else:
            # Finalmente, ambos estan vacios por lo que fusiono los tres bloques
            block.previous.end  = block.next.end
            block.previous.next = block.next.next
            self.empty.remove(block.next)