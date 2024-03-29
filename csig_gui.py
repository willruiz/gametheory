from tkinter import *
import tkinter      as tk
import numpy        as np
import csig_np      as cn
import csig_btn     as cb
import csig_logic   as cl
import csig_def     as cd

STR_HID = 0
STR_REV = 1
WEK_HID = 0
WEK_REV = 1

def draw_labels(self, root_in, canvas_in):
    canvas_in.create_text(self.cen_x+self.entry_offset, (self.cen_y),                text='Nature', fill="dark blue", font=(cd.text_font))
    canvas_in.create_text(self.cen_x-self.entry_offset, (self.cen_y+self.top_mid)/2, text='Strong', fill="blue",      font=(cd.text_font))
    canvas_in.create_text(self.cen_x-self.entry_offset, (self.cen_y+self.bot_mid)/2, text='Weak',   fill="blue",      font=(cd.text_font))
    canvas_in.create_text((self.cen_x + self.left_mid)/2,  self.top_mid-self.mini_offset, text='Hide',   fill="black", font=(cd.text_font))
    canvas_in.create_text((self.cen_x + self.right_mid)/2, self.top_mid-self.mini_offset, text='Reveal', fill="black", font=(cd.text_font))
    canvas_in.create_text((self.cen_x + self.left_mid)/2,  self.bot_mid+self.mini_offset, text='Hide',   fill="black", font=(cd.text_font))
    canvas_in.create_text((self.cen_x + self.right_mid)/2, self.bot_mid+self.mini_offset, text='Reveal', fill="black", font=(cd.text_font))

    canvas_in.create_text((self.left_leg+self.left_mid)/2,   self.tA, text='Fight',   fill='green', font=(cd.small_font))
    canvas_in.create_text((self.left_leg+self.left_mid)/2,   self.tB, text='Retreat', fill='green', font=(cd.small_font))
    canvas_in.create_text((self.right_leg+self.right_mid)/2, self.tA, text='Fight',   fill='green', font=(cd.small_font))
    canvas_in.create_text((self.right_leg+self.right_mid)/2, self.tB, text='Retreat', fill='green', font=(cd.small_font))
    
    canvas_in.create_text((self.left_leg+self.left_mid)/2, self.bA, text='Fight', fill='green',     font=(cd.small_font))
    canvas_in.create_text((self.left_leg+self.left_mid)/2, self.bB, text='Retreat', fill='green',   font=(cd.small_font))
    canvas_in.create_text((self.right_leg+self.right_mid)/2, self.bA, text='Fight', fill='green',   font=(cd.small_font))
    canvas_in.create_text((self.right_leg+self.right_mid)/2, self.bB, text='Retreat', fill='green', font=(cd.small_font))

    canvas_in.create_text((self.cen_x), (self.tA+self.top_mid*2)/3, text='P1', fill='#960091', font=(cd.small_font))
    canvas_in.create_text((self.cen_x), (self.bB+self.bot_mid*2)/3, text='P1', fill='#960091', font=(cd.small_font))

    canvas_in.create_text((self.left_mid),  (self.tA+self.top_mid*2)/3, text='P2', fill='teal', font=(cd.small_font))
    canvas_in.create_text((self.right_mid), (self.tA+self.top_mid*2)/3, text='P2', fill='teal', font=(cd.small_font))
    canvas_in.create_text((self.left_mid),  (self.bB+self.bot_mid*2)/3, text='P2', fill='teal', font=(cd.small_font))
    canvas_in.create_text((self.right_mid), (self.bB+self.bot_mid*2)/3, text='P2', fill='teal', font=(cd.small_font))

