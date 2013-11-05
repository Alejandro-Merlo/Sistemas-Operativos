'''
Created on 21/10/2013

@author: Alejandro
'''
from instruction import Instruction

class InstructionCPU(Instruction):
    
    def __init__(self, value):
        Instruction.__init__(self, value)
        
    def is_cpu(self):
        return True