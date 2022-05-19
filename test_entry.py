from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys


#matrix = np.zeros((4,2,2))
matrix = np.zeros((4,2), dtype='i,i')
matrix[0][1][1] = 3
print(matrix)

tot = np.linspace((1,9),(8,16),8)