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
        self.empty            = [Block(0, memory_size - 1)]

    def load(self, pcb, physical_memory):
        result = self.selection_method.select_for(self, pcb)
        if result is not None:
            pcb.base_direction = result.start
            self.load_physical(pcb, physical_memory)
            self.divide(pcb, result)
            self.empty.remove(result)
        elif self.free_space() >= len(pcb.program.instructions):
            self.do_shift(self)
            # Aca iria el corrimiento de huecos libres, lo hace el strategy o la clase?
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
        result = physical_memory[pcb.compute_pc(block.shift)]
        block.shift += 1
        return result
            
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
        # Divido el bloque vacio en uno lleno y en uno posible con el espacio restante
        new_full_block = Block(block.start, block.start + len(pcb.program.instructions) - 1)
        if new_full_block.size() < block.size():
            new_empty_block = Block(block.start + len(pcb.program.instructions), block.end)
        self.full[pcb] = new_full_block
        self.empty.append(new_empty_block)
            
    def unload_physical(self, pcb, physical_memory):
        for direction in range(0, len(pcb.program.instructions)):
            del physical_memory[pcb.base_direction + direction]
            
    def free(self, block):
        # Se asume que no hay bloques vacios con el rango del recientemente liberado
        # por logica del mismo algoritmo
        nextt    = None
        previous = None
        for e_block in self.empty:
            if e_block.start - 1 == block.end:
                nextt = e_block
            elif e_block.end + 1 == block.start:
                previous = e_block
        
        if nextt is None:
            if previous is None:
                # Si el bloque liberado no se puede fusionar con ningun otro
                # bloque vacio lo agrego a la lista 
                block.shift = 0
                self.empty.append(block)
            else:
                # Si el sector siguiente al final del bloque vacio
                # concuerda con el comienzo del bloque liberado los fusiono
                previous.end = block.end
        elif previous is None:
            # Si el sector anterior al comienzo del bloque vacio
            # concuerda con el final del bloque liberado los fusiono
            nextt.start = block.start
        else:
            # Si ambos extremos del bloque liberado se pueden fusionar
            # elijo uno de los bloques adyacentes y lo fusiono con los otros dos
            # eliminando de la lista al otro bloque adyacente
            previous.end = nextt.end
            self.empty.remove(nextt)