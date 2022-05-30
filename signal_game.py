from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys

class SGE:
    def __init__(self):
        self.rows = 4
        self.cols = 2
        self.width = 1200
        self.height = 800
        self.root = tk.Tk()
        self.canvas = Canvas(self.root, bg='white')
        self.left = self.width * 0.01
        self.right = self.width * 0.99
        self.top = self.height * 0.03
        self.bot = self.height * 0.85
        self.cen_x = self.width * 0.5
        self.cen_y_norm = self.height * 0.5
        self.cen_y = (self.top+self.bot) * 0.5 

        self.bot_mid = self.bot - self.height * 0.15
        self.top_mid = self.top + self.height * 0.15
        self.left_mid = self.width * 0.25
        self.right_mid = self.width * 0.75

        self.offset_leg = self.height * 0.10
        self.left_leg = self.width * 0.15
        self.right_leg = self.width * 0.85

        self.entry_offset = self.width * 0.05
        self.mini_offset = self.width * 0.015
        self.nature_boxsize = 6
        self.payoff_boxsize = 3

        self.dr = self.height * 0.01 # dr = dot radius

        self.nature_entry = [] # Dimensions [2]
        self.nature_mat = np.zeros((1,2))
        self.matrix = np.zeros((4,2), dtype='i,i')
        self.entry_list = [] # Dimensions [4][2][2]

        self.saved_file = "saved_matrix_sg.npy"
        self.saved_dim = "saved_dim_sg.npy"
        self.prev_file = "prev_matrix_sg.npy" 
        self.prev_dim = "prev_dim_sg.npy"
        self.nature_file = "nature_sg.npy"
        self.nature_prev = "nature_prev_sg.npy"
        self.matrix_import = np.zeros((4,2), dtype='i,i')
        self.matrix_import_bool = False
    
    def import_matrix(self, matrix_in): # FOR CUSTOM MATRIX INPUT FOR TEST SUITE
        self.matrix_import = matrix_in
        self.matrix_import_bool = True






    def seperating_eq(self, matrix_in):
        """
        Process for seperating equilibrium:
        X. Select case (A) [Strong > Reveal] [Weak > Hide]
        1. Nature chooses {Strong}
        2. Player 1 then chooses signal {Reveal}
        3. Player 2 chooses Fight or Quit with the best payoff P2   
        4. Player 1 then analyses P2's choice and the decides 
        if he has a higher payoff if he switches his signal
        """
        # (Case A) 
        # Top
        # 1. Nature chooses Strong > matrix[0 or 1]
        # 2. Player 1 chooses Reveal > matrix[1] ~[0+1]
        # 3. Player 2 Finds maximization matrix[1][0] vs matrix[1][1]
        top_index_offset = 0
        bot_index_offset = 2
        top_signal = 1
        bot_signal = 0
        top_sig_alt = 0 if (top_signal == 1) else 1
        bot_sig_alt = 0 if (bot_signal == 1) else 1
        
        top_branch = top_index_offset + top_signal
        bot_branch = bot_index_offset + bot_signal
        top_alt = top_index_offset + top_sig_alt
        bot_alt = bot_index_offset + bot_sig_alt
        
        p1_index = 0
        p2_index = 1
        self.get_entries_into_matrix(matrix_in)
        
        p2_top_choice = -1
        p2_top_alt = -1
        if (matrix_in[top_branch][0][p2_index] > matrix_in[top_branch][1][p2_index]):
            p2_top_choice = 0
            p2_top_alt = 1
        elif (matrix_in[top_branch][0][p2_index] < matrix_in[top_branch][1][p2_index]):
            p2_top_choice = 1
            p2_top_alt = 0
        else: # equal 
            p2_top_choice = 2

        print("p2_top_choice: ",p2_top_choice)

        print(matrix_in[top_branch][0][p2_index])
        print(matrix_in[top_branch][1][p2_index])

        # Bottom
        # 1. Nature chooses Weak > matrix[2 or 3]
        # 2. Player 1 chooses Hide > matrix[2] ~[2+0]
        # 3. Player 2 Finds maximization matrix[2][0] vs matrix[2][1]
        
        p2_bot_choice = -1
        p2_bot_alt = -1
        if (matrix_in[bot_branch][0][p2_index] > matrix_in[bot_branch][1][p2_index]):
            p2_bot_choice = 0
            p2_bot_alt = 1
        elif (matrix_in[bot_branch][0][p2_index] < matrix_in[bot_branch][1][p2_index]):
            p2_bot_choice = 1
            p2_bot_alt = 0
        else: # equal 
            p2_top_choice = 2

        print("p2_bot_choice: ",p2_bot_choice)

        print(matrix_in[bot_branch][0][p2_index])
        print(matrix_in[bot_branch][1][p2_index])

        # 4a. TOP: Player 1 then analyses TOP if this is profitable to stay with signal
        p1_top_switch = False
        if (p2_top_choice != 2):
            # Take the P2's OTHER choice to opposite signal to see if P1 changing current top signal is profitable 
            print("checkA")
            print("top_alt:",top_alt)
            print("top_branch_val:", matrix_in[top_branch][p2_top_choice][p1_index])
            print("top_alt_val:",matrix_in[top_alt][p2_top_choice][p1_index])
            if (matrix_in[top_branch][p2_top_choice][p1_index] > matrix_in[top_alt][p2_bot_choice][p1_index]):
                p1_top_switch = False
            elif (matrix_in[top_branch][p2_top_choice][p1_index] < matrix_in[top_alt][p2_bot_choice][p1_index]):
                p1_top_switch = True
            else:
                p1_top_switch = False
        else: # since both have same payoff, arbitrarily pick index 0
            print("checkB")
            if (matrix_in[top_branch][0][p1_index] > matrix_in[top_alt][0][p1_index]):
                p1_top_switch = False
            elif (matrix_in[top_branch][0][p1_index] < matrix_in[top_alt][0][p1_index]):
                p1_top_switch = True
            else:
                p1_top_switch = False
        print("p1_top_switch: ", p1_top_switch)

        # 4b. BOTTOM: Player 1 then analyses BOTTOM if this is profitable to stay with signal
        p1_bot_switch = False
        if (p2_bot_choice != 2):
            print("checkA")
            print("bot_alt:",top_alt)
            print("bot_branch_val:", matrix_in[bot_branch][p2_bot_choice][p1_index])
            print("bot_alt_val:", matrix_in[bot_alt][p2_top_choice][p1_index])
            # Take the P2's OTHER choice to opposite signal to see if P1 changing current top signal is profitable 
            if (matrix_in[bot_branch][p2_bot_choice][p1_index] > matrix_in[bot_alt][p2_top_choice][p1_index]):
                p1_bot_switch = False
            elif (matrix_in[bot_branch][p2_bot_choice][p1_index] < matrix_in[bot_alt][p2_top_choice][p1_index]):
                p1_bot_switch = True
            else:
                p1_bot_switch = False
        else: # since both have same payoff, arbitrarily pick index 0
            print("checkB")
            if (matrix_in[bot_branch][0][p1_index] > matrix_in[bot_alt][0][p1_index]):
                p1_bot_switch = False
            elif (matrix_in[bot_branch][0][p1_index] < matrix_in[bot_alt][0][p1_index]):
                p1_bot_switch = True
            else:
                p1_bot_switch = False
        print("p1_bot_switch: ", p1_bot_switch)



    def draw_labels(self, root_in, canvas_in):
        canvas_in.create_text(self.cen_x-self.entry_offset, (self.cen_y+self.top_mid)/2, text='Strong', fill="blue", font=('Arial 15 bold'))
        canvas_in.create_text(self.cen_x-self.entry_offset, (self.cen_y+self.bot_mid)/2, text='Weak', fill="blue", font=('Arial 15 bold'))
        canvas_in.create_text((self.cen_x + self.left_mid)/2, self.top_mid-self.mini_offset, text='Hide', fill="black", font=('Arial 15 bold'))
        canvas_in.create_text((self.cen_x + self.right_mid)/2, self.top_mid-self.mini_offset, text='Reveal', fill="black", font=('Arial 15 bold'))
        canvas_in.create_text((self.cen_x + self.left_mid)/2, self.bot_mid-self.mini_offset, text='Hide', fill="black", font=('Arial 15 bold'))
        canvas_in.create_text((self.cen_x + self.right_mid)/2, self.bot_mid-self.mini_offset, text='Reveal', fill="black", font=('Arial 15 bold'))

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
        tA = self.top_mid-self.offset_leg
        tB = self.top_mid+self.offset_leg
        bA = self.bot_mid-self.offset_leg
        bB = self.bot_mid+self.offset_leg
        canvas_in.create_line(self.left_mid, self.top_mid, self.left_leg, tA, fill="black", width ='4')
        canvas_in.create_line(self.left_mid, self.top_mid, self.left_leg, tB, fill="black", width ='4')
        canvas_in.create_line(self.right_mid, self.top_mid, self.right_leg, tA, fill="black", width ='4')
        canvas_in.create_line(self.right_mid, self.top_mid, self.right_leg, tB, fill="black", width ='4')

        # Spider-Legs - Bot
        canvas_in.create_line(self.left_mid, self.bot_mid, self.left_leg, bA, fill="black", width ='4')
        canvas_in.create_line(self.left_mid, self.bot_mid, self.left_leg, bB, fill="black", width ='4')
        canvas_in.create_line(self.right_mid, self.bot_mid, self.right_leg, bA, fill="black", width ='4')
        canvas_in.create_line(self.right_mid, self.bot_mid, self.right_leg, bB, fill="black", width ='4')
        canvas_in.pack(fill=BOTH, expand=1)

    def fill_entries_from_matrix(self, matrix_in):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    # if (str(matrix_in[i][j][k]) == '0'):
                    #     k_entry.set("")    
                    # else:
                    k_entry.set(str(matrix_in[i][j][k]))

    def get_entries_into_matrix(self, matrix_in):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    str_input =k_entry.get()
                    input = 0
                    if (str_input == ''):
                        input = 0
                    else:
                        input = int(str_input)
                    matrix_in[i][j][k] = input

    def create_entry_boxes(self, root_in, canvas_in):
        tA = self.top_mid-self.offset_leg
        tB = self.top_mid+self.offset_leg
        bA = self.bot_mid-self.offset_leg
        bB = self.bot_mid+self.offset_leg

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
                self.fill_entries_from_matrix(prev_mat)
            else:
                print("Prev is not loaded")
        else:
            print("Importing saved")
            self.fill_entries_from_matrix(self.matrix_import)

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
                    y_offset = tA
                elif (j == 1 and i <= 1):
                    y_offset = tB
                elif (j == 0 and i > 1):
                    y_offset = bA
                else:
                    y_offset = bB
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
    
    def enter_saved(self):
        entry = np.load(self.saved_file)
        if ((entry.shape[0] == self.rows) and (entry.shape[1] == self.cols)):
            self.matrix = entry
            self.fill_entries_from_matrix(entry)
            print("LOADED")
        else:
            print("Saved dimensions do not match - Cannot load")

    def transfer_entries_to_saved(self):
        self.get_entries_into_matrix(self.matrix)
        np.save(self.saved_file, self.matrix)
        print("SAVED")
    
    def submit(self):
        self.get_entries_into_matrix(self.matrix)
        print(self.matrix)
        print("SUBMIT")
        np.save(self.prev_file, self.matrix)


    def reset(self):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    k_entry.set("")
                    self.matrix[i][j][k] = 0
        self.nature_entry = [0,0]
        print("RESET")
        np.save(self.prev_file, self.matrix)

    def quit_game(self):
        self.get_entries_into_matrix(self.matrix)
        print(self.matrix)
        np.save(self.prev_file, self.matrix)
        print("EXIT")
        self.root.destroy()
        
    def gen_entry_buttons(self, root, canvas):
    
        sub_btn=tk.Button(root,text = 'Submit', command = lambda: self.submit())
        canvas.create_window(self.cen_x, self.bot+20, window=sub_btn)

        seperating_btn=tk.Button(root,text = 'Sepr', command = lambda: self.seperating_eq(self.matrix))
        canvas.create_window(self.cen_x+80, self.bot+80, window=seperating_btn)

        saved_btn=tk.Button(root,text = 'Load', command = lambda: self.enter_saved())
        canvas.create_window(self.cen_x+160, self.bot+80, window=saved_btn)
        prv2pst_btn=tk.Button(root,text = 'Save', command = lambda: self.transfer_entries_to_saved())
        canvas.create_window(self.cen_x +160, self.bot+50, window=prv2pst_btn)
        reset_btn=tk.Button(root,text = 'Reset', command = lambda: self.reset())
        canvas.create_window(self.cen_x, self.bot+50, window=reset_btn)
        quit_btn = tk.Button(root, text="Exit", command = lambda: self.quit_game())
        canvas.create_window(self.cen_x, self.bot+80, window=quit_btn)


def main():
    parent = SGE()
    parent.create_spider_grid(parent.root, parent.canvas)
    parent.create_entry_boxes(parent.root, parent.canvas)
    parent.gen_entry_buttons(parent.root, parent.canvas)
    parent.draw_labels(parent.root, parent.canvas)
    parent.root.mainloop()

if __name__ == '__main__':
    main()