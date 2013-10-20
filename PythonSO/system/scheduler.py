'''
Created on 19/10/2013

@author: Alejandro
'''
class Scheduler():
    
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def add_element(self, process, ready_queue):
        self.algorithm.add(process, ready_queue)

    def choose_next(self, ready_queue):
        return self.algorithm.get(ready_queue)

    # Esto se ve caro, preguntar otras maneras de hacerlo
    def aging(self, processes):
        for process in processes:
            process.aging = process.aging - 1
            
    # Esto se ve caro, preguntar otras maneras de hacerlo
    def update(self, processes):
        for process in processes:
            if process.aging == 0:
                self.algorithm.boost_priority(process)