def create_spider_grid(self, root_in, canvas_in):
    root_in.geometry(str(self.width) + "x" + str(self.height))
    ## Boundaries
    canvas_in.create_line(self.left, self.top, self.right, self.top, fill="black", width ='2')
    canvas_in.create_line(self.left, self.top, self.left, self.bot, fill="black", width ='2')
    canvas_in.create_line(self.right, self.top, self.right, self.bot, fill="black", width ='2')
    canvas_in.create_line(self.left, self.bot, self.right, self.bot, fill="black", width ='2')

    ## Spider-Mid
    canvas_in.create_line(self.cen_x, self.top_mid, self.cen_x, self.bot_mid, fill="black", width ='4')
    canvas_in.create_oval(self.cen_x -self.dr, self.cen_y-self.dr, self.cen_x +self.dr, self.cen_y+self.dr, fill='black')
    canvas_in.create_line(self.left_mid, self.top_mid, self.right_mid, self.top_mid, fill="black", width ='4')
    canvas_in.create_oval(self.cen_x -self.dr, self.top_mid-self.dr, self.cen_x +self.dr, self.top_mid+self.dr, fill='black')
    canvas_in.create_line(self.left_mid, self.bot_mid, self.right_mid, self.bot_mid, fill="black", width ='4')
    canvas_in.create_oval(self.cen_x -self.dr, self.bot_mid-self.dr, self.cen_x +self.dr, self.bot_mid+self.dr, fill='black')

    ## Dotted
    canvas_in.create_line(self.left_mid, self.top_mid, self.left_mid, self.bot_mid, fill="black", width ='4', dash=(15,32))
    canvas_in.create_oval(self.left_mid -self.dr, self.top_mid -self.dr, self.left_mid +self.dr, self.top_mid +self.dr, fill='black')
    canvas_in.create_oval(self.left_mid -self.dr, self.bot_mid -self.dr, self.left_mid +self.dr, self.bot_mid +self.dr, fill='black')
    canvas_in.create_line(self.right_mid, self.top_mid, self.right_mid, self.bot_mid, fill="black", width ='4', dash=(15,32))
    canvas_in.create_oval(self.right_mid -self.dr, self.top_mid -self.dr, self.right_mid +self.dr, self.top_mid +self.dr, fill='black')
    canvas_in.create_oval(self.right_mid -self.dr, self.bot_mid -self.dr, self.right_mid +self.dr, self.bot_mid +self.dr, fill='black')
    
    # Spider-Legs - Top
    canvas_in.create_line(self.left_mid, self.top_mid, self.left_leg, self.tA, fill="black", width ='4')
    canvas_in.create_line(self.left_mid, self.top_mid, self.left_leg, self.tB, fill="black", width ='4')
    canvas_in.create_line(self.right_mid, self.top_mid, self.right_leg, self.tA, fill="black", width ='4')
    canvas_in.create_line(self.right_mid, self.top_mid, self.right_leg, self.tB, fill="black", width ='4')

    # Spider-Legs - Bot
    canvas_in.create_line(self.left_mid, self.bot_mid, self.left_leg, self.bA, fill="black", width ='4')
    canvas_in.create_line(self.left_mid, self.bot_mid, self.left_leg, self.bB, fill="black", width ='4')
    canvas_in.create_line(self.right_mid, self.bot_mid, self.right_leg, self.bA, fill="black", width ='4')
    canvas_in.create_line(self.right_mid, self.bot_mid, self.right_leg, self.bB, fill="black", width ='4')
    ## Experiment:
    
    canvas_in.pack(fill=BOTH, expand=1)

