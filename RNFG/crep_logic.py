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
    # super duper ineffienct nested for-looping, 
    # use numpy functions later for optimization
    parent_in.initH_offset = parent_in.top+parent_in.unit_height/2
    parent_in.initW_offset = parent_in.left+parent_in.unit_width/2
    digscA = 0
    digscB = 0
    for i in range(parent_in.rows):
        for j in range(parent_in.cols):
            p1_font = ""
            p2_font = ""
            coord_x = parent_in.initW_offset+(parent_in.unit_width*(j))
            coord_y = parent_in.initH_offset+(parent_in.unit_height*(i))
            if (p1_br[i][j]):
                if (parent_in.matrix[i][j][parent_in.p1_index] >= 100):
                    digscA = 2
                elif (parent_in.matrix[i][j][parent_in.p1_index] >= 10):
                    digscA = 1

                canvas_in.create_rectangle(
                    coord_x-parent_in.poh-parent_in.poh*0.5-digscA*parent_in.poh*0.55, coord_y-parent_in.poh*0.6, 
                    coord_x-parent_in.poh+parent_in.poh*0.5+digscA*parent_in.poh*0.15, coord_y+parent_in.poh*0.6, 
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
                    coord_x+parent_in.poh-parent_in.poh*0.5-digscB*parent_in.poh*0.15, coord_y-parent_in.poh*0.6, 
                    coord_x+parent_in.poh+parent_in.poh*0.5+digscB*parent_in.poh*0.55, coord_y+parent_in.poh*0.6, 
                    fill= cd.mute_blue)
                p2_font = cd.paybold_font
            else:
                p2_font = cd.payoff_font

            # Find NEs
            if (p1_br[i][j] and p2_br[i][j]):
                canvas_in.create_rectangle(
                    coord_x-3.5*parent_in.poh, coord_y-parent_in.poh*1.5, 
                    coord_x+3.5*parent_in.poh, coord_y+parent_in.poh*1.5, 
                    outline= "yellow", width = 3)
            canvas_in.create_text(coord_x-parent_in.poh-digscB*parent_in.poh*0.2, coord_y, 
                    text=parent_in.matrix[i][j][0], fill="black", font=p1_font)
            canvas_in.create_text(coord_x, coord_y, 
                text=',', fill="black", font=(cd.payoff_font))
            canvas_in.create_text(coord_x+parent_in.poh+digscB*parent_in.poh*0.2, coord_y, 
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

def find_BRNE(parent_in): 
    # super duper ineffienct nested for-looping, 
    # use numpy functions later for optimization
    max_index = [-1,-1]
    p1_max_val   =  0
    p2_max_val   =  0
    for i, ie in enumerate(parent_in.matrix):
        for j, je in enumerate(ie):
            if (parent_in.p1_br[i][j] and parent_in.p2_br[i][j] and 
                (je[parent_in.p1_index] > p1_max_val) and 
                (je[parent_in.p2_index] > p2_max_val)):
                p1_max_val = je[parent_in.p1_index]
                p2_max_val = je[parent_in.p2_index]
                max_index = (i,j) # CAUTION: (i == p1, j == p2)
    parent_in.BRNE = max_index
    print("BRNE:",parent_in.BRNE)


def find_folk_triggers(parent_in):
    """
    1. Nash equlibrium
    2. Max deviation
    3. Alternative Strictly better outcome for both players (cooperative eq)
    """
    """
    Process:
    1. Find BR Nash Eq
    2. Find all outcomes with strictly better outcomes than the NE
    3. Do a temporal discounting factor calculation for each Folk Eq
    """
    parent_in.folk_arr = []
    parent_in.folk_indexes = []
    br_x = parent_in.BRNE[parent_in.p1_index]
    br_y = parent_in.BRNE[parent_in.p2_index]
    p1_br_val = parent_in.matrix[br_x][br_y][parent_in.p1_index]
    p2_br_val = parent_in.matrix[br_x][br_y][parent_in.p2_index]
    for i, ie in enumerate(parent_in.matrix):
        for j, je in enumerate(ie):
            if (je[parent_in.p1_index] > p1_br_val and
                je[parent_in.p2_index] > p2_br_val):
                    p1_delta, p2_delta = find_discount_shift(parent_in, i, j)
                    if (p1_delta and p2_delta):
                        parent_in.folk_arr.append((p1_delta, p2_delta))
                        parent_in.folk_indexes.append((i,j))
                    else:
                        print("Deltas do not exist for coordinates [{},{}]".format(str(i), str(j)))

def find_discount_shift(parent_in, i_in, j_in):
    c_p1 = i_in
    c_p2 = j_in

    d_p1 = parent_in.BRNE[parent_in.p1_index]
    d_p2 = parent_in.BRNE[parent_in.p2_index]

    c_eq_p1 = parent_in.matrix[c_p1][c_p2][parent_in.p1_index]
    atck_p1 = parent_in.matrix[d_p1][c_p2][parent_in.p1_index]
    d_eq_p1 = parent_in.matrix[d_p1][d_p2][parent_in.p1_index]

    p1_delta = symbols('d1')
    exprC1 = c_eq_p1/(1-p1_delta)
    exprD1 = atck_p1 + (d_eq_p1*p1_delta)/(1-p1_delta)
    
    p1_delta_solution = solve(Eq(exprC1, exprD1), p1_delta)
    if(bool(p1_delta_solution )):
        p1_delta_solution = round(float(p1_delta_solution[0]),2)
    else:
        print("[Undefined p1 delta solution]")

    c_eq_p2 = parent_in.matrix[c_p1][c_p2][parent_in.p2_index]
    atck_p2 = parent_in.matrix[c_p1][d_p2][parent_in.p2_index]
    d_eq_p2 = parent_in.matrix[d_p1][d_p2][parent_in.p2_index]

    p2_delta = symbols('d2')
    exprC2 = c_eq_p2/(1-p2_delta)
    exprD2 = atck_p2 + (d_eq_p2*p2_delta)/(1-p2_delta)

    p2_delta_solution = solve(Eq(exprC2, exprD2), p2_delta)
    if(bool(p2_delta_solution )):
        p2_delta_solution = round(float(p2_delta_solution[0]),2)
    else:
        print("[Undefined p2 delta solution]")

    return p1_delta_solution, p2_delta_solution

def draw_alt_paretos(parent_in, canvas_in, i_in, j_in):
    coord_x = parent_in.initW_offset+(parent_in.unit_width*(j_in))
    coord_y = parent_in.initH_offset+(parent_in.unit_height*(i_in))
    canvas_in.create_rectangle(
        coord_x-3.5*parent_in.poh, coord_y-parent_in.poh*1.5, 
        coord_x+3.5*parent_in.poh, coord_y+parent_in.poh*1.5, 
        outline= "lime green", width = 2)

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

    ceq  = parent_in.matrix[c_p1][c_p2][parent_in.p1_index]
    atck = parent_in.matrix[d_p1][c_p2][parent_in.p1_index]
    deq  = parent_in.matrix[d_p1][d_p2][parent_in.p1_index]

    delta = symbols('d')
    exprC = ceq/(1-delta)
    exprD = atck + (deq*delta)/(1-delta)
    #print(exprC)    
    #print(exprD)
    
    parent_in.delta_solution = solve(Eq(exprC, exprD), delta)
    if(bool(parent_in.delta_solution)):
        parent_in.delta_solution = round(float(parent_in.delta_solution[0]),2)
        parent_in.delta_exists = True
    else:
        print("[Undefined delta solution]")

def draw_delta_label(parent_in, subcan_in, i_in, j_in, p1_delta, p2_delta):
    coord_x1 = parent_in.initW_offset+(parent_in.unit_width*(j_in))
    coord_x2 = parent_in.initW_offset+(parent_in.unit_width*(parent_in.BRNE[0]))
    coord_y1 = parent_in.initH_offset+(parent_in.unit_height*(parent_in.BRNE[1]))
    coord_y2 = parent_in.initH_offset+(parent_in.unit_height*(i_in))
    # P1-delta
    subcan_in.create_text(
        coord_x1, coord_y1+parent_in.offset*1.5, 
            text = "d1: "+str(p1_delta), fill="green", font=(cd.delta_font))
    # P2-delta
    subcan_in.create_text(
        coord_x2, coord_y2+parent_in.offset*1.5, 
            text = "d2: "+str(p2_delta), fill="green", font=(cd.delta_font))


def gen_BR_grid(parent_in, match_p1, match_p2, rep_bool):
    subroot = tk.Tk()
    subcan = Canvas(subroot, bg='white')
    cg.create_matrix_grid(parent_in, subroot, subcan)
    cg.gen_labels(parent_in, subcan)
    show_payoffs(parent_in, subcan, match_p1, match_p2)
    
    if (rep_bool):
        for a, ae in enumerate(parent_in.folk_arr):
            i = parent_in.folk_indexes[a][0]
            j = parent_in.folk_indexes[a][1]
            p1_delta = ae[0]
            p2_delta = ae[1]
            draw_alt_paretos(parent_in, subcan, i, j)
            draw_delta_label(parent_in, subcan, i, j, p1_delta, p2_delta)
            

        #subcan.create_text(parent_in.cenh, parent_in.top-100, text = "delta: "+str(parent_in.delta_solution), font=(cd.label_font))
    gen_payoff_buttons(parent_in, subroot, subcan)
    subroot.mainloop()

def gen_payoff_buttons(parent_in, root, canvas):
    quit_btn = tk.Button(root, text="Exit", bg = cd.lite_ornge, command=root.destroy,  width = 5*int(parent_in.unit_width/20), height = 5)
    canvas.create_window(parent_in.cenv, parent_in.bot + 2 *(parent_in.unit_height/4), window=quit_btn)


