'''
Created on 19/11/2013

@author: Alejandro
'''
class HDD():
    
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.sectors   = {}
        
    def save(self, program):
        self.algorithm.save(program, self.sectors)
        
    def show_programs(self):
        print 'Programas en disco:'
        self.algorithm.show()
    
    def fetch(self, program_name):
        return self.algorithm.fetch(program_name, self.sectors)
    
    def programs_saved(self):
        return self.algorithm.programs_saved()
