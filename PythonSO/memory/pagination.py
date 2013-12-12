'''
Created on 03/11/2013

@author: Alejandro
'''
from __future__ import division
from algorithm import Algorithm
from frame import Frame
from page import Page
import math

class Pagination(Algorithm):
    
    def __init__(self, memory_size, page_size):
        # PRECONDICION:
        # El tamanio de una pagina es una potencia de 2
        Algorithm.__init__(self, memory_size)
        self.page_size    = page_size # Los marcos y paginas son del mismo tamanio
        self.empty_frames = [] # Marcos vacios de la memoria fisica
        self.pages        = {} # Paginas que representan la memoria logica
        self.page_table   = {} # Tabla de paginas: Numero de pagina -> Marco
        self.free_numbers = [] # Numeros de pagina libres 
        
        self._create_frames(memory_size, page_size)
            

    def _create_frames(self, memory_size, page_size):
        for number in range(int(memory_size / page_size)):
            frame_start = number * page_size
            self.empty_frames.append(Frame(page_size, number, frame_start))
            self.free_numbers.append(number)
            
    def do_dump_state(self):
        print 'Frames libres:'
        for frame in self.empty_frames:
            print str(frame.number) + ' -> [' + str(frame.start) + ',' + str(frame.end) + ']'
        print 'Paginas en uso:'
        for pcb, pages in self.pages.iteritems():
            for page in pages:
                print str(page.number) + ' -> Proceso' + str(pcb.pid) + self._print_content(page)
            
    def _print_content(self, page):
        result = ': ['
        for instruction in page.content:
            result = result + instruction.value + ', '
        result = result + ']'
        return result
    
    
    ###################
    # CARGA
    ###################
    def can_load(self, pcb):
        return len(self.empty_frames) >= math.ceil(pcb.burst / self.page_size)

    def load(self, pcb, physical_memory):
        self.pages[pcb]     = []
        pcb.remaining_pages = []
        page_start_in_list  = 0 # Entrada que indica el comienzo de una pagina dentro de la lista de instrucciones
        frames_to_use       = int(math.ceil(pcb.burst / self.page_size))
        for _ in range(frames_to_use):
            new_page                         = Page(self.page_size, self.free_numbers.pop(0)) # Creo la pagina nueva
            self.pages[pcb].append(new_page)
            frame                            = self.empty_frames.pop(0) # Saco un frame libre
            self.page_table[new_page.number] = frame # Agrego la nueva entrada a la tabla de paginas
            pcb.remaining_pages.append(new_page.number) # Agrego el numero de pagina al PCB
            self._load_page(pcb, page_start_in_list, new_page)
            self._load_physical(physical_memory, frame, new_page) # Cargo la memoria con la nueva pagina
            page_start_in_list += self.page_size
        self._update_next_page(pcb)

    def _update_next_page(self, pcb):
        pcb.current_page = pcb.remaining_pages.pop(0) # Guardo numero de pagina actual y su desplazamiento en el PCB
        pcb.offset       = 0

    def _load_page(self, pcb, page_start_in_list, new_page):
        for instruction_number in range(self.page_size):
            try:
                new_page.content.append(pcb.program.instructions[page_start_in_list + instruction_number])
            except IndexError:
                break
            
    def _load_physical(self, memory, frame, page):
        direction = frame.start
        for instruction in page.content:
            memory[direction] = instruction
            direction += 1
    
    
    #########################
    # DESCARGA
    #########################
    def unload(self, pcb, physical_memory):
        pages_for = self.pages[pcb]
        for page in pages_for:
            self._unload_physical(page, physical_memory)
            self.free_numbers.append(page.number)
        del self.pages[pcb]
        
    def _unload_physical(self, page, memory):
        frame = self.page_table[page.number]
        for direction in range(frame.start, frame.end + 1):
            memory[direction] = None
        self.empty_frames.append(frame)
        del self.page_table[page.number]
        
    
    #########################
    # BUSQUEDA
    #########################
    def fetch(self, pcb, physical_memory):
        print 'Buscando en pagina: [' + str(pcb.current_page) + ', ' + str(pcb.offset) + ']'
        frame  = self.page_table[pcb.current_page]
        result = physical_memory[frame.start + pcb.offset]
        self._update_current_page(pcb)
        return result
    
    def _update_current_page(self, pcb):
        # Si esta al final de la pagina
        if pcb.offset == self.page_size - 1:
            # Si aun tiene paginas que recorrer
            if pcb.remaining_pages:
                self._update_next_page(pcb)
        else:
            pcb.offset += 1
        