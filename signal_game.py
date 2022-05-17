from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys

class SGE:
    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.root = tk.Tk()
        self.canvas = Canvas(self.root, bg='white')
    
    def create_spider_grid(self, root_in, canvas_in):
        root_in.geometry(str(self.width) + "x" + str(self.height))
        canvas_in.create_line(self.left, self.top, self.right, self.top, fill="black", width ='5')
        canvas_in.create_line(self.left, self.top, self.left, self.bot, fill="black", width ='5')
        canvas_in.create_line(self.right, self.top, self.right, self.bot, fill="black", width ='5')
        canvas_in.create_line(self.left, self.bot, self.right, self.bot, fill="black", width ='5')

