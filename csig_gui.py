from tkinter import *
import tkinter as tk
import numpy as np
import csig_np
import csig_btn

STR_HID = 0
STR_REV = 1
WEK_HID = 0
WEK_REV = 1

def draw_labels(self, root_in, canvas_in):
        canvas_in.create_text(self.cen_x-self.entry_offset, (self.cen_y+self.top_mid)/2, text='Strong', fill="blue", font=('Arial 15 bold'))
        canvas_in.create_text(self.cen_x-self.entry_offset, (self.cen_y+self.bot_mid)/2, text='Weak', fill="blue", font=('Arial 15 bold'))
        canvas_in.create_text((self.cen_x + self.left_mid)/2, self.top_mid-self.mini_offset, text='Hide', fill="black", font=('Arial 15 bold'))
        canvas_in.create_text((self.cen_x + self.right_mid)/2, self.top_mid-self.mini_offset, text='Reveal', fill="black", font=('Arial 15 bold'))
        canvas_in.create_text((self.cen_x + self.left_mid)/2, self.bot_mid+self.mini_offset, text='Hide', fill="black", font=('Arial 15 bold'))
        canvas_in.create_text((self.cen_x + self.right_mid)/2, self.bot_mid+self.mini_offset, text='Reveal', fill="black", font=('Arial 15 bold'))

        canvas_in.create_text((self.left_leg+self.left_mid)/2, self.tA, text='Fight', fill='green', font=('Arial 12 bold'))
        canvas_in.create_text((self.left_leg+self.left_mid)/2, self.tB, text='Retreat', fill='green', font=('Arial 12 bold'))
        canvas_in.create_text((self.right_leg+self.right_mid)/2, self.tA, text='Fight', fill='green', font=('Arial 12 bold'))
        canvas_in.create_text((self.right_leg+self.right_mid)/2, self.tB, text='Retreat', fill='green', font=('Arial 12 bold'))
        
        canvas_in.create_text((self.left_leg+self.left_mid)/2, self.bA, text='Fight', fill='green', font=('Arial 12 bold'))
        canvas_in.create_text((self.left_leg+self.left_mid)/2, self.bB, text='Retreat', fill='green', font=('Arial 12 bold'))
        canvas_in.create_text((self.right_leg+self.right_mid)/2, self.bA, text='Fight', fill='green', font=('Arial 12 bold'))
        canvas_in.create_text((self.right_leg+self.right_mid)/2, self.bB, text='Retreat', fill='green', font=('Arial 12 bold'))

        canvas_in.create_text((self.cen_x), (self.tA+self.top_mid*2)/3, text='P1', fill='#960091', font=('Arial 12 bold'))
        canvas_in.create_text((self.cen_x), (self.bB+self.bot_mid*2)/3, text='P1', fill='#960091', font=('Arial 12 bold'))

        canvas_in.create_text((self.left_mid), (self.tA+self.top_mid*2)/3, text='P2', fill='teal', font=('Arial 12 bold'))
        canvas_in.create_text((self.right_mid), (self.tA+self.top_mid*2)/3, text='P2', fill='teal', font=('Arial 12 bold'))
        canvas_in.create_text((self.left_mid), (self.bB+self.bot_mid*2)/3, text='P2', fill='teal', font=('Arial 12 bold'))
        canvas_in.create_text((self.right_mid), (self.bB+self.bot_mid*2)/3, text='P2', fill='teal', font=('Arial 12 bold'))

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
    canvas_in.create_line(self.cen_x, self.top, self.cen_x, self.bot, fill="#bebebe", width ='1')
    canvas_in.create_line(self.left_mid, self.top, self.left_mid, self.bot, fill="#bebebe", width ='1')
    canvas_in.create_line(self.left_leg, self.top, self.left_leg, self.bot, fill="#bebebe", width ='1')
    canvas_in.create_line(self.right_mid, self.top, self.right_mid, self.bot, fill="#bebebe", width ='1')
    canvas_in.create_line(self.right_leg, self.top, self.right_leg, self.bot, fill="#bebebe", width ='1')

    canvas_in.create_text(self.cen_x, self.top+self.mini_offset, text='CEN_X', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.left_mid, self.top+self.mini_offset, text='LEFT_MID', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.left_leg, self.top+self.mini_offset, text='LEFT_LEG', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.right_mid, self.top+self.mini_offset, text='RIGHT_MID', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.right_leg, self.top+self.mini_offset, text='RIGHT_LEG', fill="#545454", font=('Arial 12'))

    # Left Labels
    canvas_in.create_line(self.left, self.cen_y, self.right, self.cen_y, fill="#bebebe", width ='1')
    canvas_in.create_line(self.left, self.top_mid, self.right, self.top_mid, fill="#bebebe", width ='1')
    canvas_in.create_line(self.left, self.bot_mid, self.right, self.bot_mid, fill="#bebebe", width ='1')
    canvas_in.create_line(self.left, self.tA, self.right, self.tA, fill="#bebebe", width ='1')
    canvas_in.create_line(self.left, self.tB, self.right, self.tB, fill="#bebebe", width ='1')
    canvas_in.create_line(self.left, self.bA, self.right, self.bA, fill="#bebebe", width ='1')
    canvas_in.create_line(self.left, self.bB, self.right, self.bB, fill="#bebebe", width ='1')

    canvas_in.create_text(self.left+self.text_offset, self.cen_y, text='CEN_Y', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.left+self.text_offset, self.top_mid, text='TOP_MID', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.left+self.text_offset, self.bot_mid, text='BOT_MID', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.left+self.text_offset, self.tA, text='tA', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.left+self.text_offset, self.tB, text='tB', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.left+self.text_offset, self.bA, text='bA', fill="#545454", font=('Arial 12'))
    canvas_in.create_text(self.left+self.text_offset, self.bB, text='bB', fill="#545454", font=('Arial 12'))

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
                csig_np.fill_entries_from_matrix(self, prev_mat)
            else:
                print("Prev is not loaded")
        else:
            print("Importing saved")
            csig_np.fill_entries_from_matrix(self, self.matrix_import)

        # Nature probabilities
        for i in range(2):
            self.nature_entry.append(tk.StringVar())
        entryN0 = tk.Entry (root_in, textvariable=self.nature_entry[0], width = self.nature_boxsize)
        canvas_in.create_window(self.cen_x + self.entry_offset, (self.cen_y+self.top_mid)/2, window=entryN0)
        entryN1 = tk.Entry (root_in, textvariable=self.nature_entry[1], width = self.nature_boxsize)
        canvas_in.create_window(self.cen_x + self.entry_offset, (self.cen_y+self.bot_mid)/2, window=entryN1)

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
                    x_offset = self.left_leg-self.entry_offset
                else:
                    x_offset = self.right_leg+self.entry_offset
                canvas_in.create_text(x_offset, y_offset, text=',', fill="black", font=('Arial 15 bold'))
                
                for k in range(2): # tuple
                    entryLeg = tk.Entry (root_in, textvariable=self.entry_list[i][j][k], width=self.payoff_boxsize)
                    if (k == 0):
                        canvas_in.create_window(x_offset -self.mini_offset, y_offset, window=entryLeg)
                    else:
                        canvas_in.create_window(x_offset +self.mini_offset, y_offset, window=entryLeg)

