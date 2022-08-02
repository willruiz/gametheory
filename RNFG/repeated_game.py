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
        self.boxlen = 200
        self.boxoff = 150
        self.btnspace = 100
        
        self.width  = cols*self.boxlen+self.boxoff*2
        self.height = rows*self.boxlen+self.boxoff*2
        self.left   = self.boxoff
        self.right  = self.width - self.boxoff
        self.top    = self.boxoff
        self.bot    = self.height - self.boxoff
        self.true_height = self.height + self.btnspace

        self.cenv = self.width  * 0.5
        self.cenh = self.height * 0.5
    
        self.root = tk.Tk()
        self.canvas = Canvas(self.root, bg='white')

        self.entry_list = []
        self.matrix = np.zeros((self.rows,self.cols), dtype='i,i')
        self.matrix_import = np.zeros((1,1), dtype='i,i')
        self.matrix_import_bool = False

        self.fixed_folder = "fixed_saves"
        self.save_folder  = "user_saves"

        self.saved_npy = "saved_matrix.npy"
        self.saved_file = "{}/{}".format(self.fixed_folder, self.saved_npy)
        self.prev_npy  = "prev_matrix.npy" 
        self.prev_file = "{}/{}".format(self.fixed_folder, self.prev_npy)
        self.dim_save   = []
        for i in range(5):
            self.dim_save.append("{}/dim_matrix_{}.npy".format(self.fixed_folder, str(i)))
        
        self.square_bool = False
        self.square_dim = 2
        
        self.offset   = int(self.width/30)
        self.offset_h = int(self.width/30)
        self.poh = self.offset_h

        self.p1_br    = -1
        self.p2_br    = -1

        self.p1_index = 0
        self.p2_index = 1

        self.initH_offset = self.top  + self.boxlen/2
        self.initW_offset = self.left + self.boxlen/2

        self.delta_solution = 0.0
        self.delta_exists = False

def main():
    if   len(sys.argv) == 3:
        rows = int(sys.argv[1])
        cols = int(sys.argv[2])
    elif len(sys.argv) == 2:
        rows = int(sys.argv[1])
        cols = int(sys.argv[1])
    else:
        rows = 2
        cols = 2
    parent = RNFM(rows, cols)
    if (rows == cols):
        parent.square_bool = True
        parent.square_dim  = rows
    cn.init_np(parent)
    cg.create_matrix_grid(parent, parent.root, parent.canvas)
    cg.create_entry_boxes(parent, parent.canvas)
    cg.gen_labels(parent, parent.canvas)
    cg.gen_entry_buttons(parent, parent.root, parent.canvas)
    parent.root.mainloop()

if __name__ == '__main__':
    main()