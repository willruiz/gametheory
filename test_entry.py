from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys

rows = 3
cols = 4

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


def main():
    matrix = NFM(rows, cols)
    matrix.create_matrix()
    matrix.root.mainloop()

if __name__ == '__main__':
    main()