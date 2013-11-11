'''
Created on 03/11/2013

@author: Alejandro
'''
class Page():
    
    def __init__(self, size, number):
        self.size    = size
        self.number  = number
        #self.shift   = 0 # Lo mismo que con el bloque lleno, deberia ir en el pcb o aca?
        self.content = []