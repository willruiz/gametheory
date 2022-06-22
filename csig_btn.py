from tkinter import *
import tkinter as tk
import numpy as np
import csig_np as cn

def enter_saved(self):
        entry = np.load(self.saved_file)
        if ((entry.shape[0] == self.rows) and (entry.shape[1] == self.cols)):
            self.matrix = entry
            cn.fill_entries_from_matrix(self, entry)
            print("LOADED")
        else:
            print("Saved dimensions do not match - Cannot load")

def transfer_entries_to_saved(self):
    cn.get_entries_into_matrix(self, self.matrix)
    np.save(self.saved_file, self.matrix)
    print("SAVED")

def submit(self):
    cn.get_entries_into_matrix(self, self.matrix)
    print(self.matrix)
    print("SUBMIT")
    np.save(self.prev_file, self.matrix)
    print("self.p2_bot_choice:",self.p2_bot_choice)
    print("self.top_branch:",self.top_branch)

def reset(self):
    for i, i_entry in enumerate(self.entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                k_entry.set("")
                self.matrix[i][j][k] = 0
    self.nature_entry = [0,0]
    print("RESET")
    np.save(self.prev_file, self.matrix)

def quit_game(self, root_in):
    cn.get_entries_into_matrix(self, self.matrix)
    print(self.matrix)
    np.save(self.prev_file, self.matrix)
    print("EXIT")
    root_in.destroy()