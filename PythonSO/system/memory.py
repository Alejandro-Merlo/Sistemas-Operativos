'''
Created on 27/10/2013

@author: Alejandro
'''
class Memory():
    
    def __init__(self, logical_memory):
        self.full           = {}
        self.empty          = {}
        self.logical_memory = logical_memory
        self.base_direction = 0
        
    def get(self, direction):
        return None
        
    def put(self, direction, value):
        None