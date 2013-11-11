'''
Created on 05/11/2013

@author: Alejandro
'''
from pcb import PCB

class LongTermScheduler():
    
    def __init__(self, memory):
        self.incoming_list = [] # Procesos esperando para cargarse en memoria
        self.memory        = memory
        self.global_id     = 0
        
    def create(self, program, kernel):
        process        = PCB(program, self.global_id)
        self.global_id = self.global_id + 1
        self._check_loading(process, kernel)

    def _check_loading(self, process, kernel):
        if self.memory.can_load(process):
            kernel.new_signal(process)
        else:
            print 'Proceso' + str(process.pid) + ' esperando espacio en memoria'
            self.incoming_list.append(process)
            
    def load_process(self, kernel, process):
        process.state = "Ready"
        self.memory.load(process)
        kernel.scheduler.add_element(process)

    
    def kill(self, kernel, pcb):
        print 'Proceso' + str(pcb.pid) + ' ha terminado su ejecucion'
        self.memory.unload(pcb)
        pcb.state = 'Terminated'
        self._check_next(kernel)
    
    def _check_next(self, kernel):
        next_pcb = self._look_for_next_to_load()
        while next_pcb is not None:
            self.incoming_list.remove(next_pcb)
            self.load_process(kernel, next_pcb)
            next_pcb = self._look_for_next_to_load()
            
    def _look_for_next_to_load(self):
        for pcb in self.incoming_list:
            if self.memory.can_load(pcb):
                return pcb
        return None