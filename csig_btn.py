from tkinter import *
import tkinter as tk
import numpy as np
import csig_np as cn

def enter_saved(self):
        entry = np.load(self.saved_file)
        if (entry.shape == (4,2)):
            self.matrix = entry
            cn.fill_entries_from_matrix(self, entry)
            print("MATRIX LOADED")
        else:
            print("Saved dimensions is not a signal game - Cannot load")
        nature = np.load(self.nature_file)
        if (nature.shape == (1,2)):
            self.nature_mat = nature
            #print("checkC:",nature)
            cn.fill_nature_entry_from_Natrix(self, nature)
            print("NATURE LOADED")
        else:
            print("Saved nature is not compatible - Cannot load")


def transfer_entries_to_saved(self):
    cn.get_entries_into_matrix(self, self.matrix)
    cn.get_nature_entries_into_Natrix(self, self.nature_mat)
    np.save(self.saved_file, self.matrix)
    np.save(self.nature_file, self.nature_mat)
    print(self.nature_mat)
    print("SAVED")

def submit(self):
    cn.get_entries_into_matrix(self, self.matrix)
    cn.get_nature_entries_into_Natrix(self, self.nature_mat)
    print(self.matrix)
    print("SUBMIT")
    np.save(self.prev_file, self.matrix)
    np.save(self.nature_prev, self.nature_mat)

def reset(self):
    for i, i_entry in enumerate(self.entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                k_entry.set("")
                self.matrix[i][j][k] = 0
    for i, i_entry in enumerate(self.nature_entry):
        i_entry.set("")
    # self.nature_mat[0][0] = 0.5
    # self.nature_mat[0][1] = 0.5

    print("RESET")
    np.save(self.prev_file, self.matrix)
    np.save(self.nature_prev, self.nature_mat)

def quit_game(self, root_in):
    cn.get_entries_into_matrix(self, self.matrix)
    cn.get_nature_entries_into_Natrix(self, self.nature_mat)
    print(self.matrix)
    np.save(self.prev_file, self.matrix)
    np.save(self.nature_prev, self.nature_mat)
    print("EXIT")
    root_in.destroy()