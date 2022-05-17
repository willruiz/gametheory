from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys

class SGE:
    def __init__(self):
        self.width = 1500
        self.height = 1000
        self.root = tk.Tk()
        self.canvas = Canvas(self.root, bg='white')
        self.left = self.width * 0.01
        self.right = self.width * 0.99
        self.top = self.height * 0.05
        self.bot = self.height * 0.95
        self.cen_x = self.width * 0.5
        self.cen_y = self.height * 0.5

        self.bot_mid = self.height * 0.75
        self.top_mid = self.height * 0.25
        self.left_mid = self.width * 0.25
        self.right_mid = self.width * 0.75

        self.offset_leg = self.height * 0.10
        self.left_leg = self.width * 0.15
        self.right_leg = self.width * 0.85

        self.entry_offset = self.width * 0.03

        self.dr = self.height * 0.01

        self.nature = []
        self.payoffs = []
    
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
        canvas_in.create_line(self.left_mid, self.top_mid, self.left_mid, self.bot_mid, fill="black", width ='4', dash=(25,22))
        canvas_in.create_oval(self.left_mid -self.dr, self.top_mid -self.dr, self.left_mid +self.dr, self.top_mid +self.dr, fill='black')
        canvas_in.create_oval(self.left_mid -self.dr, self.bot_mid -self.dr, self.left_mid +self.dr, self.bot_mid +self.dr, fill='black')
        canvas_in.create_line(self.right_mid, self.top_mid, self.right_mid, self.bot_mid, fill="black", width ='4', dash=(25,22))
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

    def create_entry_boxes(self, root_in, canvas_in):
        tA = self.top_mid-self.offset_leg
        tB = self.top_mid+self.offset_leg
        bA = self.bot_mid-self.offset_leg
        bB = self.bot_mid+self.offset_leg

        # Nature probabilities
        for i in range(2):
            self.nature.append(tk.StringVar())
        entryN0 = tk.Entry (root_in, textvariable=self.nature[0], width = 6)
        canvas_in.create_window(self.cen_x + self.entry_offset, (self.cen_y+self.top_mid)/2, window=entryN0)
        entryN1 = tk.Entry (root_in, textvariable=self.nature[1], width = 6)
        canvas_in.create_window(self.cen_x + self.entry_offset, (self.cen_y+self.bot_mid)/2, window=entryN1)
        # Player Payoffs [4][2][2]
        for i in range(4):
            in_tuple = []
            for j in range(2):
                in_tuple.append((tk.StringVar(), tk.StringVar()))
            self.payoffs.append(in_tuple)

        for i in range(4):
            for j in range(2):
                for k in range(2):
                    if (k == 0):
                        offset = tA
                    else:
                        offset = tB
                    entryA0 = tk.Entry (root_in, textvariable=self.payoffs[i][j][k], width=4)
                    canvas_in.create_window(self.cen_x + self.entry_offset, (self.cen_y+self.top_mid)/2, window=entryA0)

        # if (not self.matrix_import_bool):
        #     prev_mat = np.load(self.prev_file)
        #     if ((prev_mat.shape[0] == self.rows) and (prev_mat.shape[1] == self.cols)):
        #         self.fill_entries_from_matrix(prev_mat)
        #     else:
        #         print("Prev is not loaded")
        # else:
        #     self.fill_entries_from_matrix(self.matrix_import)
            

def main():
    parent = SGE()
    parent.create_spider_grid(parent.root, parent.canvas)
    parent.create_entry_boxes(parent.root, parent.canvas)
    parent.root.mainloop()

if __name__ == '__main__':
    main()