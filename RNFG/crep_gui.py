from tkinter import *
import tkinter as tk
import numpy as np
import crep_btn as cb
import crep_def as cd

def create_matrix_grid(parent_in, root_in, canvas_in):
        root_in.geometry(str(parent_in.width) + "x" + str(parent_in.true_height))
        print("width: ", parent_in.width)
        print("height: ", parent_in.height)

        canvas_in.create_line(parent_in.left,  parent_in.top, parent_in.right, parent_in.top, fill="black", width ='5')
        canvas_in.create_line(parent_in.left,  parent_in.top, parent_in.left,  parent_in.bot, fill="black", width ='5')
        canvas_in.create_line(parent_in.right, parent_in.top, parent_in.right, parent_in.bot, fill="black", width ='5')
        canvas_in.create_line(parent_in.left,  parent_in.bot, parent_in.right, parent_in.bot, fill="black", width ='5')

        for i in range(parent_in.cols-1):
            divs_v = parent_in.left+parent_in.unit_width* (i+1)
            canvas_in.create_line(divs_v, parent_in.top, divs_v, parent_in.bot, fill="black", width ='5')

        for j in range(parent_in.rows-1):
            divs_h = parent_in.top+parent_in.unit_height * (j+1)
            canvas_in.create_line(parent_in.left, divs_h, parent_in.right, divs_h, fill="black", width ='5')
        
        canvas_in.pack(fill=BOTH, expand=1)

def create_entry_boxes(parent_in, canvas):
    for i in range(parent_in.rows):
        entry_row = []
        for j in range(parent_in.cols):
            entry_row.append((tk.StringVar(), tk.StringVar()))
        parent_in.entry_list.append(entry_row)

    if (not parent_in.matrix_import_bool):
        try:
            prev_mat = np.load(parent_in.prev_file)
        except:
            prev_mat = np.zeros((parent_in.rows,parent_in.cols), dtype='i,i')
        if ((prev_mat.shape[0] == parent_in.rows) and (prev_mat.shape[1] == parent_in.cols)):
            parent_in.fill_entries_from_matrix(prev_mat)
        else:
            print("Prev is not loaded")
    else:
        parent_in.fill_entries_from_matrix(parent_in.matrix_import)
        

    initH_offset = parent_in.top + parent_in.unit_height/2
    initW_offset = parent_in.left+parent_in.unit_width/2
    for i in range(parent_in.rows):
        for j in range(parent_in.cols):
            coord_x = initW_offset+(parent_in.unit_width*(j))
            coord_y = initH_offset+(parent_in.unit_height*(i))
            entryA0 = tk.Entry (parent_in.root, textvariable=parent_in.entry_list[i][j][0], width= 4)
            canvas.create_window(coord_x-parent_in.offset, coord_y, window=entryA0)
            entryA1 = tk.Entry (parent_in.root, textvariable=parent_in.entry_list[i][j][1], width= 4)
            canvas.create_window(coord_x+parent_in.offset, coord_y, window=entryA1)

def gen_entry_buttons(parent_in, root, canvas):
    sub_btn   = tk.Button(root, text = 'Submit', bg = cd.reg_salmon, command = lambda: cb.submit(parent_in))
    load_btn  = tk.Button(root, text = 'Load'  , bg = cd.sea_green,  command = lambda: cb.load_entries(parent_in))
    save_btn  = tk.Button(root, text = 'Save'  , bg = cd.sea_green,  command = lambda: cb.save_entries(parent_in))
    reset_btn = tk.Button(root, text = 'Reset' , bg = cd.lite_teal,  command = lambda: cb.reset(parent_in))
    quit_btn  = tk.Button(root, text = "Exit"  , bg = cd.lite_ornge, command = lambda: cb.quit_game(parent_in), width = int(parent_in.width/60), height = 2)
    canvas.create_window(parent_in.cenv, parent_in.bot + 1 *(parent_in.height/20), window=sub_btn)
    canvas.create_window(parent_in.cenv, parent_in.bot + 2 *(parent_in.height/20), window=reset_btn)
    canvas.create_window(parent_in.cenv, parent_in.bot + 3.5 *(parent_in.height/20), window=quit_btn)
    canvas.create_window(parent_in.cenv + int(parent_in.height/6), parent_in.bot+1 *(parent_in.height/20), window=save_btn)
    canvas.create_window(parent_in.cenv + int(parent_in.height/6), parent_in.bot+2 *(parent_in.height/20), window=load_btn)