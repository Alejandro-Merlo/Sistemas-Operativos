'''
Created on 27/10/2013

@author: Alejandro
'''
class MMU():
    
    def __init__(self, logical_memory):
        self.physical_memory = {} # Memoria fisica: Direccion -> Valor
        self.logical_memory  = logical_memory # Memoria logica (Solo MVT por ahora)
        
    def load(self, pcb):
        print pcb.program.name + ' alocandose en memoria'
        self.logical_memory.load(pcb, self.physical_memory)
        
    def unload(self, pcb):
        print pcb.program.name + ' desalocandose de la memoria'
        self.logical_memory.unload(pcb, self.physical_memory)
        
    def fetch(self, pcb):
        print 'Memoria buscando siguiente instruccion de ' + pcb.program.name
        return self.logical_memory.fetch(pcb, self.physical_memory)