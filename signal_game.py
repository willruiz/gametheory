from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys
import csig_gui
import csig_np
import csig_btn
import csig_sep

STR_HID = 0
STR_REV = 1
WEK_HID = 0
WEK_REV = 1

class SGE:
    def __init__(self):
        ## Dimensions
        self.rows = 4
        self.cols = 2
        self.width = 1200
        self.height = 900

        ## TKinter Classes
        self.root = tk.Tk()
        self.canvas = Canvas(self.root, bg='white')
        ## Base Coordinates
        self.left = self.width * 0.01
        self.right = self.width * 0.99
        self.top = self.height * 0.03
        self.bot = self.height * 0.85
        self.cen_x = self.width * 0.5
        self.cen_y_norm = self.height * 0.5
        self.cen_y = (self.top+self.bot) * 0.5 

        ## Distances
        self.cf_vert_mid = self.height * 0.25
        self.cf_horz_mid = self.width * 0.25
        self.cf_full_leg   = self.width * 0.35
        self.cf_branch_leg = self.width * 0.1

        self.top_mid = self.cen_y - self.cf_vert_mid
        self.bot_mid = self.cen_y + self.cf_vert_mid 
        self.left_mid = self.cen_x - self.cf_horz_mid  #self.width * 0.25
        self.right_mid = self.cen_x + self.cf_horz_mid

        self.offset_leg = self.height * 0.10
        self.left_leg = self.cen_x - self.cf_full_leg
        self.right_leg = self.cen_x + self.cf_full_leg

        self.tA = self.top_mid-self.offset_leg
        self.tB = self.top_mid+self.offset_leg
        self.bA = self.bot_mid-self.offset_leg
        self.bB = self.bot_mid+self.offset_leg

        ## Offsets
        self.entry_offset = self.width * 0.05
        self.text_offset  = self.width * 0.03
        self.mini_offset  = self.width * 0.015
        self.text_height = self.height * 0.04
        self.nature_boxsize = 6
        self.payoff_boxsize = 3

        self.dr = self.height * 0.01 # dr = dot radius

        # Data structures
        self.nature_entry = [] # Dimensions [2]
        self.nature_mat = np.zeros((1,2))
        self.matrix = np.zeros((4,2), dtype='i,i')
        self.entry_list = [] # Dimensions [4][2][2]
        self.p1_payoff_deviation = np.zeros((2,2))

        # Save files
        self.saved_file = "saved_matrix_sg.npy"
        self.saved_dim = "saved_dim_sg.npy"
        self.prev_file = "prev_matrix_sg.npy" 
        self.prev_dim = "prev_dim_sg.npy"
        self.nature_file = "nature_sg.npy"
        self.nature_prev = "nature_prev_sg.npy"
        self.matrix_import = np.zeros((4,2), dtype='i,i')
        self.matrix_import_bool = False

        # Matrix indexing
        self.top_index_offset = 0
        self.bot_index_offset = 2

    def write_sep_payoff(self, canvas_in, matrix_in):
        MO  = self.mini_offset      # mini_offset
        EO  = self.entry_offset

        for i in range(4): # Corners
            # i = 0,1 -> Top
            # i = 2,3 -> Bot
            bool_top = i <= 1
            bool_bot = i > 1
            for j in range(2): # up / down
                x_offset = 0
                y_offset = 0
                if (j == 0 and bool_top):
                    y_offset = self.tA
                elif (j == 1 and bool_top):
                    y_offset = self.tB
                elif (j == 0 and bool_bot):
                    y_offset = self.bA
                else:
                    y_offset = self.bB
                if (i % 2 == 0):
                    x_offset = self.left_leg-self.entry_offset
                else:
                    x_offset = self.right_leg+self.entry_offset
                canvas_in.create_text(x_offset, y_offset, text=',', fill="black", font=('Arial 15 bold'))
                
                for k in range(2): # tuple
                    xtext = 0
                    if (k == 0):
                        xtext = x_offset -self.mini_offset
                    else:
                        xtext = x_offset +self.mini_offset

                    # Color in the payoff of p1 to compare if switching 
                    if(k == 0 and 
                      ((bool_top and j == self.p2_top_choice and self.top_signal == i) 
                    or (bool_bot and j == self.p2_bot_choice and self.bot_signal == i-2)
                    or (bool_top and j == self.p2_top_alt    and self.top_alt    == i)
                    or (bool_bot and j == self.p2_bot_alt    and self.bot_alt    == i-2)
                    )):
                        canvas_in.create_text(xtext, y_offset, text=str(matrix_in[i][j][k]), fill="#db3052", font=('Arial 15 bold'))
                    else:
                        canvas_in.create_text(xtext, y_offset, text=str(matrix_in[i][j][k]), fill="black", font=('Arial 15 bold'))

    def draw_sep_logic(self, root_in, canvas_in, matrix_in):
        ### Use colored rectangles, solid arrows, and dotted arrows
        # X. Text out payoffs
        MO  = self.mini_offset      # mini_offset
        EO  = self.entry_offset
        TO  = self.text_offset

        self.write_sep_payoff(canvas_in, matrix_in)

        # 1. Draw branch re-sets (solid curved arrows)- signals
        #- Arrows
        # Top
        print("self.bot_branch:", self.bot_branch)
        
        Atx = self.cen_x + (self.top_signal*2*MO)
        Aty = self.cen_y # Green branch center point
        Btx = self.cen_x + (self.top_signal*2*MO)
        Bty = self.top_mid # Green branch center cen vert point
        Ctx = self.left_mid + (self.top_signal*((2*self.cf_horz_mid)-(2*self.mini_offset)))
        Cty = self.top_mid # Green branch center mid horz point
        
        canvas_in.create_line(Atx-MO, Aty-MO, Btx-MO, Bty+MO, fill="lime green", width ='3')
        canvas_in.create_line(Btx-MO, Bty+MO, Ctx+MO, Cty+MO, fill="lime green", width ='3',arrow=tk.LAST)

        # Bot
        Abx = self.cen_x + (self.bot_signal*2*MO)
        Aby = self.cen_y
        Bbx = self.cen_x + (self.bot_signal*2*MO)
        Bby = self.bot_mid
        Cbx = self.left_mid + (self.bot_signal*((2*self.cf_horz_mid)-(2*self.mini_offset)))
        Cby = self.bot_mid
        
        canvas_in.create_line(Abx-MO, Aby+MO, Bbx-MO, Bby-MO, fill="lime green", width ='3')
        canvas_in.create_line(Bbx-MO, Bby-MO, Cbx+MO, Cby-MO, fill="lime green", width ='3',arrow=tk.LAST)

        # 2. Draw P2 payoffs given signal choices 
        # (solid colored arrows) and (highlight rectangles)

        ## TOP MAGENTA
        TSJ = self.top_signal*2     # Top signal jump
        TJP2 = self.p2_top_choice*2   # P2 Top Jump
        
        Dtx = self.left_mid + (TSJ*self.cf_horz_mid) # Magenta same with Ctx without mini_offset
        Dty = self.top_mid
        Etx = Dtx -self.cf_branch_leg +(TSJ*self.cf_branch_leg) # Magenta Leg point
        Ety = Dty -self.offset_leg + (self.p2_top_choice*(2*self.offset_leg))
        
        canvas_in.create_line(Dtx, Dty-MO+TJP2*MO, Etx , Ety-MO+TJP2*MO, fill="#ff5fff", width ='8',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (Etx-MO)+TSJ*MO, Ety-self.text_height, 
            (Etx-2*(EO-MO/2))+TSJ*(2*(EO-MO/2)), Ety+self.text_height, 
            outline='red', width = '3')

        ## TOP-ALT
        TAP2 = self.p2_top_alt
        Ftx = Dtx
        Fty = self.bot_mid # want Bot
        Gtx = Etx
        Gty = Fty -self.offset_leg + (self.p2_top_choice*(2*self.offset_leg))
        canvas_in.create_line(Ftx, Fty-MO+TJP2*MO, Gtx , Gty-MO+TJP2*MO, fill="#fdddff", width ='5',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (Gtx-MO)+TSJ*MO,                        Gty-self.text_height, 
            (Gtx-2*(EO-MO/2))+TSJ*(2*(EO-MO/2)),    Gty+self.text_height, 
            outline='#ffdddd', width = '2')

        ## BOT MAGENTA
        BSJ = self.bot_signal*2     # Bot signal jump
        BJP2 = self.p2_bot_choice*2   # P2 Bot Jump
        # Magenta same with Ctx without mini_offset
        Dbx = self.left_mid + (BSJ*self.cf_horz_mid)
        Dby = self.bot_mid
        Ebx = Dbx -self.cf_branch_leg +(BSJ*self.cf_branch_leg)
        Eby = Dby -self.offset_leg + (self.p2_bot_choice*(2*self.offset_leg))

        canvas_in.create_line(Dbx, Dby-MO+BJP2*MO, Ebx , Eby-MO+BJP2*MO, fill="#ff5fff", width ='8',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (Ebx-MO)+BSJ*MO, Eby-self.text_height, 
            (Ebx-2*(EO-MO/2))+BSJ*(2*(EO-MO/2)), Eby+self.text_height, 
            outline='red', width = '3')

        ## BOT-ALT
        Fbx = Dbx
        Fby = self.top_mid # want Top
        Gbx = Ebx
        Gby = Fby -self.offset_leg + (self.p2_bot_choice*(2*self.offset_leg))
        canvas_in.create_line(Fbx, Fby-MO+BJP2*MO, Gbx , Gby-MO+BJP2*MO, fill="#fdddff", width ='5',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (Gbx-MO)+BSJ*MO, Gby-self.text_height, 
            (Gbx-2*(EO-MO/2))+BSJ*(2*(EO-MO/2)), Gby+self.text_height, 
            outline='#ffdddd', width = '2')
        # 3. Label or draw if P1 decides to swithc signals
        # (Dotted rectangles) and (highlight rectangles)
        ## Use text to indeicate no switch
        ## Highlight payoofs being compared.
        ## Use text and arrows to indeicate switch
        sigT_offset = 2*MO - self.top_signal*3*MO
        SAtx = self.left_mid + MO - self.top_signal*2*MO + (self.top_signal*((2*self.cf_horz_mid)-(2*self.mini_offset)))
        SBtx = self.left_mid + MO - self.top_alt*2*MO + (self.top_alt*((2*self.cf_horz_mid)-(2*self.mini_offset)))
        Sty = (self.top_mid + self.tA)/2
        
        sigB_offset = 2*MO - self.bot_signal*3*MO
        SAbx = self.left_mid + MO - self.bot_signal*2*MO + (self.bot_signal*((2*self.cf_horz_mid)-(2*self.mini_offset)))
        SBbx = self.left_mid + MO - self.bot_alt*2*MO + (self.bot_alt*((2*self.cf_horz_mid)-(2*self.mini_offset)))
        Sby = (self.bot_mid + self.bB)/2
        if(self.p1_top_switch):
            canvas_in.create_line(SAtx, Sty, SBtx, Sty, fill="#b8a200", width ='5',arrow=tk.LAST, arrowshape=(14,15,8))
        else:
            canvas_in.create_text(SAtx + 2*sigT_offset, Sty, text="No Deviation",fill="#b8a200", font=('Arial 15 bold'))
        if(self.p1_bot_switch):
            canvas_in.create_line(SAbx, Sby, SBbx, Sby, fill="#b8a200", width ='5',arrow=tk.LAST, arrowshape=(14,15,8))
        else:
            canvas_in.create_text(SAbx + 2*sigB_offset, Sby, text="No Deviation",fill="#b8a200", font=('Arial 15 bold'))
        
        ## Write out text to indicate if this is a successful seperating equlibrium and store in self class
        if(not self.p1_top_switch and  not self.p1_bot_switch):
            canvas_in.create_rectangle(
            self.cen_x-EO*2, self.bB-MO, 
            self.cen_x+EO*2, self.bB+TO, 
            outline='orange', width = '3')

            canvas_in.create_text(self.cen_x, self.bB, text="Seperating",fill="orange", font=('Arial 15 bold'))
            canvas_in.create_text(self.cen_x, self.bB+MO, text="Equilibrium",fill="orange", font=('Arial 15 bold'))
        else:
            canvas_in.create_rectangle(
            self.cen_x-EO*2, self.bB-MO, 
            self.cen_x+EO*2, self.bB+TO, 
            outline='orange', width = '3')

            canvas_in.create_text(self.cen_x, self.bB, text="Not Seperating",fill="orange", font=('Arial 15 bold'))
            canvas_in.create_text(self.cen_x, self.bB+MO, text="Equilibrium",fill="orange", font=('Arial 15 bold'))


    def draw_sep_base(self,  matrix_in):
        subroot = tk.Tk()
        subcan = Canvas(subroot, bg='white')
        
        subroot.geometry(str(self.width) + "x" + str(self.height))
        self.draw_sep_logic(subroot, subcan, matrix_in)
        csig_gui.create_spider_grid(self, subroot, subcan)
        csig_gui.draw_labels(self, subroot, subcan)
        csig_gui.label_grid(self, subroot, subcan)
        quit_btn = tk.Button(subroot, text="Exit", bg = "#FA8072", command = lambda: csig_btn.quit_game(self, subroot))
        subcan.create_window(self.cen_x, self.bot+80, window=quit_btn)

    def seperating_eq(self, matrix_in, top_signal, bot_signal):
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
        top_sig_alt = 0 if (top_signal == 1) else 1
        bot_sig_alt = 0 if (bot_signal == 1) else 1

        self.top_signal = top_signal
        self.bot_signal = bot_signal
        
        self.top_branch = self.top_index_offset + top_signal
        self.bot_branch = self.bot_index_offset + bot_signal
        print("top_branch:", self.top_branch)
        print("bot_branch:", self.bot_branch)        
        self.top_alt = top_sig_alt
        self.bot_alt = bot_sig_alt
        
        p1_index = 0
        p2_index = 1
        csig_np.get_entries_into_matrix(self, matrix_in)
        
        self.p2_top_choice = -1
        self.p2_top_alt = -1
        if (matrix_in[self.top_branch][0][p2_index] >= matrix_in[self.top_branch][1][p2_index]):
            self.p2_top_choice = 0
            self.p2_top_alt = 1
        elif (matrix_in[self.top_branch][0][p2_index] < matrix_in[self.top_branch][1][p2_index]):
            self.p2_top_choice = 1
            self.p2_top_alt = 0
        # else: # equal 
        #     self.p2_top_choice = 0

        print("self.p2_top_choice: ",self.p2_top_choice)

        print(matrix_in[self.top_branch][0][p2_index])
        print(matrix_in[self.top_branch][1][p2_index])

        # Bottom
        # 1. Nature chooses Weak > matrix[2 or 3]
        # 2. Player 1 chooses Hide > matrix[2] ~[2+0]
        # 3. Player 2 Finds maximization matrix[2][0] vs matrix[2][1]
        
        self.p2_bot_choice = -1
        self.p2_bot_alt = -1
        if (matrix_in[self.bot_branch][0][p2_index] >= matrix_in[self.bot_branch][1][p2_index]):
            self.p2_bot_choice = 0
            self.p2_bot_alt = 1
            # IF EQUAL, arbitrarily take index zero
        elif (matrix_in[self.bot_branch][0][p2_index] < matrix_in[self.bot_branch][1][p2_index]):
            self.p2_bot_choice = 1
            self.p2_bot_alt = 0
        # else: # equal 
        #     self.p2_top_choice = 0

        print("self.p2_bot_choice: ",self.p2_bot_choice)

        print(matrix_in[self.bot_branch][0][p2_index])
        print(matrix_in[self.bot_branch][1][p2_index])

        # 4a. TOP: Player 1 then analyses TOP if this is profitable to stay with signal
        self.p1_top_switch = False

        # Take the P2's OTHER choice to opposite signal to see if P1 changing current top signal is profitable 
        top_branch_val = matrix_in[self.top_branch][self.p2_top_choice][p1_index]
        top_alt_val = matrix_in[self.top_alt + self.top_index_offset][self.p2_bot_choice][p1_index]

        if (top_branch_val > top_alt_val):
            self.p1_top_switch = False
        elif (top_branch_val < top_alt_val):
            self.p1_top_switch = True
        else:
            self.p1_top_switch = False
        print("self.p1_top_switch: ", self.p1_top_switch)
        # 4b. BOTTOM: Player 1 then analyses BOTTOM if this is profitable to stay with signal
        self.p1_bot_switch = False
        bot_branch_val = matrix_in[self.bot_branch][self.p2_bot_choice][p1_index]
        bot_alt_val = matrix_in[self.bot_alt + self.bot_index_offset][self.p2_top_choice][p1_index]

        if (bot_branch_val > bot_alt_val):
            self.p1_bot_switch = False
        elif (bot_branch_val < bot_alt_val):
            self.p1_bot_switch = True
        else:
            self.p1_bot_switch = False

        print("self.p1_bot_switch: ", self.p1_bot_switch)

        self.draw_sep_base(matrix_in)
    
    ## Incomplete 
    def pooling_eq(self, matrix_in, top_signal, bot_signal):
        # 1. Choose case - (need input p and q (signal probablilties determined by nature))
        # 2. Find U_p2 of each action of player 2 (F or R) (Fight or Retreat)
        # 3. Check for p1 deviation > if deviate, not pooling [DONE]
        # 4. If no deviation, find oppoisite signal probability
        # 5. Find the deviation point for oppositie signal probability
        top_sig_alt = 0 if (top_signal == 1) else 1
        bot_sig_alt = 0 if (bot_signal == 1) else 1

        self.top_signal = top_signal
        self.bot_signal = bot_signal   

def main():
    parent = SGE()
    csig_gui.create_spider_grid(parent, parent.root, parent.canvas)
    csig_gui.label_grid(parent, parent.root, parent.canvas)
    csig_gui.create_entry_boxes(parent, parent.root, parent.canvas)
    csig_gui.gen_entry_buttons(parent, parent.root, parent.canvas)
    csig_gui.draw_labels(parent, parent.root, parent.canvas)
    parent.root.mainloop()

if __name__ == '__main__':
    main()