'''
Created on 19/11/2013

@author: Alejandro
'''
class HDD():
    
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.map       = {}
        
    def save(self, program):
        self.algorithm.save(program, self.map)
        
    def show_programs(self):
        print 'Programas en disco:'
        self.algorithm.show(self.map)
                    
    def fetch(self, program_name):
        self.algorithm.fetch(program_name, self.map)