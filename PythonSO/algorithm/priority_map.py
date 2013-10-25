'''
Created on 19/10/2013

@author: Alejandro
'''
import random

class PriorityMap:
    
    def __init__(self, priorities_quant, aging_quant):
        self.priorities   = {}
        self.max_priority = priorities_quant
        self.max_aging    = aging_quant
        
        self.priorities[0] = {0:[]}
        for p in range(1, self.max_priority):
            new_dict = {}
            for a in range(self.max_aging):
                new_dict[a] = []
            self.priorities[p] = new_dict
        
    def add(self, process):
        # TODO: Pensar en la forma de recuperar prioridad de los procesos evitando guardarlo en la clase
        new_priority = random.randint(0, self.max_priority - 1)
        self.priorities[new_priority][0].append(process)
        
    def pop_next_to_execute(self):
        # Si la prioridad 0 con envejecimiento 0 esta vacia
        if not self.priorities[0][0]:
            # Busca en orden ascendente por el diccionario el proximo que no es vacio
            for p in range(1, self.max_priority):
                for a in range(self.max_aging - 1, -1, -1):
                    if self.priorities[p][a]:
                        return self.priorities[p][a].pop(0)
        else:
            return self.priorities[0][0].pop(0)
        # Si no encuentra nada devuelve nulo
        return None
    
    def age_all(self):
        for p in range(1, self.max_priority):
            # Si estoy parado en la prioridad 1 con el maximo envejecimiento
            if p == 1:
                self.priorities[p-1][0].extend(self.priorities[p][self.max_aging - 1])
            # Entonces estoy parado en cualquier otra prioridad con el maximo envejecimiento
            else:
                self.priorities[p-1][0] = self.priorities[p][self.max_aging - 1]
            # Actualiza los otros envejecimientos de cada prioridad
            for a in range(self.max_aging - 2, -1, -1):
                self.priorities[p][a+1] = self.priorities[p][a]
        # Asigna lista vacia a la maxima prioridad con envejecimiento 0 (Final del diccionario)
        self.priorities[self.max_priority-1][0] = []