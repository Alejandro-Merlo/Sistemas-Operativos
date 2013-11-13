'''
Created on 27/10/2013

@author: Alejandro
'''
class MMU():
    
    def __init__(self, logical_memory, memory_size):
        self.physical_memory = {} # Memoria fisica: Direccion -> Valor
        self.logical_memory  = logical_memory # Memoria logica (MVT o Paginacion)
        
        self.init_memory(memory_size)
        self.do_dump_state()
        
        
    def init_memory(self, memory_size):
        for direction in range(memory_size):
            self.physical_memory[direction] = None
    
    def do_dump_state(self):
        print 'Estado de memoria'
        self.logical_memory.do_dump_state()
        print 'Memoria principal:'
        for cell, instruction in self.physical_memory.iteritems():
            if instruction is not None:
                print str(cell) + ' -> ' + instruction.value
            else:
                print str(cell) + ' -> Vacio'
        
    def can_load(self, pcb):
        return self.logical_memory.can_load(pcb)
        
    def load(self, pcb):
        print 'Proceso' + str(pcb.pid) + ' alocandose en memoria'
        self.logical_memory.load(pcb, self.physical_memory)
        self.do_dump_state()
        
    def unload(self, pcb):
        print 'Proceso' + str(pcb.pid) + ' desalocandose de la memoria'
        self.logical_memory.unload(pcb, self.physical_memory)
        self.do_dump_state()
        
    def fetch(self, pcb):
        return self.logical_memory.fetch(pcb, self.physical_memory)