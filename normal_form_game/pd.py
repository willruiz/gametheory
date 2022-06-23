## NOTE: Only supports 2-player games - N-player games will have to developed in the future

from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys

rows = 4
cols = 5

height = 500
width = 500

left = 0
right = 0
top = 0
bot = 0

left = width * 0.2
right = width * 0.8
top = height * 0.2
bot = height * 0.8
cenv = width * 0.5
cenh = height * 0.5
unit_width = 0.0
unit_height = 0.0

offset = 20


root = tk.Tk()

saved_file = "saved_matrix.npy"
saved_dim = "saved_dim.npy"
prev_file = "prev_matrix.npy" 
prev_dim = "prev_dim.npy"
##
def update_dimensions(rows_in, cols_in):
    global width 
    global height
    global left
    global right
    global top
    global unit_width
    global unit_height   
    global bot 
    global cenv
    global cenh
    
    width = cols_in*200+50
    height = rows_in*200+50
    left = width * 0.2
    right = width * 0.8
    top = height * 0.2
    bot = height * 0.8
    unit_width = (right-left)/cols_in
    unit_height = (bot-top)/rows_in
    cenv = width * 0.5
    cenh = height * 0.5
##
def create_matrix(canvas, rows, cols, root):
    update_dimensions(rows, cols)
    root.geometry(str(width) + "x" + str(height))
    print("width: ", width)
    print("height: ", height)

    canvas.create_line(left, top, right, top, fill="black", width ='5')
    canvas.create_line(left, top, left, bot, fill="black", width ='5')
    canvas.create_line(right, top, right, bot, fill="black", width ='5')
    canvas.create_line(left, bot, right, bot, fill="black", width ='5')

    for i in range(cols-1):
        divs_v = left+unit_width* (i+1)
        canvas.create_line(divs_v, top, divs_v, bot, fill="black", width ='5')

    for j in range(rows-1):
        divs_h = top+unit_height * (j+1)
        canvas.create_line(left, divs_h, right, divs_h, fill="black", width ='5')
    
    canvas.pack(fill=BOTH, expand=1)