def gen_entry_buttons(self, root, canvas):

    sub_btn=tk.Button(root,text = 'Submit', command = lambda: csig_btn.submit(self))
    canvas.create_window(self.cen_x, self.bot+20, window=sub_btn)

    seperating_btnA=tk.Button(root,text = 'Sepr A', bg = "red", fg = "white", command = lambda: self.seperating_eq(self.matrix, STR_REV, WEK_HID))
    canvas.create_window(self.cen_x+80, self.bot+40,  window=seperating_btnA)
    seperating_btnB=tk.Button(root,text = 'Sepr B', bg = "blue", fg = "white", command = lambda: self.seperating_eq(self.matrix, STR_HID, WEK_REV))
    canvas.create_window(self.cen_x+80, self.bot+80, window=seperating_btnB)
    saved_btn=tk.Button(root,text = 'Load', command = lambda: csig_btn.enter_saved(self))
    canvas.create_window(self.cen_x+160, self.bot+80, window=saved_btn)
    prv2pst_btn=tk.Button(root,text = 'Save', command = lambda: self.transfer_entries_to_saved(self))
    canvas.create_window(self.cen_x +160, self.bot+50, window=prv2pst_btn)
    reset_btn=tk.Button(root,text = 'Reset', command = lambda: csig_btn.reset(self))
    canvas.create_window(self.cen_x, self.bot+50, window=reset_btn)
    quit_btn = tk.Button(root, text="Exit", bg = "#FA8072", command = lambda: csig_btn.quit_game(self, self.root))
    canvas.create_window(self.cen_x, self.bot+80, window=quit_btn)