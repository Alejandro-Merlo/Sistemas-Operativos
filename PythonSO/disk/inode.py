'''
Created on 02/12/2013

@author: Alejandro
'''
from disk.algorithm import Algorithm

class INode(Algorithm):
    
    def __init__(self, size):
        Algorithm.__init__(self, size)
        self.nodes = {} # El mapa de nodos, algunos nodos son indices y otros contienen la direccion en disco del programa
        
    # Cada nodo guarda una instruccion del programa?
    def save(self, program, sectors):
        None
        
    #def show(self, sectors):
        
    #def fetch(self, p_name, sectors):