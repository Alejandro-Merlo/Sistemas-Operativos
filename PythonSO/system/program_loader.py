'''
Created on 19/11/2013

@author: Alejandro
'''
import random
from program import Program
from instruction_cpu import InstructionCPU
from instruction_io import InstructionIO

class ProgramLoader:
    
    def __init__(self, hdd):
        self.hdd = hdd
        
    def save_programs(self):
        for e in range(20):
            instructions = []
            
            for i in range(1, random.randint(2, 8)):
                instructions.append(InstructionCPU('Programa' + str(e) + ' -> Instruccion CPU' + str(i)))
                
            for i in range(1, random.randint(2, 3)):
                instructions.append(InstructionIO('Programa' + str(e) + ' -> Instruccion IO' + str(i)))
                
            new_program = Program("Programa" + str(e), instructions)
            self.hdd.save(new_program)
        