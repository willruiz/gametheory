from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys
import crep_gui as cg
import crep_def as cd
import crep_np  as cn

def show_payoffs(parent_in, canvas_in, p1_br, p2_br):
    initH_offset = parent_in.top+parent_in.unit_height/2
    initW_offset = parent_in.left+parent_in.unit_width/2
    for i in range(parent_in.rows):
        for j in range(parent_in.cols):
            coord_x = initW_offset+(parent_in.unit_width*(j))
            coord_y = initH_offset+(parent_in.unit_height*(i))
            if (p1_br[i][j]):
                canvas_in.create_rectangle(coord_x-parent_in.offset-10, coord_y-10, 
                    coord_x-parent_in.offset+15, coord_y+10, fill= cd.mute_red)
            if (p2_br[i][j]):
                canvas_in.create_rectangle(coord_x+parent_in.offset-10, coord_y-10, 
                    coord_x+parent_in.offset+15, coord_y+10, fill= cd.mute_blue)
            canvas_in.create_text(coord_x-parent_in.offset, coord_y, 
                text=parent_in.matrix[i][j][0], fill="black", font=(cd.payoff_font))
            canvas_in.create_text(coord_x, coord_y, 
                text=',', fill="black", font=(cd.payoff_font))
            canvas_in.create_text(coord_x+parent_in.offset, coord_y, 
                text=parent_in.matrix[i][j][1], fill="black", font=(cd.payoff_font))


def find_basic_BR(parent_in): # return index coordinates of BRs
    # Player 1 (going down each column)
    match_p1 = np.zeros((parent_in.rows, parent_in.cols), dtype=bool)
    match_p2 = np.zeros((parent_in.rows, parent_in.cols), dtype=bool)
    for i in range(parent_in.matrix.shape[1]): # increment right
        local_br_val = (-1*sys.maxsize)-1
        curr_col = (parent_in.matrix[:,i])
        curr_col_indexed = [x[0] for x in curr_col]
        for j in range(parent_in.matrix.shape[0]): # scan down
            curr = parent_in.matrix[j][i][0]
            if (curr > local_br_val):
                local_br_val = curr
        comp_col = np.zeros((1, parent_in.rows))
        comp_col.fill(local_br_val)
        bool_col = (curr_col_indexed == comp_col)
        for x in range(match_p1.shape[0]):
            match_p1[x,i] = bool_col[0][x]
    
    # Player 2 (going right each row)
    for i in range(parent_in.matrix.shape[0]): # increment down
        local_br_val = (-1*sys.maxsize)-1
        curr_row = (parent_in.matrix[i,:])
        curr_row_indexed = [x[1] for x in curr_row]
        for j in range(parent_in.matrix.shape[1]): # scan right
            curr = parent_in.matrix[i][j][1]
            if (curr > local_br_val):
                local_br_val = curr
        #print("p2 br: ", local_br_val)
        comp_row = np.zeros((1, parent_in.cols))
        comp_row.fill(local_br_val)
        bool_row = (curr_row_indexed == comp_row)
        for x in range(match_p1.shape[0]):
            match_p2[i,x] = bool_row[0][x]
    return match_p1, match_p2

def gen_payoff_buttons(parent_in, root, canvas):
    quit_btn = tk.Button(root, text="Exit", bg = cd.lite_ornge, command=root.destroy,  width = int(parent_in.width/30), height = 3)
    canvas.create_window(parent_in.cenv, parent_in.bot+2 *(parent_in.height/20), window=quit_btn)

def gen_BR_grid(parent_in, match_p1, match_p2):
    subroot = tk.Tk()
    subcan = Canvas(subroot, bg='white')
    cg.create_matrix_grid(parent_in, subroot, subcan)
    cg.gen_labels(parent_in, subcan)
    show_payoffs(parent_in, subcan, match_p1, match_p2)
    gen_payoff_buttons(parent_in, subroot, subcan)
    subroot.mainloop()
