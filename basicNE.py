from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys

class NFM:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.width = cols*200+100
        self.height = rows*200+100
        self.left = self.width * 0.2
        self.right = self.width * 0.8
        self.top = self.height * 0.2
        self.bot = self.height * 0.8
        self.unit_width = (self.right-self.left)/cols
        self.unit_height = (self.bot-self.top)/rows
        self.cenv = self.width * 0.5
        self.cenh = self.height * 0.5
        self.root = tk.Tk()
        self.offset = 20
        self.canvas = Canvas(self.root, bg='white')
        self.entry_list = []
        self.matrix = np.zeros((1,1), dtype='i,i')
        self.saved_file = "saved_matrix.npy"
        self.saved_dim = "saved_dim.npy"
        self.prev_file = "prev_matrix.npy" 
        self.prev_dim = "prev_dim.npy"
        self.matrix_import = np.zeros((1,1), dtype='i,i')
        self.matrix_import_bool = False


    def create_matrix_grid(self, root_in, canvas_in):
        root_in.geometry(str(self.width) + "x" + str(self.height))
        print("width: ", self.width)
        print("height: ", self.height)

        canvas_in.create_line(self.left, self.top, self.right, self.top, fill="black", width ='5')
        canvas_in.create_line(self.left, self.top, self.left, self.bot, fill="black", width ='5')
        canvas_in.create_line(self.right, self.top, self.right, self.bot, fill="black", width ='5')
        canvas_in.create_line(self.left, self.bot, self.right, self.bot, fill="black", width ='5')

        for i in range(self.cols-1):
            divs_v = self.left+self.unit_width* (i+1)
            canvas_in.create_line(divs_v, self.top, divs_v, self.bot, fill="black", width ='5')

        for j in range(self.rows-1):
            divs_h = self.top+self.unit_height * (j+1)
            canvas_in.create_line(self.left, divs_h, self.right, divs_h, fill="black", width ='5')
        
        canvas_in.pack(fill=BOTH, expand=1)

    def fill_entries_from_matrix(self, matrix_in):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    if (str(matrix_in[i][j][k]) == '0'):
                        k_entry.set("")    
                    else:
                        k_entry.set(str(matrix_in[i][j][k]))

    def create_entry_boxes(self, canvas):
        for i in range(self.rows):
            entry_row = []
            for j in range(self.cols):
                entry_row.append((tk.StringVar(), tk.StringVar()))
            self.entry_list.append(entry_row)

        if (not self.matrix_import_bool):
            prev_mat = np.load(self.prev_file)
            if ((prev_mat.shape[0] == self.rows) and (prev_mat.shape[1] == self.cols)):
                self.fill_entries_from_matrix(prev_mat)
            else:
                print("Prev is not loaded")
        else:
            self.fill_entries_from_matrix(self.matrix_import)
            

        initH_offset = self.top + self.unit_height/2
        initW_offset = self.left+self.unit_width/2
        for i in range(self.rows):
            for j in range(self.cols):
                coord_x = initW_offset+(self.unit_width*(j))
                coord_y = initH_offset+(self.unit_height*(i))
                entryA0 = tk.Entry (self.root, textvariable=self.entry_list[i][j][0], width= 4)
                canvas.create_window(coord_x-self.offset, coord_y, window=entryA0)
                entryA1 = tk.Entry (self.root, textvariable=self.entry_list[i][j][1], width= 4)
                canvas.create_window(coord_x+self.offset, coord_y, window=entryA1)

    def show_payoffs(self, canvas, p1_br, p2_br):
        initH_offset = self.top+self.unit_height/2
        initW_offset = self.left+self.unit_width/2
        for i in range(self.rows):
            for j in range(self.cols):
                coord_x = initW_offset+(self.unit_width*(j))
                coord_y = initH_offset+(self.unit_height*(i))
                if (p1_br[i][j]):
                    canvas.create_rectangle(coord_x-self.offset-10, coord_y-10, 
                        coord_x-self.offset+15, coord_y+10, fill='#FFCCCB')
                if (p2_br[i][j]):
                    canvas.create_rectangle(coord_x+self.offset-10, coord_y-10, 
                        coord_x+self.offset+15, coord_y+10, fill='#ADD8E6')
                canvas.create_text(coord_x-self.offset, coord_y, 
                    text=self.matrix[i][j][0], fill="black", font=('Helvetica 15 bold'))
                canvas.create_text(coord_x, coord_y, 
                    text=',', fill="black", font=('Helvetica 15 bold'))
                canvas.create_text(coord_x+self.offset, coord_y, 
                    text=self.matrix[i][j][1], fill="black", font=('Helvetica 15 bold'))

    def import_matrix(self, matrix_in):
        self.matrix_import = matrix_in
        self.matrix_import_bool = True


    def find_basic_BR(self): # return index coordinates of BRs
        # Player 1 (going down each column)
        match_p1 = np.zeros((self.rows, self.cols), dtype=bool)
        match_p2 = np.zeros((self.rows, self.cols), dtype=bool)
        for i in range(self.matrix.shape[1]): # increment right
            local_br_val = (-1*sys.maxsize)-1
            curr_col = (self.matrix[:,i])
            curr_col_indexed = [x[0] for x in curr_col]
            for j in range(self.matrix.shape[0]): # scan down
                curr = self.matrix[j][i][0]
                if (curr > local_br_val):
                    local_br_val = curr
            comp_col = np.zeros((1, self.rows))
            comp_col.fill(local_br_val)
            bool_col = (curr_col_indexed == comp_col)
            for x in range(match_p1.shape[0]):
                match_p1[x,i] = bool_col[0][x]
        
        # Player 2 (going right each row)
        for i in range(self.matrix.shape[0]): # increment down
            local_br_val = (-1*sys.maxsize)-1
            curr_row = (self.matrix[i,:])
            curr_row_indexed = [x[1] for x in curr_row]
            for j in range(self.matrix.shape[1]): # scan right
                curr = self.matrix[i][j][1]
                if (curr > local_br_val):
                    local_br_val = curr
            #print("p2 br: ", local_br_val)
            comp_row = np.zeros((1, self.cols))
            comp_row.fill(local_br_val)
            bool_row = (curr_row_indexed == comp_row)
            for x in range(match_p1.shape[0]):
                match_p2[i,x] = bool_row[0][x]

        return match_p1, match_p2
    def get_entries_into_matrix(self):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    str_input =k_entry.get()
                    input = 0
                    if (str_input == ''):
                        input = 0
                    else:
                        input = int(str_input)
                    self.matrix[i][j][k] = input

    def reset(self):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    k_entry.set("")
                    self.matrix[i][j][k] = 0
        print("RESET")
        np.save(self.prev_file, self.matrix)

    def quit_game(self):
        np.save(self.prev_file, self.matrix)
        print("EXIT")
        self.root.destroy()

    def enter_saved(self):
        entry = np.load(self.saved_file)
        if ((entry.shape[0] == self.rows) and (entry.shape[1] == self.cols)):
            self.matrix = entry
            self.fill_entries_from_matrix(entry)
            print("LOADED")
        else:
            print("Saved dimensions do not match - Cannot load")
    
    def transfer_entries_to_saved(self):
        self.get_entries_into_matrix()
        np.save(self.saved_file, self.matrix)
        print("SAVED")

    def init_np(self):
        self.matrix = np.resize(self.matrix, (self.rows, self.cols))

    def gen_payoff_buttons(self, root, canvas):
        quit_btn = tk.Button(root, text="Exit", command=root.destroy)
        canvas.create_window(self.cenv, self.bot+80, window=quit_btn)

    def gen_BR_grid(self, match_p1, match_p2):
        subroot = tk.Tk()
        subcan = Canvas(subroot, bg='white')
        self.create_matrix_grid(subroot, subcan)
        self.show_payoffs(subcan, match_p1, match_p2)
        self.gen_payoff_buttons(subroot, subcan)
        subroot.mainloop()

    def submit(self):
        for i, i_entry in enumerate(self.entry_list):
            for j, j_entry in enumerate(i_entry):
                for k, k_entry in enumerate(j_entry): # iterate through tuple
                    str_input =k_entry.get()
                    input = 0
                    if (str_input == ''):
                        input = 0
                    else:
                        input = int(str_input)
                    self.matrix[i][j][k] = input
                    #print(matrix)
        print("SUBMIT")
        np.save(self.prev_file, self.matrix)

        p1_br, p2_br = self.find_basic_BR()
        self.gen_BR_grid(p1_br, p2_br)
        

    def gen_entry_buttons(self, root, canvas):
        
        sub_btn=tk.Button(root,text = 'Submit', command = lambda: self.submit())
        canvas.create_window(self.cenv, self.bot+20, window=sub_btn)
        saved_btn=tk.Button(root,text = 'Load', command = lambda: self.enter_saved())
        canvas.create_window(self.cenv+160, self.bot+80, window=saved_btn)
        prv2pst_btn=tk.Button(root,text = 'Save', command = lambda: self.transfer_entries_to_saved())
        canvas.create_window(self.cenv +160, self.bot+40, window=prv2pst_btn)
        reset_btn=tk.Button(root,text = 'Reset', command = lambda: self.reset())
        canvas.create_window(self.cenv, self.bot+50, window=reset_btn)
        quit_btn = tk.Button(root, text="Exit", command = lambda: self.quit_game())
        #quit_btn = tk.Button(root, text="Exit", command=root.destroy)
        canvas.create_window(self.cenv, self.bot+80, window=quit_btn)

# def main():
#     parent = NFM(rows, cols)
#     parent.init_np()
#     parent.create_matrix_grid(parent.root, parent.canvas)
#     parent.create_entry_boxes(parent.canvas)
#     parent.gen_entry_buttons(parent.root, parent.canvas)
#     parent.root.mainloop()

# if __name__ == '__main__':
#     main()