##
def fill_entries_from_matrix(entry_list, matrix):
    for i, i_entry in enumerate(entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                if (str(matrix[i][j][k]) == '0'):
                    k_entry.set("")    
                else:
                    k_entry.set(str(matrix[i][j][k]))

##
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
        print("Prev is not loaded")

    initH_offset = top+unit_height/2
    initW_offset = left+unit_width/2
    for i in range(rows):
        for j in range(cols):
            entryA0 = tk.Entry (root, textvariable=entry_list[i][j][0], width= 4)
            canvas.create_window(initW_offset+(unit_width*(j))-offset, initH_offset+(unit_height*(i)), window=entryA0)
            entryA1 = tk.Entry (root, textvariable=entry_list[i][j][1], width= 4)
            canvas.create_window(initW_offset+(unit_width*(j))+offset, initH_offset+(unit_height*(i)), window=entryA1)

##
def show_payoffs(canvas, matrix, p1_br, p2_br):
    initH_offset = top+unit_height/2
    initW_offset = left+unit_width/2
    for i in range(rows):
        for j in range(cols):
            coord_x = initW_offset+(unit_width*(j))
            coord_y = initH_offset+(unit_height*(i))
            if (p1_br[i][j]):
                canvas.create_rectangle(coord_x-offset-10, coord_y-10, coord_x-offset+15, coord_y+10, fill='#FFCCCB')
            if (p2_br[i][j]):
                canvas.create_rectangle(coord_x+offset-10, coord_y-10, coord_x+offset+15, coord_y+10, fill='#ADD8E6')
            canvas.create_text(coord_x-offset, coord_y, 
                text=matrix[i][j][0], fill="black", font=('Helvetica 15 bold'))
            canvas.create_text(coord_x, coord_y, 
                text=',', fill="black", font=('Helvetica 15 bold'))
            canvas.create_text(coord_x+offset, coord_y, 
                text=matrix[i][j][1], fill="black", font=('Helvetica 15 bold'))


def find_basic_BR(matrix): # return index coordinates of BRs
    # Player 1 (going down each column)
    match_p1 = np.zeros((rows, cols), dtype=bool)
    match_p2 = np.zeros((rows, cols), dtype=bool)
    for i in range(matrix.shape[1]): # increment right
        local_br_val = (-1*sys.maxsize)-1
        curr_col = (matrix[:,i])
        curr_col_indexed = [x[0] for x in curr_col]
        for j in range(matrix.shape[0]): # scan down
            curr = matrix[j][i][0]
            if (curr > local_br_val):
                local_br_val = curr
        # print("p1 br: ", local_br_val)
        # print("rows: ", rows)
        comp_col = np.zeros((1, rows))
        comp_col.fill(local_br_val)
        bool_col = (curr_col_indexed == comp_col)
        # #bool_col = np.reshape(bool_col[0], (rows,1))
        # print("comp_col: ", comp_col)
        # print("curr_col: ", curr_col)
        # print("curr_col_indexed: ", curr_col_indexed)
        # print("bool_matches: ", bool_col)
        # #print("match_p1[i,:].shape: ", match_col.shape)
        # print("bool_col.shape: ", bool_col.shape)
        for x in range(match_p1.shape[0]):
            match_p1[x,i] = bool_col[0][x]
    print(match_p1)
        # col_np = np.asarray(col_list)
        # matches = np.where(col_np == local_br_val)
        # match_p1.append(matches)
    
    # Player 2 (going right each row)
    for i in range(matrix.shape[0]): # increment down
        local_br_val = (-1*sys.maxsize)-1
        curr_row = (matrix[i,:])
        curr_row_indexed = [x[1] for x in curr_row]
        for j in range(matrix.shape[1]): # scan right
            curr = matrix[i][j][1]
            if (curr > local_br_val):
                local_br_val = curr
        #print("p2 br: ", local_br_val)
        comp_row = np.zeros((1, cols))
        comp_row.fill(local_br_val)
        bool_row = (curr_row_indexed == comp_row)
        # print("comp_row: ", comp_row)
        # print("curr_row: ", curr_row)
        # print("curr_row_indexed: ", curr_row_indexed)
        # print("bool_matches: ", bool_row)

        for x in range(match_p1.shape[0]):
            match_p2[i,x] = bool_row[0][x]
    print(match_p2)
        # row_np = np.asarray(row_list)
        # matches = np.where(row_np == local_br_val)
        # match_p2.append(matches)
    return match_p1, match_p2

def reset(entry_list, matrix):
    for i, i_entry in enumerate(entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                k_entry.set("")
                matrix[i][j][k] = 0
    print("RESET")
    #np.save(prev_file, matrix)


def enter_saved(entry_list):
    entry = np.load(saved_file)
    if ((entry.shape[0] == rows) and (entry.shape[1] == cols)):
        fill_entries_from_matrix(entry_list,entry)
        print("LOADED")
    else:
        print("Saved dimensions do not match - Cannot load")
    

def transfer_prev_to_saved():
    temp = np.load(prev_file)
    np.save(saved_file, temp)
    print("SAVED")



def init_np(matrix, rows, cols):
    matrix = np.resize(matrix, (rows, cols))
    return matrix

def gen_payoff_buttons(root, canvas):
    quit_btn = tk.Button(root, text="Exit", command=root.destroy)
    canvas.create_window(cenv, bot+80, window=quit_btn)

def gen_BR_grid(matrix, match_p1, match_p2):
    subroot = tk.Tk()
    subcan = Canvas(subroot, bg='white')
    create_matrix(subcan, rows, cols, subroot)
    show_payoffs(subcan, matrix, match_p1, match_p2)
    gen_payoff_buttons(subroot, subcan)
    subroot.mainloop()

def submit(entry_list, matrix):
    for i, i_entry in enumerate(entry_list):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): # iterate through tuple
                str_input =k_entry.get()
                input = 0
                if (str_input == ''):
                    input = 0
                else:
                    input = int(str_input)
                matrix[i][j][k] = input
                #print(matrix)
    print("SUBMIT")
    np.save(prev_file, matrix)

    # p1_br = []
    # p2_br = []
    p1_br, p2_br = find_basic_BR(matrix)
    # p1_br = np.asarray(p1_br)
    # p2_br = np.asarray(p2_br)
    gen_BR_grid(matrix, p1_br, p2_br)
    

def gen_entry_buttons(root, canvas, matrix, entry_list):
    
    sub_btn=tk.Button(root,text = 'Submit', command = lambda: submit(entry_list, matrix))
    canvas.create_window(cenv, bot+20, window=sub_btn)
    saved_btn=tk.Button(root,text = 'Load saved', command = lambda: enter_saved(entry_list))
    canvas.create_window(cenv+160, bot+80, window=saved_btn)
    prv2pst_btn=tk.Button(root,text = 'Move to saved', command = lambda: transfer_prev_to_saved())
    canvas.create_window(cenv+160, bot+40, window=prv2pst_btn)
    reset_btn=tk.Button(root,text = 'Reset', command = lambda: reset(entry_list, matrix))
    canvas.create_window(cenv, bot+50, window=reset_btn)
    quit_btn = tk.Button(root, text="Exit", command=root.destroy)
    canvas.create_window(cenv, bot+80, window=quit_btn)


def main():
    
    canvas = Canvas(root, bg='white')

    entry_list = []
    matrix = np.zeros((1,1), dtype='i,i')

    matrix = init_np(matrix, rows, cols)
    print(matrix)
    
    create_matrix(canvas, rows, cols, root)
    create_entry_boxes(canvas, root, rows, cols, entry_list)
    gen_entry_buttons(root, canvas, matrix, entry_list)
    
    root.mainloop()


if __name__ == '__main__':
    main()