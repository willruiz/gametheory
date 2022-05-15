import math
import numpy as np

def gen_basic_BR(matrix): # return index coordinates of BRs
    # Player 1 (going down each column)
    for i in range(matrix.shape[0]): # increment to the left
        for j in range(matrix.shape[1]): # scan down
            