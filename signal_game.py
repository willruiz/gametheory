from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys
import csig_gui
import csig_np
import csig_btn
import csig_sep

STR_HID = 0
STR_REV = 1
WEK_HID = 0
WEK_REV = 1

class SGE:
    def __init__(self):
        ## Dimensions
        self.rows = 4
        self.cols = 2
        self.width = 1200
        self.height = 900

        ## TKinter Classes
        self.root = tk.Tk()
        self.canvas = Canvas(self.root, bg='white')
        ## Base Coordinates
        self.left = self.width * 0.01
        self.right = self.width * 0.99
        self.top = self.height * 0.03
        self.bot = self.height * 0.85
        self.cen_x = self.width * 0.5
        self.cen_y_norm = self.height * 0.5
        self.cen_y = (self.top+self.bot) * 0.5 

        ## Distances
        self.cf_vert_mid = self.height * 0.25
        self.cf_horz_mid = self.width * 0.25
        self.cf_full_leg   = self.width * 0.35
        self.cf_branch_leg = self.width * 0.1

        self.top_mid = self.cen_y - self.cf_vert_mid
        self.bot_mid = self.cen_y + self.cf_vert_mid 
        self.left_mid = self.cen_x - self.cf_horz_mid  #self.width * 0.25
        self.right_mid = self.cen_x + self.cf_horz_mid

        self.offset_leg = self.height * 0.10
        self.left_leg = self.cen_x - self.cf_full_leg
        self.right_leg = self.cen_x + self.cf_full_leg

        self.tA = self.top_mid-self.offset_leg
        self.tB = self.top_mid+self.offset_leg
        self.bA = self.bot_mid-self.offset_leg
        self.bB = self.bot_mid+self.offset_leg

        ## Offsets
        self.entry_offset = self.width * 0.05
        self.text_offset  = self.width * 0.03
        self.mini_offset  = self.width * 0.015
        self.text_height = self.height * 0.04
        self.nature_boxsize = 6
        self.payoff_boxsize = 3

        self.dr = self.height * 0.01 # dr = dot radius

        # Data structures
        self.nature_entry = [] # Dimensions [2]
        self.nature_mat = np.zeros((1,2))
        self.matrix = np.zeros((4,2), dtype='i,i')
        self.entry_list = [] # Dimensions [4][2][2]
        self.p1_payoff_deviation = np.zeros((2,2))

        # Save files
        self.saved_file = "saved_matrix_sg.npy"
        self.saved_dim = "saved_dim_sg.npy"
        self.prev_file = "prev_matrix_sg.npy" 
        self.prev_dim = "prev_dim_sg.npy"
        self.nature_file = "nature_sg.npy"
        self.nature_prev = "nature_prev_sg.npy"
        self.matrix_import = np.zeros((4,2), dtype='i,i')
        self.matrix_import_bool = False

        # Matrix indexing
        self.top_index_offset = 0
        self.bot_index_offset = 2
    
    ## Incomplete 
    def pooling_eq(self, matrix_in, top_signal, bot_signal):
        # 1. Choose case - (need input p and q (signal probablilties determined by nature))
        # 2. Find U_p2 of each action of player 2 (F or R) (Fight or Retreat)
        # 3. Check for p1 deviation > if deviate, not pooling [DONE]
        # 4. If no deviation, find oppoisite signal probability
        # 5. Find the deviation point for oppositie signal probability
        top_sig_alt = 0 if (top_signal == 1) else 1
        bot_sig_alt = 0 if (bot_signal == 1) else 1

        self.top_signal = top_signal
        self.bot_signal = bot_signal   

def main():
    parent = SGE()
    csig_gui.create_spider_grid(parent, parent.root, parent.canvas)
    csig_gui.label_grid(parent, parent.root, parent.canvas)
    csig_gui.create_entry_boxes(parent, parent.root, parent.canvas)
    csig_gui.gen_entry_buttons(parent, parent.root, parent.canvas)
    csig_gui.draw_labels(parent, parent.root, parent.canvas)
    parent.root.mainloop()

if __name__ == '__main__':
    main()