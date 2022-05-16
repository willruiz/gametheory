from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys
import basicNE as bne

rows = 3
cols = 3

def main():
    parent = bne.NFM(rows, cols)
    parent.init_np()
    parent.create_matrix_grid(parent.root, parent.canvas)
    parent.create_entry_boxes(parent.canvas)
    parent.gen_entry_buttons(parent.root, parent.canvas)
    parent.root.mainloop()

if __name__ == '__main__':
    main()