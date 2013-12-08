'''
Created on 02/12/2013

@author: Alejandro
'''
from disk.algorithm import Algorithm

class INode(Algorithm):
    
    def __init__(self, size):
        Algorithm.__init__(self, size)
        self.nodes      = {} # El mapa de nodos, algunos nodos son indices y otros contienen la direccion en disco del programa
        self.inodes     = {} # El mapa de inodos segun el nombre del programa
        self.free_nodes = [] # Los numeros de nodo libres
        self._set_up_free_nodes(size)
        
    def _set_up_free_nodes(self, size):
        for number in range(size):
            self.free_nodes.append(number)        
        
    def save(self, program, sectors):
        program_size = len(program.instructions)
        if program_size <= len(self.free_nodes):
            inode_entry = self.free_nodes.pop()
            indexes     = []
            self.inodes[program.name] = inode_entry
            self.nodes[inode_entry]   = indexes
            for instruction in program.instructions:
                next_entry = self.free_nodes.pop(0)
                self.nodes[next_entry] = next_entry
                sectors[next_entry]    = instruction
                indexes.append(next_entry)
        else:
            print 'No hay espacio en disco'
        
    def show(self):
        for program_name, indexes in self.inodes.iteritems():
            print program_name + ' -> [' + self._show_indexes(indexes) + ']'
            
    def _show_indexes(self, indexes):
        result = ''
        for i in indexes:
            result + i + ', '
        
    def fetch(self, p_name, sectors):
        None