def label_grid(self, root_in, canvas_in):
    # Grid labels:
    # Top labels:
    canvas_in.create_line(self.cen_x,     self.top, self.cen_x,     self.bot, fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.left_mid,  self.top, self.left_mid,  self.bot, fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.left_leg,  self.top, self.left_leg,  self.bot, fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.right_mid, self.top, self.right_mid, self.bot, fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.right_leg, self.top, self.right_leg, self.bot, fill=cd.dark_gray, width ='1')

    canvas_in.create_text(self.cen_x,     self.top+self.mini_offset, text='CEN_X', fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.left_mid,  self.top+self.mini_offset, text='LEFT_MID', fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.left_leg,  self.top+self.mini_offset, text='LEFT_LEG', fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.right_mid, self.top+self.mini_offset, text='RIGHT_MID', fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.right_leg, self.top+self.mini_offset, text='RIGHT_LEG', fill=cd.lite_gray, font=(cd.grid_font))

    # Left Labels
    canvas_in.create_line(self.left, self.cen_y,   self.right, self.cen_y,   fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.left, self.top_mid, self.right, self.top_mid, fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.left, self.bot_mid, self.right, self.bot_mid, fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.left, self.tA,      self.right, self.tA,      fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.left, self.tB,      self.right, self.tB,      fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.left, self.bA,      self.right, self.bA,      fill=cd.dark_gray, width ='1')
    canvas_in.create_line(self.left, self.bB,      self.right, self.bB,      fill=cd.dark_gray, width ='1')
    
    canvas_in.create_text(self.left+self.text_offset, self.cen_y,   text='CEN_Y',   fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.left+self.text_offset, self.top_mid, text='TOP_MID', fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.left+self.text_offset, self.bot_mid, text='BOT_MID', fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.left+self.text_offset, self.tA,      text='tA',      fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.left+self.text_offset, self.tB,      text='tB',      fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.left+self.text_offset, self.bA,      text='bA',      fill=cd.lite_gray, font=(cd.grid_font))
    canvas_in.create_text(self.left+self.text_offset, self.bB,      text='bB',      fill=cd.lite_gray, font=(cd.grid_font))

def create_entry_boxes(self, root_in, canvas_in):
    # Player entry_list [4][2][2]
    for i in range(4):
        in_tuple = []
        for j in range(2):
            in_tuple.append((tk.StringVar(), tk.StringVar()))
        self.entry_list.append(in_tuple)

    if (not self.matrix_import_bool):
        prev_mat = np.load(self.prev_file)
        if ((prev_mat.shape[0] == self.rows) and (prev_mat.shape[1] == self.cols)):
            print("Loading prev")
            cn.fill_entries_from_matrix(self, prev_mat)
        else:
            print("Prev is not loaded")
    else:
        print("Importing saved")
        cn.fill_entries_from_matrix(self, self.matrix_import)

    # Nature probabilities
    for i in range(2):
        self.nature_entry.append(tk.StringVar())
    entryN0 = tk.Entry (root_in, textvariable=self.nature_entry[0], width = self.nature_boxsize)
    entryN1 = tk.Entry (root_in, textvariable=self.nature_entry[1], width = self.nature_boxsize)
    canvas_in.create_window(self.cen_x + self.entry_offset, (self.cen_y+self.top_mid)/2, window=entryN0)
    canvas_in.create_window(self.cen_x + self.entry_offset, (self.cen_y+self.bot_mid)/2, window=entryN1)
    nature_prev_mat = np.load(self.nature_prev)
    cn.fill_nature_entry_from_Natrix(self, nature_prev_mat)

    for i in range(4): # Corners
        for j in range(2): # up / down
            x_offset = 0
            y_offset = 0
            if (j == 0 and i <= 1):
                y_offset = self.tA
            elif (j == 1 and i <= 1):
                y_offset = self.tB
            elif (j == 0 and i > 1):
                y_offset = self.bA
            else:
                y_offset = self.bB
            if (i % 2 == 0):
                x_offset = self.left_leg  - self.entry_offset
            else:
                x_offset = self.right_leg + self.entry_offset
            canvas_in.create_text(x_offset, y_offset, text=',', fill="black", font=(cd.text_font))
            
            for k in range(2): # tuple
                entryLeg = tk.Entry (root_in, textvariable=self.entry_list[i][j][k], width=self.payoff_boxsize)
                if (k == 0):
                    canvas_in.create_window(x_offset - self.mini_offset, y_offset, window=entryLeg)
                else:
                    canvas_in.create_window(x_offset + self.mini_offset, y_offset, window=entryLeg)

    self.save_as_str = tk.StringVar()
    self.load_as_str = tk.StringVar()
    entry_save_as = tk.Entry (root_in, textvariable= self.save_as_str, width = self.file_boxsize)
    entry_load_as = tk.Entry (root_in, textvariable= self.load_as_str, width = self.file_boxsize)
    canvas_in.create_window(self.cen_x-380, self.bot+40, window=entry_save_as)
    canvas_in.create_window(self.cen_x-380, self.bot+80, window=entry_load_as)
    
