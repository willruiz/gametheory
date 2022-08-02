from tkinter import *
import tkinter as tk
import numpy as np
import crep_btn as cb
import crep_def as cd
import crep_np  as cn

def create_matrix_grid(parent_in, root_in, canvas_in):
        root_in.geometry(str(parent_in.width) + "x" + str(parent_in.true_height))

        canvas_in.create_line(parent_in.left,  parent_in.top, parent_in.right, parent_in.top, fill=cd.dark_blue, width ='5')
        canvas_in.create_line(parent_in.left,  parent_in.top, parent_in.left,  parent_in.bot, fill=cd.dark_red,  width ='5')
        canvas_in.create_line(parent_in.right, parent_in.top, parent_in.right, parent_in.bot, fill="black", width ='5')
        canvas_in.create_line(parent_in.left,  parent_in.bot, parent_in.right, parent_in.bot, fill="black", width ='5')

        for i in range(parent_in.cols-1):
            divs_v = parent_in.left+parent_in.boxlen* (i+1)
            canvas_in.create_line(divs_v, parent_in.top, divs_v, parent_in.bot, fill="black", width ='5')

        for j in range(parent_in.rows-1):
            divs_h = parent_in.top+parent_in.boxlen * (j+1)
            canvas_in.create_line(parent_in.left, divs_h, parent_in.right, divs_h, fill="black", width ='5')
        
        canvas_in.pack(fill=BOTH, expand=1)

def gen_labels(parent_in, canvas_in):
    label_left = parent_in.left - int(parent_in.boxlen*0.4)
    p1_cen     = parent_in.top + (parent_in.rows*parent_in.boxlen)/2
    label_top  = parent_in.top - int(parent_in.boxlen*0.35)
    p2_cen     = parent_in.left + (parent_in.cols*parent_in.boxlen)/2
    canvas_in.create_text(label_left, p1_cen, 
                text = "P1", fill="red", font=(cd.label_font))
    canvas_in.create_text(p2_cen, label_top, 
                text = "P2", fill="blue", font=(cd.label_font))
    for i in range(parent_in.rows): # P1 indexes
        canvas_in.create_text(label_left + parent_in.boxlen*0.24, parent_in.initH_offset + i*parent_in.boxlen, 
                text = "[{}]".format(str(i)), fill=cd.lite_red, font=(cd.entry_font))
    for i in range(parent_in.cols): # P1 indexes
        canvas_in.create_text(parent_in.initW_offset + i*parent_in.boxlen, label_top+parent_in.boxlen*0.24,
                text = "[{}]".format(str(i)), fill=cd.lite_blue, font=(cd.entry_font))

def create_entry_boxes(parent_in, canvas):
    for i in range(parent_in.rows):
        entry_row = []
        for j in range(parent_in.cols):
            entry_row.append((tk.StringVar(), tk.StringVar()))
        parent_in.entry_list.append(entry_row)

    if (not parent_in.matrix_import_bool):
        try:
            if parent_in.square_bool:
                prev_mat = np.load(parent_in.dim_save[parent_in.square_dim])    
            else:
                prev_mat = np.load(parent_in.prev_file)
        except:
            print("Prev not loaded")
            prev_mat = np.zeros((parent_in.rows,parent_in.cols), dtype='i,i')
        if ((prev_mat.shape[0] == parent_in.rows) and (prev_mat.shape[1] == parent_in.cols)):
            cn.fill_entries_from_matrix(parent_in, prev_mat)
        else:
            print("Prev is not loaded")
    else:
        cn.fill_entries_from_matrix(parent_in, parent_in.matrix_import)
        
    for i in range(parent_in.rows):
        for j in range(parent_in.cols):
            coord_x = parent_in.initW_offset+(parent_in.boxlen*(j))
            coord_y = parent_in.initH_offset+(parent_in.boxlen*(i))
            entryA0 = tk.Entry (parent_in.root, textvariable=parent_in.entry_list[i][j][parent_in.p1_index], width= 3, font = cd.entry_font)
            canvas.create_window(coord_x-parent_in.offset, coord_y, window=entryA0)
            entryA1 = tk.Entry (parent_in.root, textvariable=parent_in.entry_list[i][j][parent_in.p2_index], width= 3, font = cd.entry_font)
            canvas.create_window(coord_x+parent_in.offset, coord_y, window=entryA1)

    parent_in.save_as_str = tk.StringVar()
    parent_in.load_as_str = tk.StringVar()
    entry_save_as = tk.Entry (parent_in.root, textvariable= parent_in.save_as_str, width = cd.file_boxsize)
    entry_load_as = tk.Entry (parent_in.root, textvariable= parent_in.load_as_str, width = cd.file_boxsize)
    canvas.create_window(parent_in.cenv + 2.1*int(parent_in.boxlen/2), parent_in.bot + 1 *(parent_in.boxlen/4),    window=entry_save_as)
    canvas.create_window(parent_in.cenv + 2.1*int(parent_in.boxlen/2), parent_in.bot + 1.75 *(parent_in.boxlen/4), window=entry_load_as)

