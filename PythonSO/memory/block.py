'''
Created on 30/10/2013

@author: Alejandro
'''
class Block():
    
    def __init__(self, start, end, previous = None, nextt = None, is_empty = True):
        self.start    = start
        self.end      = end
        self.previous = previous # El bloque previo dentro de la memoria
        self.next     = nextt # El bloque proximo dentro de la memoria
        self.is_empty = is_empty
        # Desplazamiento del proceso en memoria asignado a este bloque
        # Los bloques vacios siempre lo tienen en 0
        self.shift = 0
        
    def size(self):
        return self.end - self.start + 1