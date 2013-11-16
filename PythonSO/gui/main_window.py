# -*- coding: utf-8 -*-
'''
Created on 14/11/2013

@author: Alejandro
'''
from PyQt4 import QtCore, QtGui
from scheduler.fifo import FIFO
from system.kernel import Kernel
from memory.mvt import MVT
from memory.mmu import MMU
from memory.first_fit import FirstFit
from memory.worst_fit import WorstFit
from memory.best_fit import BestFit

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()
        
        
    def init_ui(self):
        self.setObjectName(QtCore.QString.fromUtf8('main_window'))
        self.center()
        self.resize(640, 480)
        self.setWindowTitle('Simulador de un Sistema Operativo')
        self.init_central_widget()
        
    def center(self):
        rectangle    = self.frameGeometry()
        center_point = QtGui.QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())
        
    def init_central_widget(self):
        self.central_widget = QtGui.QWidget()
        self.form_layout    = QtGui.QFormLayout()
        options_label       = QtGui.QLabel(self.central_widget)
        options_label.move(10, 0)
        options_label.setText('Opciones')
        
        dispatcher_label = QtGui.QLabel(self.central_widget)
        dispatcher_label.move(10, 20)
        dispatcher_label.setText('Planificador de corto plazo')
        
        self.combo = QtGui.QToolButton(self.central_widget)
        self.combo.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.combo.setMenu(QtGui.QMenu(self.combo))
        
        fifo_opt = QtGui.QWidgetAction(self.combo)
        fifo_opt.setText('FSFC')
        #fifo_opt.triggered.connect(lambda: self.set_dispatcher_algorithm(FIFO()))
        rr_opt = QtGui.QWidgetAction(self.combo)
        rr_opt.setText('Round Robin con prioridad')
        
        self.combo.move(10, 45)
        self.combo.menu().addAction(fifo_opt)
        self.combo.menu().addAction(rr_opt)
        self.combo.menu().setDefaultAction(fifo_opt)
        self.combo.setText(fifo_opt.text())
        
        memory_label = QtGui.QLabel(self.central_widget)
        memory_label.move(10, 80)
        memory_label.setText('Memoria')
        
        size_label = QtGui.QLabel(self.central_widget)
        size_label.move(10, 102)
        size_label.setText('Tamanio:')
        spin_box = QtGui.QSpinBox(self.central_widget)
        spin_box.move(65, 100)
        #spin_box.connect(lambda: self.set_memory_size(50))
        
        self.opt_group = QtGui.QButtonGroup(self.central_widget)
        radio1 = QtGui.QRadioButton('MVT con primer ajuste', self.central_widget)
        radio1.move(10, 125)
        #radio1.clicked.connect(lambda: self.set_memory_algorithm(MVT(32, FirstFit())))
        radio2 = QtGui.QRadioButton('MVT con mejor ajuste', self.central_widget)
        radio2.move(10, 145)
        #radio2.clicked.connect(lambda: self.set_memory_algorithm(MVT(32, FirstFit())))
        radio3 = QtGui.QRadioButton('MVT con peor ajuste', self.central_widget)
        radio3.move(10, 165)
        #radio3.clicked.connect(lambda: self.set_memory_algorithm(MVT(32, FirstFit())))
        self.opt_group.addButton(radio1)
        self.opt_group.addButton(radio2)
        self.opt_group.addButton(radio3)
        
        self.init_buttons()
        self.setCentralWidget(self.central_widget)

    def init_buttons(self):
        start_button = QtGui.QPushButton('Empezar', self.central_widget)
        start_button.move(10, 300)
        quit_button  = QtGui.QPushButton('Salir', self.central_widget)
        quit_button.move(90, 300)
        
        start_button.resize(quit_button.sizeHint())
        #start_button.clicked.connect(lambda: self.run_application())
        quit_button.resize(quit_button.sizeHint())
        quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        #hbox = QtGui.QHBoxLayout()
        #hbox.addStretch(1)
        #hbox.addWidget(start_button)
        #hbox.addWidget(quit_button)
        
        #vbox = QtGui.QVBoxLayout()
        #vbox.addStretch(1)
        #vbox.addLayout(hbox)
        
    def run_application(self):
        self.application.start()