from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys
import crep_gui as cg
import crep_def as cd
import crep_btn as cb
import crep_np  as cn
import crep_logic as cl

class RNFM:
    def __init__(self, rows, cols):
        self.rows   = rows
        self.cols   = cols
        self.width  = cols*250+200
        self.height = rows*250+200
        self.left   = self.width * 0.2
        self.right  = self.width * 0.8
        self.top    = self.height * 0.2
        self.bot    = self.height * 0.8
        self.true_height = rows*250+300

        self.unit_width  = (self.right-self.left)/cols
        self.unit_height = (self.bot-self.top)/rows
        self.cenv = self.width  * 0.5
        self.cenh = self.height * 0.5
    
        self.root = tk.Tk()
        self.canvas = Canvas(self.root, bg='white')

        self.entry_list = []
        self.matrix = np.zeros((self.rows,self.cols), dtype='i,i')
        self.matrix_import = np.zeros((1,1), dtype='i,i')
        self.matrix_import_bool = False

        self.saved_file = "saved_matrix.npy"
        self.saved_dim  = "saved_dim.npy"
        self.prev_file  = "prev_matrix.npy" 
        self.prev_dim   = "prev_dim.npy"
        
        self.offset   = int(self.width/30)
        self.offset_h = int(self.width/30)
        self.poh = self.offset_h

        self.p1_br    = 0
        self.p2_br    = 0

        self.p1_index = 0
        self.p2_index = 1

        self.initH_offset = self.top  + self.unit_height/2
        self.initW_offset = self.left + self.unit_width/2

        self.delta_solution = 0.0
        self.delta_exists = False

def main():
    parent = RNFM(2, 2)
    cn.init_np(parent)
    cg.create_matrix_grid(parent, parent.root, parent.canvas)
    cg.create_entry_boxes(parent, parent.canvas)
    cg.gen_labels(parent, parent.canvas)
    cg.gen_entry_buttons(parent, parent.root, parent.canvas)
    parent.root.mainloop()

if __name__ == '__main__':
    main()