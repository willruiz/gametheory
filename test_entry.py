# Program to make a simple
# login screen 
 
import numpy as np
import tkinter as tk
#x = np.arange(10)
x = np.zeros((3,3), dtype='i,i')

np.save("test.npy", x)

y = np.load("test.npy")
print(y)