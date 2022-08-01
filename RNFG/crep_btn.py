from tkinter import *
import tkinter as tk
import numpy as np
import crep_gui as cg
import crep_def as cd
import crep_np  as cn
import crep_logic as cl
import os

def nfg(parent_in):
    cn.get_entries_into_matrix(parent_in)
    print("NORMAL FORM")
    np.save(parent_in.prev_file, parent_in.matrix)
    parent_in.p1_br, parent_in.p2_br = cl.find_basic_BR(parent_in)
    cl.gen_BR_grid(parent_in, parent_in.p1_br, parent_in.p2_br, False)

def rnfg(parent_in):
    cn.get_entries_into_matrix(parent_in)
    print("REPEATED NORMAL FORM")
    np.save(parent_in.prev_file, parent_in.matrix)
    parent_in.p1_br, parent_in.p2_br = cl.find_basic_BR(parent_in)
    #cl.find_PD_grim_trigger(parent_in)
    cl.find_BRNE(parent_in)
    cl.find_folk_triggers(parent_in)
    
    cl.gen_BR_grid(parent_in, parent_in.p1_br, parent_in.p2_br, True)

def print_output(parent_in):
    cn.get_entries_into_matrix(parent_in)
    print("PRINT")
    print(parent_in.matrix)

def save_entries(parent_in, save_str, as_flag):
    cn.get_entries_into_matrix(parent_in)
    save_matrix_npy = ""
    if as_flag:
        save_matrix_npy = "./{}/{}_mx.npy".format(parent_in.save_folder, save_str)
        print("SAVE AS")
    else:
        save_matrix_npy = parent_in.saved_file
        print("SAVE")
    np.save(save_matrix_npy, parent_in.matrix)
    

def save_as(parent_in): # SAVE AS BUTTON
    save_str_entry = parent_in.save_as_str.get()
    if (save_str_entry.isspace() or not save_str_entry):
        print("Save As invalid file string")
    else:
        save_entries(parent_in, save_str_entry, True)


def load_entries(parent_in, load_str, as_flag):
    entry = np.load(parent_in.saved_file)
    if (as_flag):
        if(os.path.exists("./{}/{}_mx.npy".format(parent_in.save_folder, load_str))):
            entry = np.load("./{}/{}_mx.npy".format(parent_in.save_folder, load_str))
            print("LOAD AS")
        else:
            print("Load As file not found")
    else:
        entry = np.load(parent_in.saved_file)
        print("LOAD")

    if ((entry.shape[0] == parent_in.rows) and (entry.shape[1] == parent_in.cols)):
        parent_in.matrix = entry
        cn.fill_entries_from_matrix(parent_in, entry)
        
    else:
        print("Saved dimensions do not match - Cannot load")

def load_as(parent_in):
    load_str_entry = parent_in.load_as_str.get()
    if (load_str_entry.isspace() or not load_str_entry):
        print("Load As invalid file string")
    else:
        load_entries(parent_in, load_str_entry, True)

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