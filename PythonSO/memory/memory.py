'''
Created on 27/10/2013

@author: Alejandro
'''
class MMU():
    
    def __init__(self, logical_memory):
        # La memoria fisica es un mapa de direccion -> valor
        # La memoria logica en el caso de asignacion continua
        # es un bloque del tama�o de la memoria fisica entera
        # que se va dividiendo a medida que cargo la memoria
        # en m�s bloques, los usados y los libres.
        self.physical_memory = {}
        self.logical_memory  = logical_memory
        
    def fetch(self, pcb):
        program_direction = pcb.base_direction
        return self.physical_memory.get(self.logical_memory.fetch(program_direction))
        
    def load(self, pcb):
        # Seteo la direcci�n base del pcb ac�
        # Alojo las instrucciones del pcb en un bloque
        self.logical_memory.load(pcb, self.physical_memory)
        
    def unload(self, pcb):
        # Libero el bloque donde aloj� al proceso ac� y luego
        # si queda adyacente a otro bloque vac�o, los fusiono.
        # Seteo en nulo la direcci�n base del pcb
        self.logical_memory.unload(pcb, self.physical_memory)