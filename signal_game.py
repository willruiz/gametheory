from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys

class SGE:
    def __init__(self):
        self.rows = 4
        self.cols = 2
        self.width = 1500
        self.height = 1000
        self.root = tk.Tk()
        self.canvas = Canvas(self.root, bg='white')
        self.left = self.width * 0.01
        self.right = self.width * 0.99
        self.top = self.height * 0.03
        self.bot = self.height * 0.85
        self.cen_x = self.width * 0.5
        self.cen_y = self.height * 0.5

        self.bot_mid = self.bot - self.height * 0.15
        self.top_mid = self.top + self.height * 0.15
        self.left_mid = self.width * 0.25
        self.right_mid = self.width * 0.75

        self.offset_leg = self.height * 0.10
        self.left_leg = self.width * 0.15
        self.right_leg = self.width * 0.85

        self.entry_offset = self.width * 0.04
        self.mini_offset = self.width * 0.015

        self.dr = self.height * 0.01

        self.nature = [] # Dimensions [2]
        self.matrix = np.zeros((4,2), dtype='i,i')
        self.entry_list = [] # Dimensions [4][2][2]

        self.saved_file = "saved_matrix_sg.npy"
        self.saved_dim = "saved_dim_sg.npy"
        self.prev_file = "prev_matrix_sg.npy" 
        self.prev_dim = "prev_dim_sg.npy"
        self.matrix_import = np.zeros((4,2), dtype='i,i')
        self.matrix_import_bool = False
    
    def import_matrix(self, matrix_in): # FOR CUSTOM MATRIX INPUT FOR TEST SUITE
        self.matrix_import = matrix_in
        self.matrix_import_bool = True

    def create_spider_grid(self, root_in, canvas_in):
        root_in.geometry(str(self.width) + "x" + str(self.height))
        ## Boundaries
        canvas_in.create_line(self.left, self.top, self.right, self.top, fill="black", width ='2')
        canvas_in.create_line(self.left, self.top, self.left, self.bot, fill="black", width ='2')
        canvas_in.create_line(self.right, self.top, self.right, self.bot, fill="black", width ='2')
        canvas_in.create_line(self.left, self.bot, self.right, self.bot, fill="black", width ='2')

        ## Spider-Mid
        canvas_in.create_line(self.cen_x, self.top_mid, self.cen_x, self.bot_mid, fill="black", width ='4')
        canvas_in.create_oval(self.cen_x -self.dr, self.cen_y-self.dr, self.cen_x +self.dr, self.cen_y+self.dr, fill='black')
        canvas_in.create_line(self.left_mid, self.top_mid, self.right_mid, self.top_mid, fill="black", width ='4')
        canvas_in.create_oval(self.cen_x -self.dr, self.top_mid-self.dr, self.cen_x +self.dr, self.top_mid+self.dr, fill='black')
        canvas_in.create_line(self.left_mid, self.bot_mid, self.right_mid, self.bot_mid, fill="black", width ='4')
        canvas_in.create_oval(self.cen_x -self.dr, self.bot_mid-self.dr, self.cen_x +self.dr, self.bot_mid+self.dr, fill='black')

        ## Dotted
        canvas_in.create_line(self.left_mid, self.top_mid, self.left_mid, self.bot_mid, fill="black", width ='4', dash=(15,32))
        canvas_in.create_oval(self.left_mid -self.dr, self.top_mid -self.dr, self.left_mid +self.dr, self.top_mid +self.dr, fill='black')
        canvas_in.create_oval(self.left_mid -self.dr, self.bot_mid -self.dr, self.left_mid +self.dr, self.bot_mid +self.dr, fill='black')
        canvas_in.create_line(self.right_mid, self.top_mid, self.right_mid, self.bot_mid, fill="black", width ='4', dash=(15,32))
        canvas_in.create_oval(self.right_mid -self.dr, self.top_mid -self.dr, self.right_mid +self.dr, self.top_mid +self.dr, fill='black')
        canvas_in.create_oval(self.right_mid -self.dr, self.bot_mid -self.dr, self.right_mid +self.dr, self.bot_mid +self.dr, fill='black')
        
        # Spider-Legs - Top
        tA = self.top_mid-self.offset_leg
        tB = self.top_mid+self.offset_leg
        bA = self.bot_mid-self.offset_leg
        bB = self.bot_mid+self.offset_leg
        canvas_in.create_line(self.left_mid, self.top_mid, self.left_leg, tA, fill="black", width ='4')
        canvas_in.create_line(self.left_mid, self.top_mid, self.left_leg, tB, fill="black", width ='4')
        canvas_in.create_line(self.right_mid, self.top_mid, self.right_leg, tA, fill="black", width ='4')
        canvas_in.create_line(self.right_mid, self.top_mid, self.right_leg, tB, fill="black", width ='4')

        # Spider-Legs - Bot
        canvas_in.create_line(self.left_mid, self.bot_mid, self.left_leg, bA, fill="black", width ='4')
        canvas_in.create_line(self.left_mid, self.bot_mid, self.left_leg, bB, fill="black", width ='4')
        canvas_in.create_line(self.right_mid, self.bot_mid, self.right_leg, bA, fill="black", width ='4')
        canvas_in.create_line(self.right_mid, self.bot_mid, self.right_leg, bB, fill="black", width ='4')
        canvas_in.pack(fill=BOTH, expand=1)

    def fill_entries_from_matrix(self, matrix_in):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    if (str(matrix_in[i][j][k]) == '0'):
                        k_entry.set("")    
                    else:
                        k_entry.set(str(matrix_in[i][j][k]))

    def get_entries_into_matrix(self):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    str_input =k_entry.get()
                    input = 0
                    if (str_input == ''):
                        input = 0
                    else:
                        input = int(str_input)
                    self.matrix[i][j][k] = input

    def create_entry_boxes(self, root_in, canvas_in):
        tA = self.top_mid-self.offset_leg
        tB = self.top_mid+self.offset_leg
        bA = self.bot_mid-self.offset_leg
        bB = self.bot_mid+self.offset_leg

        # Player entry_list [4][2][2]
        for i in range(4):
            in_tuple = []
            for j in range(2):
                in_tuple.append((tk.StringVar(), tk.StringVar()))
            self.entry_list.append(in_tuple)

        if (not self.matrix_import_bool):
            prev_mat = np.load(self.prev_file)
            if ((prev_mat.shape[0] == self.rows) and (prev_mat.shape[1] == self.cols)):
                print("Loading prev")
                self.fill_entries_from_matrix(prev_mat)
            else:
                print("Prev is not loaded")
        else:
            print("Importing saved")
            self.fill_entries_from_matrix(self.matrix_import)

        # Nature probabilities
        for i in range(2):
            self.nature.append(tk.StringVar())
        entryN0 = tk.Entry (root_in, textvariable=self.nature[0], width = 6)
        canvas_in.create_window(self.cen_x + self.entry_offset, (self.cen_y+self.top_mid)/2, window=entryN0)
        entryN1 = tk.Entry (root_in, textvariable=self.nature[1], width = 6)
        canvas_in.create_window(self.cen_x + self.entry_offset, (self.cen_y+self.bot_mid)/2, window=entryN1)

        for i in range(4): # Corners
            for j in range(2): # up / down
                x_offset = 0
                y_offset = 0
                if (j == 0 and i <= 1):
                    y_offset = tA
                elif (j == 1 and i <= 1):
                    y_offset = tB
                elif (j == 0 and i > 1):
                    y_offset = bA
                else:
                    y_offset = bB
                if (i % 2 == 0):
                    x_offset = self.left_leg-self.entry_offset
                else:
                    x_offset = self.right_leg+self.entry_offset
                canvas_in.create_text(x_offset, y_offset, text=',', fill="black", font=('Arial 15 bold'))
                
                for k in range(2): # tuple
                    entryLeg = tk.Entry (root_in, textvariable=self.entry_list[i][j][k], width=4)
                    if (k == 0):
                        canvas_in.create_window(x_offset -self.mini_offset, y_offset, window=entryLeg)
                    else:
                        canvas_in.create_window(x_offset +self.mini_offset, y_offset, window=entryLeg)
    
    def submit(self):
        self.get_entries_into_matrix()
        print(self.matrix)
        print("SUBMIT")
        np.save(self.prev_file, self.matrix)

    def reset(self):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    k_entry.set("")
                    self.matrix[i][j][k] = 0
        print("RESET")
        np.save(self.prev_file, self.matrix)

    def quit_game(self):
        self.get_entries_into_matrix()
        print(self.matrix)
        np.save(self.prev_file, self.matrix)
        print("EXIT")
        self.root.destroy()
        
    def gen_entry_buttons(self, root, canvas):
    
        sub_btn=tk.Button(root,text = 'Submit', command = lambda: self.submit())
        canvas.create_window(self.cen_x, self.bot+20, window=sub_btn)
        # saved_btn=tk.Button(root,text = 'Load', command = lambda: self.enter_saved())
        # canvas.create_window(self.cen_x+160, self.bot+80, window=saved_btn)
        # prv2pst_btn=tk.Button(root,text = 'Save', command = lambda: self.transfer_entries_to_saved())
        # canvas.create_window(self.cen_x +160, self.bot+40, window=prv2pst_btn)
        reset_btn=tk.Button(root,text = 'Reset', command = lambda: self.reset())
        canvas.create_window(self.cen_x, self.bot+50, window=reset_btn)
        quit_btn = tk.Button(root, text="Exit", command = lambda: self.quit_game())
        canvas.create_window(self.cen_x, self.bot+80, window=quit_btn)


def main():
    parent = SGE()
    parent.create_spider_grid(parent.root, parent.canvas)
    parent.create_entry_boxes(parent.root, parent.canvas)
    parent.gen_entry_buttons(parent.root, parent.canvas)
    parent.root.mainloop()

if __name__ == '__main__':
    main()