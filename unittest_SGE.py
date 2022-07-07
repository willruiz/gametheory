from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys
import csig_gui     as cg
import csig_btn     as cb
import csig_logic   as cl
import csig_def     as cd
import csig_np     as cn
import signal_game  as sig


def mainGUItest(parent_in):
    cg.create_spider_grid(parent_in, parent_in.root, parent_in.canvas)
    cg.label_grid(parent_in, parent_in.root, parent_in.canvas)
    matrix_A = np.zeros((4,2), dtype='i,i')
    incrA = 0
    for i, i_entry in enumerate(matrix_A):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                matrix_A[i][j][k] = incrA
                incrA = incrA + 1
    cn.import_matrix(parent_in, matrix_A)
    cg.create_entry_boxes(parent_in, parent_in.root, parent_in.canvas)
    cg.gen_entry_buttons(parent_in, parent_in.root, parent_in.canvas)
    cg.draw_labels(parent_in, parent_in.root, parent_in.canvas)
    parent_in.root.mainloop()

def testA_sep(parent_in):
    matrix_A = np.zeros((4,2), dtype='i,i')
    incrA = 0
    for i, i_entry in enumerate(matrix_A):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                matrix_A[i][j][k] = incrA
                incrA = incrA + 1
    cn.import_matrix(parent_in, matrix_A)
    cl.seperating_eq(parent_in, matrix_A, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p2_top_alt    == 1)
    assert(parent_in.p2_bot_alt    == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.seperating_eq(parent_in, matrix_A, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p2_top_alt    == 1)
    assert(parent_in.p2_bot_alt    == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == False)

    print("TestA_sep: SUCCESS")


def main():
    parent = sig.SGE()
    #mainGUItest(parent)
    testA_sep(parent)

if __name__ == '__main__':
    main()