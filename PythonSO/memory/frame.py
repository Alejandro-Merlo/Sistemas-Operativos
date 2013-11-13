'''
Created on 03/11/2013

@author: Alejandro
'''
class Frame():
    
    def __init__(self, size, number, start):
        self.start  = start
        self.end    = start + size - 1
        self.size   = size
        self.number = number