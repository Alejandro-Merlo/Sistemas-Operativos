'''
Created on 02/12/2013

@author: Alejandro
'''
from disk.algorithm import Algorithm
from system.program import Program

class INode(Algorithm):
    
    def __init__(self, size):
        Algorithm.__init__(self, size)
        self.nodes      = {} # El mapa de nodos, algunos nodos son indices y otros contienen la direccion en disco del programa
        self.inodes     = {} # El mapa de inodos segun el nombre del programa
        self.free_nodes = [] # Los numeros de nodo libres
        self._set_up_free_nodes(size)
        
    def _set_up_free_nodes(self, size):
        for number in range(size, -1, -1):
            self.free_nodes.append(number)        
        
    def save(self, program, sectors):
        program_size = len(program.instructions)
        if program_size <= len(self.free_nodes):
            inode_entry               = self.free_nodes.pop()
            indexes                   = []
            self.inodes[program.name] = inode_entry
            for instruction in program.instructions:
                next_entry = self.free_nodes.pop()
                self.nodes[next_entry] = next_entry
                sectors[next_entry]    = instruction
                indexes.append(next_entry)
            self.nodes[inode_entry]   = indexes
        else:
            print 'No hay espacio en disco'
        
    def show(self):
        for program_name, inode in self.inodes.iteritems():
            print program_name + ' -> Nodos: [ ' + self._show_indexes(self.nodes[inode]) + ']'
            
    def _show_indexes(self, indexes):
        result = ''
        for i in indexes:
            result = result + str(i) + ' '
        return result
        
    def fetch(self, p_name, sectors):
        program = Program(p_name, [])
        for index in self.nodes[self.inodes[p_name]]:
            program.instructions.append(sectors[self.nodes[index]])
        return program
    
    def programs_saved(self):
        return len(self.inodes.keys())