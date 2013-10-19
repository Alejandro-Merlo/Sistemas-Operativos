'''
Created on 19/10/2013

@author: Alejandro
'''
class Program:
  
    def __init__(self, name, instructions_list):
        self.instructions = instructions_list
        self.name         = name

    def print_instructions(self):
        print 'Program Instructions:'
        for inst in self.instructions:
            print inst