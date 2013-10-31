'''
Created on 31/10/2013

@author: Alejandro
'''
class IRQ():
    
    def io_signal(self, kernel, pcb, io_instruction):
        kernel.io_handler.add(pcb, io_instruction)
        kernel.kernel_waiting_cpu.release()
        
    def io_kill_signal(self, kernel, pcb):
        # Agregar mecanismo que detenga los otros threads?
        kernel.memory.unload(pcb)
        pcb.state = 'Terminated'
        
    def io_ready_signal(self, kernel, pcb):
        kernel.ready_list.append(pcb)
        kernel.scheduler.add_element(pcb)
        
    def cpu_kill_signal(self, kernel, pcb):
        # Agregar mecanismo que detenga los otros threads?
        kernel.memory.unload(pcb)
        pcb.state = 'Terminated'
        kernel.kernel_waiting_cpu.release()
        
    def cpu_ready_signal(self, kernel, pcb):
        kernel.ready_list.append(pcb)
        kernel.scheduler.add_element(pcb)
        kernel.kernel_waiting_cpu.release()