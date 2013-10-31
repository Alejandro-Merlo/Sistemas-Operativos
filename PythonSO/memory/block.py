'''
Created on 30/10/2013

@author: Alejandro
'''
class Block():
    
    def __init__(self, start, end):
        self.start = start
        self.end   = end
        # Desplazamiento del proceso en memoria asignado a este bloque
        # Los bloques vacios siempre lo tienen en 0
        self.shift = 0
        
    def size(self):
        return self.end - self.start + 1