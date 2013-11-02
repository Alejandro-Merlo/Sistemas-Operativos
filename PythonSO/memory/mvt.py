'''
Created on 30/10/2013

@author: Alejandro
'''
from algorithm import Algorithm
from block import Block

class MVT(Algorithm):
    
    def __init__(self, memory_size, selection_method):
        # Los bloques adyacentes a un bloque vacio siempre estan llenos
        # Los bloques adyacentes a un bloque lleno pueden estar vacios o llenos 
        self.memory_size      = memory_size
        self.selection_method = selection_method
        self.full             = {} # Mapeo de bloques llenos: PCB -> Bloque
        self.empty            = [Block(0, memory_size - 1)] # Lista de bloques vacios
        
    def can_load(self, pcb):
        free_space = self.free_space()
        for block in self.empty:
            if pcb.size_in_memory() <= block.size() or pcb.size_in_memory() <= free_space:
                return True
        return False

    def load(self, pcb, physical_memory):
        result = self.selection_method.select_for(self, pcb)
        if result is not None:
            self._load_result(pcb, physical_memory, result)
        else:
            self.do_shift(self, physical_memory)
            self._load_result(pcb, physical_memory, self.empty[0])

    def _load_result(self, pcb, physical_memory, result):
        pcb.base_direction = result.start
        self.load_physical(pcb, physical_memory)
        self.divide(pcb, result)
        
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
        return block.shift + 1 == pcb.size_in_memory()
    
    def do_shift(self, physical_memory):
        print 'Memoria haciendo corrimiento de bloques'
        first = self.first_empty_block()
        # Se repite hasta quedar un solo bloque vacio al final de la memoria
        while first.next is not None:
            if not first.next.is_empty:
                self.swap(first, first.next, physical_memory)
            else:
                self.fuse(first, first.next)            
        
    def swap(self, empty_block, full_block, physical_memory):
        f_ex_start           = full_block.start
        # Intercambio posiciones
        f_size               = full_block.size() - 1
        full_block.start     = empty_block.start
        empty_block.end      = full_block.end
        full_block.end       = full_block.start + f_size
        empty_block.start    = full_block.end + 1
        # Actualizo su anterior y su siguiente
        f_next               = full_block.next
        full_block.next      = empty_block
        full_block.previous  = empty_block.previous
        empty_block.previous = full_block
        empty_block.next     = f_next
        self.swap_physical(f_ex_start, full_block, physical_memory, self.find_pcb(full_block))
            
    def fuse(self, empty, empty_next):
        self.empty.remove(empty_next)
        empty.end  = empty_next.end
        empty.next = empty_next.next
        
    def swap_physical(self, ex_start, full_block, physical_memory, pcb):
        # Reacomodo cada instruccion en su nueva entrada correspondiente
        pcb.base_direction = full_block.start
        for direction in range(0, pcb.size_in_memory()):
            physical_memory[pcb.base_direction + direction] = physical_memory[ex_start + direction]
            
    def find_pcb(self, full_block):
        for pcb, block in self.full.iteritems():
            if block == full_block:
                return pcb
        
    def first_empty_block(self):
        for block in self.empty:
            # Si esta al comienzo de la lista o todos los bloques anteriores estan llenos
            if block.previous is None or (not block.previous.is_empty and self._are_previous_full(block.previous)):
                return block
            
    def _are_all_full(self, block):
        previous = block.previous
        while previous is not None:
            if previous.is_empty:
                return False
            previous = previous.previous
        return True
    
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
        new_block_size = pcb.size_in_memory() - 1
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
        for direction in range(0, pcb.size_in_memory()):
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