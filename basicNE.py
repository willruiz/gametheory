import math
import numpy as np
import sys

def gen_basic_BR(matrix): # return index coordinates of BRs
    # Player 1 (going down each column)
    match_p1 = []
    match_p2 = []
    for i in range(matrix.shape[1]): # increment right
        local_br_val = (-1*sys.maxsize)-1
        col_list = []
        for j in range(matrix.shape[0]): # scan down
            curr = matrix[i][j][0]
            col_list.append(curr)
            if (curr > local_br_val):
                local_br_val = curr
        col_np = np.asarray(col_list)
        matches = np.where(col_np == local_br_val)
        match_p1.append(matches)
    
    # Player 2 (going right each row)
    for i in range(matrix.shape[0]): # increment down
        local_br_val = (-1*sys.maxsize)-1
        row_list = []
        for j in range(matrix.shape[1]): # scan right
            curr = matrix[i][j][1]
            row_list.append(curr)
            if (curr > local_br_val):
                local_br_val = curr
        row_np = np.asarray(row_list)
        matches = np.where(row_np == local_br_val)
        match_p2.append(matches)
        
        
