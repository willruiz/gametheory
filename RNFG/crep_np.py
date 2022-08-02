import numpy as np

def fill_entries_from_matrix(parent_in, matrix_in):
    zero_bool = True
    for i, i_entry in enumerate(parent_in.entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                k_entry.set(str(matrix_in[i][j][k]))
                if (matrix_in[i][j][k] != 0):
                    zero_bool = False
    if zero_bool:
        for i, i_entry in enumerate(parent_in.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    k_entry.set("")

def import_matrix(parent_in, matrix_in): # FOR CUSTOM MATRIX INPUT FOR TEST SUITE
    parent_in.matrix_import = matrix_in
    parent_in.matrix_import_bool = True

def get_entries_into_matrix(parent_in):
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

def init_np(parent_in):
    parent_in.matrix = np.resize(parent_in.matrix, (parent_in.rows, parent_in.cols))