'''
Created on 19/11/2013

@author: Alejandro
'''
class HDD():
    
    def __init__(self):
        self.programs = []
        
    def save(self, program):
        self.programs.append(program)
        
    def show_programs(self):
        print 'Programas en disco:'
        for program in self.programs:
            print program.name
            
    def fetch(self, program_name):
        for program in self.programs:
            if program.name == program_name:
                return program
        return RuntimeError