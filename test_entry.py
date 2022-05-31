from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys


master = Tk()

w = Canvas(master, width=200, height=100)
w.pack()

w.create_line(150,0, 100,50, 50,0, 0,50, smooth=1)

mainloop()