def gen_entry_buttons(parent_in, root, canvas_in):

    reset_btn   = tk.Button(root, text = 'Reset', bg = cd.sea_green,  command = lambda: cb.reset(parent_in))
    load_btn    = tk.Button(root, text = 'Load' , bg = cd.sea_green,  command = lambda: cb.load_entries(parent_in, "_", False))
    print_btn   = tk.Button(root, text = 'Print',                     command = lambda: cb.print_output(parent_in))
    save_btn    = tk.Button(root, text = 'Save' ,                     command = lambda: cb.save_entries(parent_in, "_", False))
    save_as_btn = tk.Button(root, text = 'Save As', bg = cd.lite_teal,               command = lambda: cb.save_as(parent_in))
    load_as_btn = tk.Button(root, text = 'Load As', bg = cd.lite_teal, fg = "black", command = lambda: cb.load_as(parent_in))
    rand_btn    = tk.Button(root,text = 'Rand',    bg = cd.lite_magnta, fg = "black", command = lambda: cb.rand_gen(parent_in))

    nfg_btn     = tk.Button(root, text = ' NFG ', bg = cd.dim_red,  fg = "white", command = lambda: cb.nfg(parent_in),  width = int(parent_in.boxlen/20))
    rnfg_btn    = tk.Button(root, text = 'RNFG' , bg = cd.dim_blue, fg = "white", command = lambda: cb.rnfg(parent_in), width = int(parent_in.boxlen/20))
    quit_btn    = tk.Button(root, text = "Exit" , bg = cd.lite_ornge, command = lambda: cb.quit_game(parent_in), width = int(parent_in.boxlen/5), height = 3)
    
    canvas_in.create_window(parent_in.cenv - 1.75 * int(parent_in.boxlen/2), parent_in.bot + 1 *(parent_in.boxlen/4),    window=print_btn)
    canvas_in.create_window(parent_in.cenv - 1.75 * int(parent_in.boxlen/2), parent_in.bot + 1.75 *(parent_in.boxlen/4), window=save_btn)
    canvas_in.create_window(parent_in.cenv - 1.0  * int(parent_in.boxlen/2), parent_in.bot + 1 *(parent_in.boxlen/4),    window=reset_btn)
    canvas_in.create_window(parent_in.cenv - 1.0  * int(parent_in.boxlen/2), parent_in.bot + 1.75 *(parent_in.boxlen/4), window=load_btn)
    canvas_in.create_window(parent_in.cenv + 1.1  * int(parent_in.boxlen/2), parent_in.bot + 1 *(parent_in.boxlen/4),    window=save_as_btn)
    canvas_in.create_window(parent_in.cenv + 1.1  * int(parent_in.boxlen/2), parent_in.bot + 1.75 *(parent_in.boxlen/4), window=load_as_btn)
    canvas_in.create_window(parent_in.cenv - 2.5  * int(parent_in.boxlen/2), parent_in.bot + 1.3  *(parent_in.boxlen/4), window=rand_btn)

    canvas_in.create_window(parent_in.cenv, parent_in.bot + 1 *int(parent_in.boxlen/4), window=nfg_btn)
    canvas_in.create_window(parent_in.cenv, parent_in.bot + 1.75 *int(parent_in.boxlen/4), window=rnfg_btn)

    canvas_in.create_window(parent_in.cenv, parent_in.bot + int(3.2 *int(parent_in.boxlen/4)), window=quit_btn)
    