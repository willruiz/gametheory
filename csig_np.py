from tkinter import *
import tkinter as tk
import numpy as np



def import_matrix(self, matrix_in): # FOR CUSTOM MATRIX INPUT FOR TEST SUITE
        self.matrix_import = matrix_in
        self.matrix_import_bool = True

def fill_entries_from_matrix(self, matrix_in):
    for i, i_entry in enumerate(self.entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                # if (str(matrix_in[i][j][k]) == '0'):
                #     k_entry.set("")    
                # else:
                k_entry.set(str(matrix_in[i][j][k]))

def get_entries_into_matrix(self, matrix_in):
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