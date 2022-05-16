from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys

rows = 3
cols = 3

class NFM:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.width = cols*200+100
        self.height = rows*200+100
        self.left = self.width * 0.2
        self.right = self.width * 0.8
        self.top = self.height * 0.2
        self.bot = self.height * 0.8
        self.unit_width = (self.right-self.left)/cols
        self.unit_height = (self.bot-self.top)/rows
        self.cenv = self.width * 0.5
        self.cenh = self.height * 0.5
        self.root = tk.Tk()
        self.offset = 20
        self.canvas = Canvas(self.root, bg='white')
        self.entry_list = []
        self.saved_file = "saved_matrix.npy"
        self.saved_dim = "saved_dim.npy"
        self.prev_file = "prev_matrix.npy" 
        self.prev_dim = "prev_dim.npy"

    def create_matrix(self):
        self.root.geometry(str(self.width) + "x" + str(self.height))
        print("width: ", self.width)
        print("height: ", self.height)

        self.canvas.create_line(self.left, self.top, self.right, self.top, fill="black", width ='5')
        self.canvas.create_line(self.left, self.top, self.left, self.bot, fill="black", width ='5')
        self.canvas.create_line(self.right, self.top, self.right, self.bot, fill="black", width ='5')
        self.canvas.create_line(self.left, self.bot, self.right, self.bot, fill="black", width ='5')

        for i in range(cols-1):
            divs_v = self.left+self.unit_width* (i+1)
            self.canvas.create_line(divs_v, self.top, divs_v, self.bot, fill="black", width ='5')

        for j in range(rows-1):
            divs_h = self.top+self.unit_height * (j+1)
            self.canvas.create_line(self.left, divs_h, self.right, divs_h, fill="black", width ='5')
        
        self.canvas.pack(fill=BOTH, expand=1)

    def fill_entries_from_matrix(self):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    if (str(self.matrix[i][j][k]) == '0'):
                        k_entry.set("")    
                    else:
                        k_entry.set(str(self.matrix[i][j][k]))

    def create_entry_boxes(canvas, root, rows, cols, entry_list):
        for i in range(rows):
            entry_row = []
            for j in range(cols):
                entry_row.append((tk.StringVar(), tk.StringVar()))
            entry_list.append(entry_row)

        prev_mat = np.load(prev_file)
        if ((prev_mat.shape[0] == rows) and (prev_mat.shape[1] == cols)):
            fill_entries_from_matrix(entry_list, prev_mat)
        else:
            print("Prev dimensions do not match - Cannot load")

        initH_offset = top+unit_height/2
        initW_offset = left+unit_width/2
        for i in range(rows):
            for j in range(cols):
                entryA0 = tk.Entry (root, textvariable=entry_list[i][j][0], width= 4)
                canvas.create_window(initW_offset+(unit_width*(j))-offset, initH_offset+(unit_height*(i)), window=entryA0)
                entryA1 = tk.Entry (root, textvariable=entry_list[i][j][1], width= 4)
                canvas.create_window(initW_offset+(unit_width*(j))+offset, initH_offset+(unit_height*(i)), window=entryA1)


def main():
    matrix = NFM(rows, cols)
    matrix.create_matrix()
    matrix.root.mainloop()

if __name__ == '__main__':
    main()