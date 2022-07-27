from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys
import crep_gui as cg
import crep_def as cd
import crep_btn as cb

class RNFM:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.width  = cols*250+200
        self.height = rows*250+200
        self.left = self.width * 0.2
        self.right = self.width * 0.8
        self.top = self.height * 0.2
        self.bot = self.height * 0.8
        self.true_height = rows*250+250

        self.unit_width = (self.right-self.left)/cols
        self.unit_height = (self.bot-self.top)/rows
        self.cenv = self.width * 0.5
        self.cenh = self.height * 0.5
        self.root = tk.Tk()
        self.offset = 20
        self.canvas = Canvas(self.root, bg='white')
        self.entry_list = []
        self.matrix = np.zeros((self.rows,self.cols), dtype='i,i')
        self.saved_file = "saved_matrix.npy"
        self.saved_dim = "saved_dim.npy"
        self.prev_file = "prev_matrix.npy" 
        self.prev_dim = "prev_dim.npy"
        self.matrix_import = np.zeros((1,1), dtype='i,i')
        self.matrix_import_bool = False


    def fill_entries_from_matrix(self, matrix_in):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    if (str(matrix_in[i][j][k]) == '0'):
                        k_entry.set("")    
                    else:
                        k_entry.set(str(matrix_in[i][j][k]))


    def show_payoffs(self, canvas, p1_br, p2_br):
        initH_offset = self.top+self.unit_height/2
        initW_offset = self.left+self.unit_width/2
        for i in range(self.rows):
            for j in range(self.cols):
                coord_x = initW_offset+(self.unit_width*(j))
                coord_y = initH_offset+(self.unit_height*(i))
                if (p1_br[i][j]):
                    canvas.create_rectangle(coord_x-self.offset-10, coord_y-10, 
                        coord_x-self.offset+15, coord_y+10, fill='#FFCCCB')
                if (p2_br[i][j]):
                    canvas.create_rectangle(coord_x+self.offset-10, coord_y-10, 
                        coord_x+self.offset+15, coord_y+10, fill='#ADD8E6')
                canvas.create_text(coord_x-self.offset, coord_y, 
                    text=self.matrix[i][j][0], fill="black", font=(cd.payoff_font))
                canvas.create_text(coord_x, coord_y, 
                    text=',', fill="black", font=(cd.payoff_font))
                canvas.create_text(coord_x+self.offset, coord_y, 
                    text=self.matrix[i][j][1], fill="black", font=(cd.payoff_font))

    def import_matrix(self, matrix_in): # FOR CUSTOM MATRIX INPUT FOR TEST SUITE
        self.matrix_import = matrix_in
        self.matrix_import_bool = True


    def find_basic_BR(self): # return index coordinates of BRs
        # Player 1 (going down each column)
        match_p1 = np.zeros((self.rows, self.cols), dtype=bool)
        match_p2 = np.zeros((self.rows, self.cols), dtype=bool)
        for i in range(self.matrix.shape[1]): # increment right
            local_br_val = (-1*sys.maxsize)-1
            curr_col = (self.matrix[:,i])
            curr_col_indexed = [x[0] for x in curr_col]
            for j in range(self.matrix.shape[0]): # scan down
                curr = self.matrix[j][i][0]
                if (curr > local_br_val):
                    local_br_val = curr
            comp_col = np.zeros((1, self.rows))
            comp_col.fill(local_br_val)
            bool_col = (curr_col_indexed == comp_col)
            for x in range(match_p1.shape[0]):
                match_p1[x,i] = bool_col[0][x]
        
        # Player 2 (going right each row)
        for i in range(self.matrix.shape[0]): # increment down
            local_br_val = (-1*sys.maxsize)-1
            curr_row = (self.matrix[i,:])
            curr_row_indexed = [x[1] for x in curr_row]
            for j in range(self.matrix.shape[1]): # scan right
                curr = self.matrix[i][j][1]
                if (curr > local_br_val):
                    local_br_val = curr
            #print("p2 br: ", local_br_val)
            comp_row = np.zeros((1, self.cols))
            comp_row.fill(local_br_val)
            bool_row = (curr_row_indexed == comp_row)
            for x in range(match_p1.shape[0]):
                match_p2[i,x] = bool_row[0][x]
        return match_p1, match_p2

    def get_entries_into_matrix(self):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    str_input =k_entry.get()
                    input = 0
                    if (str_input == ''):
                        input = 0
                    else:
                        input = int(str_input)
                    self.matrix[i][j][k] = input

    def init_np(self):
        self.matrix = np.resize(self.matrix, (self.rows, self.cols))

    def gen_payoff_buttons(self, root, canvas):
        quit_btn = tk.Button(root, text="Exit", bg = cd.lite_ornge, command=root.destroy,  width = int(self.width/30), height = 3)
        canvas.create_window(self.cenv, self.bot+2 *(self.height/20), window=quit_btn)

    def gen_BR_grid(self, match_p1, match_p2):
        subroot = tk.Tk()
        subcan = Canvas(subroot, bg='white')
        cg.create_matrix_grid(self, subroot, subcan)
        self.show_payoffs(subcan, match_p1, match_p2)
        self.gen_payoff_buttons(subroot, subcan)
        subroot.mainloop()

def main():
    parent = RNFM(2, 2)
    parent.init_np()
    cg.create_matrix_grid(parent, parent.root, parent.canvas)
    cg.create_entry_boxes(parent, parent.canvas)
    cg.gen_entry_buttons(parent, parent.root, parent.canvas)
    parent.root.mainloop()

if __name__ == '__main__':
    main()