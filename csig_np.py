from tkinter import *
import tkinter as tk
import numpy as np

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def import_matrix(self, matrix_in, nature_in): # FOR CUSTOM MATRIX INPUT FOR TEST SUITE
    self.matrix_import = matrix_in
    self.nature_import = nature_in
    self.matrix = matrix_in
    self.nature_mat = nature_in
    self.matrix_import_bool = True

def get_entries_into_matrix(self, matrix_in):
    assert(matrix_in.shape == (4,2) or matrix_in.shape == (4,2,2))
    for i, i_entry in enumerate(self.entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                str_input =k_entry.get()
                input = 0
                if (str_input == ''):
                    input = 0
                else:
                    input = int(str_input)
                matrix_in[i][j][k] = input

def fill_entries_from_matrix(self, matrix_in):
    assert(matrix_in.shape == (4,2) or matrix_in.shape == (4,2,2))
    for i, i_entry in enumerate(self.entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                k_entry.set(str(matrix_in[i][j][k]))

def get_nature_entries_into_Natrix(self, matrix_in):
    assert(matrix_in.shape == (1,2))
    for i, i_entry in enumerate(self.nature_entry):
        str_input = i_entry.get()
        input = 0.0 
        if (str_input == ""):
            input = 0.5
        elif (not isfloat(str_input)):
            print("Non-numerical nature probability entered")
            break
        else:
            input = float(str_input)
        matrix_in[0][i] = input
    checksum = np.sum(matrix_in)
    #print("checksum:",checksum)
    # if checksum != 1.0:
    #     print("Nature probabilities must equal 1.0")
    #     assert(False)
    

def fill_nature_entry_from_Natrix(self, matrix_in): # 1x2 matrix
    for i, i_entry in enumerate(self.nature_entry):
        i_entry.set(str(matrix_in[0][i]))

def fill_nature_half(matrix_in):
    assert(matrix_in.shape == (1,2))
    for i, i_entry in enumerate(matrix_in[0]):
        matrix_in[0][i] = 0.5

def save_test_matrix(self, save_str):
    test_matrix_npy = "./{}/{}_mx.npy".format(self.test_folder, save_str)
    test_nature_npy = "./{}/{}_nt.npy".format(self.test_folder, save_str)
    np.save(test_matrix_npy, self.matrix)
    np.save(test_nature_npy, self.nature_mat)

# def gen_test_file(self, test_str):
    