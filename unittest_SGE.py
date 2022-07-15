from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys
import csig_gui     as cg
import csig_btn     as cb
import csig_logic   as cl
import csig_def     as cd
import csig_np      as cn
import csig_unittests as cu
import signal_game  as sig
import os

gui_debug = True
matrix_show = False
try:
    if(sys.argv[1] == "t"):
        gui_debug = True
except:
    gui_debug = False


def main():
    parent = sig.SGE()
    if(gui_debug):
        run_gui(parent, 'D')
        return 0

    latest_index = cd.tests.index(cu.latest_testchar)
    spliced_tests = cd.tests[0:latest_index+1]
    test_matrix_arr = []
    test_nature_arr = []
    parent.debug_on = False
    parent.msg_on = False
    #mainGUItest(parent)
    gencheck = True
    for i in spliced_tests:
        if (not os.path.exists("./{}/test{}_mx.npy".format(parent.test_folder, i))):
            gencheck = False
        elif (not os.path.exists("./{}/test{}_nt.npy".format(parent.test_folder, i))):
            gencheck = False
    if not gencheck:
        print("Test matrix missing >> regenerating test matricies")
        cu.gen_test_matricies_file(parent, spliced_tests)

    load_test_matricies(parent, spliced_tests, test_matrix_arr, test_nature_arr)
    run_tests(parent, test_matrix_arr, test_nature_arr, latest_index)

def run_gui(parent_in, test_name):
    cg.create_spider_grid(parent_in, parent_in.root, parent_in.canvas)
    cg.label_grid(parent_in, parent_in.root, parent_in.canvas)
    test_matrix = np.zeros((4,2), dtype='i,i')
    cd.testGEN_functor_list[ord(test_name) - ord('A')](parent_in, test_name, test_matrix)
    cg.create_entry_boxes(parent_in, parent_in.root, parent_in.canvas)
    cg.gen_entry_buttons(parent_in, parent_in.root, parent_in.canvas)
    cg.draw_labels(parent_in, parent_in.root, parent_in.canvas)
    parent_in.root.mainloop()

def load_test_matricies(parent_in, tests_in, test_matrix_arr_in, test_nature_arr_in):
    for ti, test_char in enumerate(tests_in):
        test_matrix_arr_in.append(np.load("./{}/test{}_mx.npy".format(parent_in.test_folder, tests_in[ti])))
        test_nature_arr_in.append(np.load("./{}/test{}_nt.npy".format(parent_in.test_folder, tests_in[ti])))

def update_test_incr(incr_in, test_matrix_arr_in, test_nature_arr_in):
    incr_in = incr_in + 1
    rr_matrix_in = test_matrix_arr_in[incr_in]
    rr_nature_in = test_nature_arr_in[incr_in]
    return incr_in, rr_matrix_in, rr_nature_in

def run_tests(parent_in, test_matrix_arr_in, test_nature_arr_in, latest_index_in):
    incr = -1
    for i in range(latest_index_in+1):
        incr, rr_matrix, rr_nature = update_test_incr(incr, test_matrix_arr_in, test_nature_arr_in)
        if(matrix_show):print(rr_matrix)
        cu.test_functor_list[i](parent_in, rr_matrix, rr_nature)

if __name__ == '__main__':
    main()