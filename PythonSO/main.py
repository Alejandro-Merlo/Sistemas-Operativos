'''
Created on 14/11/2013

@author: Alejandro
'''
from gui.main_window import MainWindow
from system.shell import Shell
from system.kernel import Kernel
from memory.mmu import MMU
from memory.pagination import Pagination
from memory.mvt import MVT
from scheduler.prioritary_round_robin import PrioritaryRoundRobin
#from memory.first_fit import FirstFit
#from scheduler.fifo import FIFO
from memory.best_fit import BestFit
#from memory.worst_fit import WorstFit
from time import sleep

import sys
from PyQt4 import QtGui

def main():
    #app = QtGui.QApplication(sys.argv)
    
    #window = MainWindow()
    #window.show()
    
    #sys.exit(app.exec_())
    
    memory_size = 32
    page_size   = 4
    quantum     = 3
    priorities  = 5
    aging       = 3
    
    kernel = Kernel(PrioritaryRoundRobin(quantum, priorities, aging), MMU(Pagination(memory_size, page_size), memory_size))
    #kernel = Kernel(PrioritaryRoundRobin(quantum, priorities, aging), MMU(MVT(memory_size, BestFit()), memory_size))
    shell  = Shell(kernel)
    shell.start()
    
    while True:
        if kernel.cpu.assigned_pcb is None:
            kernel.run_next_process()
            sleep(1)

if __name__ == '__main__':
    main()