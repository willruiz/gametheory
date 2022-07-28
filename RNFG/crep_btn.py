from tkinter import *
import tkinter as tk
import numpy as np
import crep_gui as cg
import crep_def as cd
import crep_np  as cn
import crep_logic as cl

def submit(parent_in):
    for i, i_entry in enumerate(parent_in.entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                str_input =k_entry.get()
                input = 0
                if (str_input == ''):
                    input = 0
                else:
                    input = int(str_input)
                parent_in.matrix[i][j][k] = input
                #print(matrix)
    print("SUBMIT")
    np.save(parent_in.prev_file, parent_in.matrix)

    p1_br, p2_br = cl.find_basic_BR(parent_in)
    cl.gen_BR_grid(parent_in, p1_br, p2_br)

def save_entries(parent_in):
    cn.get_entries_into_matrix(parent_in)
    np.save(parent_in.saved_file, parent_in.matrix)
    print("SAVE")


def load_entries(parent_in):
    entry = np.load(parent_in.saved_file)
    if ((entry.shape[0] == parent_in.rows) and (entry.shape[1] == parent_in.cols)):
        parent_in.matrix = entry
        cn.fill_entries_from_matrix(parent_in, entry)
        print("LOAD")
    else:
        print("Saved dimensions do not match - Cannot load")

def reset(parent_in):
    for i, i_entry in enumerate(parent_in.entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                k_entry.set("")
                parent_in.matrix[i][j][k] = 0
    print("RESET")
    np.save(parent_in.prev_file, parent_in.matrix)

def quit_game(parent_in):
    cn.get_entries_into_matrix(parent_in)
    np.save(parent_in.prev_file, parent_in.matrix)
    print("EXIT")
    parent_in.root.destroy()