from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys
import crep_gui as cg
import crep_def as cd
import crep_np  as cn
from sympy import symbols, Eq, solve

def show_payoffs(parent_in, canvas_in, p1_br, p2_br):
    initH_offset = parent_in.top+parent_in.unit_height/2
    initW_offset = parent_in.left+parent_in.unit_width/2
    poh = parent_in.offset_h
    digscA = 0
    digscB = 0
    for i in range(parent_in.rows):
        for j in range(parent_in.cols):
            p1_font = ""
            p2_font = ""
            coord_x = initW_offset+(parent_in.unit_width*(j))
            coord_y = initH_offset+(parent_in.unit_height*(i))
            if (p1_br[i][j]):
                if (parent_in.matrix[i][j][parent_in.p1_index] >= 100):
                    digscA = 2
                elif (parent_in.matrix[i][j][parent_in.p1_index] >= 10):
                    digscA = 1

                canvas_in.create_rectangle(
                    coord_x-poh-poh*0.5-digscA*poh*0.55, coord_y-poh*0.6, 
                    coord_x-poh+poh*0.5+digscA*poh*0.15, coord_y+poh*0.6, 
                    fill= cd.mute_red)
                p1_font = cd.paybold_font
            else:
                p1_font = cd.payoff_font
            if (p2_br[i][j]):
                
                if (parent_in.matrix[i][j][parent_in.p2_index] >= 100):
                    digscB = 2
                elif (parent_in.matrix[i][j][parent_in.p2_index] >= 10):
                    digscB = 1
                canvas_in.create_rectangle(
                    coord_x+poh-poh*0.5-digscB*poh*0.15, coord_y-poh*0.6, 
                    coord_x+poh+poh*0.5+digscB*poh*0.55, coord_y+poh*0.6, 
                    fill= cd.mute_blue)
                p2_font = cd.paybold_font
            else:
                p2_font = cd.payoff_font
            canvas_in.create_text(coord_x-poh-digscB*poh*0.2, coord_y, 
                text=parent_in.matrix[i][j][0], fill="black", font=p1_font)
            canvas_in.create_text(coord_x, coord_y, 
                text=',', fill="black", font=(cd.payoff_font))
            canvas_in.create_text(coord_x+poh+digscB*poh*0.2, coord_y, 
                text=parent_in.matrix[i][j][1], fill="black", font=p2_font)


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

def gen_BR_grid(parent_in, match_p1, match_p2, rep_bool):
    subroot = tk.Tk()
    subcan = Canvas(subroot, bg='white')
    cg.create_matrix_grid(parent_in, subroot, subcan)
    cg.gen_labels(parent_in, subcan)
    show_payoffs(parent_in, subcan, match_p1, match_p2)
    if (rep_bool):
        subcan.create_text(parent_in.cenh, parent_in.top-100, text = "delta: "+str(parent_in.delta_solution), font=(cd.label_font))
    gen_payoff_buttons(parent_in, subroot, subcan)
    subroot.mainloop()

# def inifinite_series_sum(payoff, discount):
#     return payoff/(1-discount)

def find_PD_grim_trigger(parent_in):
    # Assume PD game
    """
    1. Cooperative eq (C,C): [0,0]
    2. One-time gain (D,C):  [1,0]
    3. Defective eq (D,D):   [1,1]
    """
    c_p1 = 0
    c_p2 = 0
    d_p1 = 1
    d_p2 = 1

    ceq    = parent_in.matrix[c_p1][c_p2][parent_in.p1_index]
    atck = parent_in.matrix[d_p1][c_p2][parent_in.p1_index]
    deq    = parent_in.matrix[d_p1][d_p2][parent_in.p1_index]

    delta = symbols('d')
    exprC = ceq/(1-delta)
    exprD = atck + (deq*delta)/(1-delta)
    print(exprC)    
    print(exprD)
    parent_in.delta_solution = 0.0
    parent_in.delta_exists = False
    parent_in.delta_solution = solve(Eq(exprC, exprD), delta)
    if(bool(parent_in.delta_solution)):
        parent_in.delta_solution = round(float(parent_in.delta_solution[0]),2)
        parent_in.delta_exists = True
    else:
        print("[Undefined delta solution]")
       

def gen_payoff_buttons(parent_in, root, canvas):
    quit_btn = tk.Button(root, text="Exit", bg = cd.lite_ornge, command=root.destroy,  width = int(parent_in.width/30), height = 3)
    canvas.create_window(parent_in.cenv, parent_in.bot+2 *(parent_in.height/20), window=quit_btn)


