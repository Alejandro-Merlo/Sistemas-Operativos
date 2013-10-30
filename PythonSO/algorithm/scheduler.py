'''
Created on 19/10/2013

@author: Alejandro
'''
class Scheduler():
    
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def add_element(self, process):
        self.algorithm.add(process)

    def choose_next(self):
        return self.algorithm.get()