def gen_entry_buttons(self, root, canvas):
    SEPR_btn_A  = tk.Button(root,text = 'SEPR A',  bg = "red",        fg = "white", command = lambda: cl.seperating_eq(self, self.matrix, STR_REV, WEK_HID))
    SEPR_btn_B  = tk.Button(root,text = 'SEPR B',  bg = "blue",       fg = "white", command = lambda: cl.seperating_eq(self, self.matrix, STR_HID, WEK_REV))
    POOL_btn_A  = tk.Button(root,text = 'POOL A',  bg = cd.mute_red,  fg = "white", command = lambda: cl.pooling_eq (self, self.matrix, self.nature_mat, STR_REV, WEK_REV))
    POOL_btn_B  = tk.Button(root,text = 'POOL B',  bg = cd.mute_blue, fg = "white", command = lambda: cl.pooling_eq (self, self.matrix, self.nature_mat, STR_HID, WEK_HID))
    print_btn   = tk.Button(root,text = 'Print',                                    command = lambda: cb.submit(self)) # cannot name function cb.print()
    reset_btn   = tk.Button(root,text = 'Reset',   bg = cd.sea_green, fg = "black", command = lambda: cb.reset(self))  # keyword conflict
    save_btn    = tk.Button(root,text = 'Save',                                     command = lambda: cb.save_entry(self, self.saved_file, False))
    load_btn    = tk.Button(root,text = 'Load',    bg = cd.sea_green, fg = "black", command = lambda: cb.load_entry(self, self.saved_file, False))
    save_as_btn = tk.Button(root,text = 'Save As', bg = cd.lite_teal,               command = lambda: cb.save_as(self))
    load_as_btn = tk.Button(root,text = 'Load As', bg = cd.lite_teal, fg = "black", command = lambda: cb.load_as(self))
    quit_btn    = tk.Button(root,text = "Exit",    bg = cd.lite_ornge, command = lambda: cb.quit_game(self, self.root), width = 36, height = 3)
    rnd_btn     = tk.Button(root,text = 'Rand',    bg = cd.lite_magnta, fg = "black", command = lambda: cb.random_gen(self))
    
    wi = self.width/120
    hi = self.height/90

    canvas.create_window(self.cen_x-5 *wi, self.bot+4*hi,   window=SEPR_btn_A)
    canvas.create_window(self.cen_x-5 *wi, self.bot+8*hi,   window=SEPR_btn_B)
    canvas.create_window(self.cen_x+5 *wi, self.bot+4*hi,   window=POOL_btn_A)
    canvas.create_window(self.cen_x+5 *wi, self.bot+8*hi,   window=POOL_btn_B)
    canvas.create_window(self.cen_x-25*wi, self.bot+4*hi,   window=print_btn)
    canvas.create_window(self.cen_x-25*wi, self.bot+8*hi,   window=reset_btn)
    canvas.create_window(self.cen_x-18*wi, self.bot+4*hi,   window=save_btn)
    canvas.create_window(self.cen_x-18*wi, self.bot+8*hi,   window=load_btn)
    canvas.create_window(self.cen_x-48*wi, self.bot+4*hi,   window=save_as_btn)
    canvas.create_window(self.cen_x-48*wi, self.bot+8*hi,   window=load_as_btn)
    canvas.create_window(self.cen_x+52*wi, self.bot+6.1*hi, window=rnd_btn)
    canvas.create_window(self.cen_x+30*wi, self.bot+6*hi,   window=quit_btn)

