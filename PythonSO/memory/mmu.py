'''
Created on 27/10/2013

@author: Alejandro
'''
class MMU():
    
    def __init__(self, logical_memory):
        # La memoria fisica es un mapa de direccion -> valor
        # La memoria logica en el caso de asignacion continua
        # es un bloque del tamaño de la memoria fisica entera
        # que se va dividiendo a medida que cargo la memoria
        # en más bloques, los usados y los libres.
        self.physical_memory = {}
        self.logical_memory  = logical_memory
        
    def fetch(self, pcb):
        program_direction = pcb.base_direction
        return self.physical_memory.get(self.logical_memory.fetch(program_direction))
        
    def load(self, pcb):
        # Seteo la dirección base del pcb acá
        # Alojo las instrucciones del pcb en un bloque
        self.logical_memory.load(pcb, self.physical_memory)
        
    def unload(self, pcb):
        # Libero el bloque donde alojé al proceso acá y luego
        # si queda adyacente a otro bloque vacío, los fusiono.
        # Seteo en nulo la dirección base del pcb
        self.logical_memory.unload(pcb, self.physical_memory)