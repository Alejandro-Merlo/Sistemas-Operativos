'''
Created on 03/11/2013

@author: Alejandro
'''
from algorithm import Algorithm
from frame import Frame
from page import Page

class Pagination(Algorithm):
    
    def __init__(self, memory_size, page_size):
        # PRECONDICION:
        # El tamanio de la pagina debe ser multiplo del tamanio de la memoria
        Pagination.__init__(self, memory_size)
        self.page_size  = page_size # Los marcos y paginas son del mismo tamaño
        self.frames     = [] # Marcos que representan la memoria fisica
        self.pages      = [] # Paginas que representan la memoria logica
        self.page_table = {} # Tabla de paginas: Numero de pagina -> Numero de marco
        
        for number in range(memory_size / page_size):
            frame_start = number * page_size
            self.frames.append(Frame(page_size, number, frame_start, frame_start + page_size - 1))
            self.pages.append(Page(page_size, number))
            
    
    def can_load(self, pcb):
        frames_needed = pcb.size_in_memory() / self.page_size
        if isinstance(frames_needed, int):
            return len(self.frames) >= frames_needed
        else:
            return len(self.frames) >= frames_needed + 1
        
    def load(self, pcb, physical_memory):
        for instruction in pcb.program.instructions:
            None
        
    #def unload(self, pcb, physical_memory):
        
    #def fetch(self, program_direction):
        