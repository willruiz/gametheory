import csig_gui     as cg
import csig_btn     as cb
import csig_def     as cd
import csig_np      as cn

import signal_game as sg
from tkinter import *
import tkinter as tk
import math
import numpy as np
import sys

SEPR_INDEX = 0
POOL_INDEX = 1

def draw_eq_base(parent_in,  matrix_in, eq_type):
    subroot = tk.Tk()
    subcan = Canvas(subroot, bg='white')
    subroot.geometry(str(parent_in.width) + "x" + str(parent_in.height))
    inst = EQ_GUI(parent_in)
    
    cg.create_spider_grid(parent_in, subroot, subcan)
    cg.draw_labels(parent_in, subroot, subcan)
    cg.label_grid(parent_in, subroot, subcan)
    quit_btn = tk.Button(subroot, text="Exit", width = 24, height = 4, bg = cd.lite_ornge, command = lambda: cb.quit_game(parent_in, subroot))
    subcan.create_window(parent_in.cen_x, parent_in.bot+60, window=quit_btn)
    if eq_type == SEPR_INDEX:
        inst.draw_sep_logic(parent_in, subroot, subcan, matrix_in)
    else:
        inst.draw_pool_logic(parent_in, subroot, subcan, matrix_in)

def eq_setup(parent_in, matrix_in, top_signal, bot_signal):
    top_sig_alt = 0 if (top_signal == 1) else 1
    bot_sig_alt = 0 if (bot_signal == 1) else 1

    parent_in.top_signal = top_signal
    parent_in.bot_signal = bot_signal
    
    parent_in.top_branch = parent_in.top_index_offset + top_signal
    parent_in.bot_branch = parent_in.bot_index_offset + bot_signal
    print("top_branch:", parent_in.top_branch)
    print("bot_branch:", parent_in.bot_branch)        
    parent_in.top_alt = top_sig_alt
    parent_in.bot_alt = bot_sig_alt
    cn.get_entries_into_matrix(parent_in, matrix_in)
    parent_in.p2_top_choice = -1
    parent_in.p2_top_alt = -1
    parent_in.p2_bot_choice = -1
    parent_in.p2_bot_alt = -1
    parent_in.p1_top_switch = False
    parent_in.p1_bot_switch = False

def pooling_eq(self, matrix_in, top_signal, bot_signal):
    """
        1. Choose case - (need input p and q (signal probablilties determined by nature))
        2. Find U_p2 of each action of player 2 (F or R) (Fight or Retreat)
        3. Check for p1 deviation > if deviate, not pooling [DONE]
        4. If no deviation, find oppoisite signal probability
        5. Find the deviation point for oppositie signal probability
    """
    eq_setup(self, matrix_in, top_signal, bot_signal)
    draw_eq_base(self, matrix_in, POOL_INDEX)

    ## (CASE A): Both choose reveal

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
    eq_setup(self, matrix_in, top_signal, bot_signal)
    
    if (matrix_in[self.top_branch][0][self.index_p2] >= matrix_in[self.top_branch][1][self.index_p2]):
        self.p2_top_choice = 0
        self.p2_top_alt = 1
    else:
        self.p2_top_choice = 1
        self.p2_top_alt = 0

    # Bottom
    # 1. Nature chooses Weak > matrix[2 or 3]
    # 2. Player 1 chooses Hide > matrix[2] ~[2+0]
    # 3. Player 2 Finds maximization matrix[2][0] vs matrix[2][1]
    if (matrix_in[self.bot_branch][0][self.index_p2] >= matrix_in[self.bot_branch][1][self.index_p2]):
        self.p2_bot_choice = 0
        self.p2_bot_alt = 1
        # IF EQUAL, arbitrarily take index zero
    else:
        self.p2_bot_choice = 1
        self.p2_bot_alt = 0
    
    # 4a. TOP: Player 1 then analyses TOP if this is profitable to stay with signal
    # Take the P2's OTHER choice to opposite signal to see if P1 changing current top signal is profitable 
    top_branch_val = matrix_in[self.top_branch][self.p2_top_choice][self.index_p1]
    top_alt_val = matrix_in[self.top_alt + self.top_index_offset][self.p2_bot_choice][self.index_p1]
    bot_branch_val = matrix_in[self.bot_branch][self.p2_bot_choice][self.index_p1]
    bot_alt_val = matrix_in[self.bot_alt + self.bot_index_offset][self.p2_top_choice][self.index_p1]

    self.p1_top_switch = top_branch_val < top_alt_val
    self.p1_bot_switch = bot_branch_val < bot_alt_val

    print("self.p2_top_choice: ",self.p2_top_choice)
    print(matrix_in[self.top_branch][0][self.index_p2])
    print(matrix_in[self.top_branch][1][self.index_p2])
    print("self.p2_bot_choice: ",self.p2_bot_choice)
    print(matrix_in[self.bot_branch][0][self.index_p2])
    print(matrix_in[self.bot_branch][1][self.index_p2])
    print("self.p1_top_switch: ", self.p1_top_switch)
    print("self.p1_bot_switch: ", self.p1_bot_switch)
    draw_eq_base(self, matrix_in, SEPR_INDEX)

class EQ_GUI:
    def __init__(self, parent_in):
        self.parent = parent_in
        self.MO  = parent_in.mini_offset
        self.EO  = parent_in.entry_offset
        self.TO  = parent_in.text_offset
        self.TH  = parent_in.text_height

        self.Atx = parent_in.cen_x + (parent_in.top_signal*2*self.MO)
        self.Aty = parent_in.cen_y # Green branch center point
        self.Btx = parent_in.cen_x + (parent_in.top_signal*2*self.MO)
        self.Bty = parent_in.top_mid # Green branch center cen vert point
        self.Ctx = parent_in.left_mid + (parent_in.top_signal*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.Cty = parent_in.top_mid # Green branch center mid horz point
        self.Abx = parent_in.cen_x + (parent_in.bot_signal*2*self.MO)
        self.Aby = parent_in.cen_y
        self.Bbx = parent_in.cen_x + (parent_in.bot_signal*2*self.MO)
        self.Bby = parent_in.bot_mid
        self.Cbx = parent_in.left_mid + (parent_in.bot_signal*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.Cby = parent_in.bot_mid
        self.TSJ = parent_in.top_signal*2     # Top signal jump
        self.TJP2 = parent_in.p2_top_choice*2   # P2 Top Jump
        
        self.Dtx = parent_in.left_mid + (self.TSJ*parent_in.cf_horz_mid) # Magenta same with self.Ctx without MO
        self.Dty = parent_in.top_mid
        self.Etx = self.Dtx -parent_in.cf_branch_leg +(self.TSJ*parent_in.cf_branch_leg) # Magenta Leg point
        self.Ety = self.Dty -parent_in.offset_leg + (parent_in.p2_top_choice*(2*parent_in.offset_leg))

        self.BSJ = parent_in.bot_signal*2     # Bot signal jump
        self.BJP2 = parent_in.p2_bot_choice*2   # P2 Bot Jump
        self.Dbx = parent_in.left_mid + (self.BSJ*parent_in.cf_horz_mid)
        self.Dby = parent_in.bot_mid
        self.Ebx = self.Dbx -parent_in.cf_branch_leg +(self.BSJ*parent_in.cf_branch_leg)
        self.Eby = self.Dby -parent_in.offset_leg + (parent_in.p2_bot_choice*(2*parent_in.offset_leg))

        self.Ftx = self.Dtx
        self.Fty = parent_in.bot_mid # want Bot
        self.Gtx = self.Etx
        self.Gty = self.Fty -parent_in.offset_leg + (parent_in.p2_top_choice*(2*parent_in.offset_leg))

        self.Fbx = self.Dbx
        self.Fby = parent_in.top_mid # want Top
        self.Gbx = self.Ebx
        self.Gby = self.Fby -parent_in.offset_leg + (parent_in.p2_bot_choice*(2*parent_in.offset_leg))

        self.sigT_offset = 2*self.MO - parent_in.top_signal*4*self.MO
        self.SA_tx = parent_in.left_mid + self.MO + (parent_in.top_signal*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.SB_tx = parent_in.left_mid + self.MO + (parent_in.top_alt*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.Sty = (parent_in.top_mid + parent_in.tA)/2
        
        self.sigB_offset = 2*self.MO - parent_in.bot_signal*4*self.MO
        self.SA_bx = parent_in.left_mid + self.MO + (parent_in.bot_signal*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.SB_bx = parent_in.left_mid + self.MO + (parent_in.bot_alt*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.Sby = (parent_in.bot_mid + parent_in.bB)/2

    def write_eq_payoff(self, parent_in, canvas_in, matrix_in):
        for i in range(4): # Corners
            # i = 0,1 -> Top
            # i = 2,3 -> Bot
            bool_top = i <= 1
            bool_bot = i > 1
            for j in range(2): # up / down
                x_offset = 0
                y_offset = 0
                if (j == 0 and bool_top):
                    y_offset = parent_in.tA
                elif (j == 1 and bool_top):
                    y_offset = parent_in.tB
                elif (j == 0 and bool_bot):
                    y_offset = parent_in.bA
                else:
                    y_offset = parent_in.bB
                if (i % 2 == 0):
                    x_offset = parent_in.left_leg-self.EO
                else:
                    x_offset = parent_in.right_leg+self.EO
                canvas_in.create_text(x_offset, y_offset, text=',', fill="black", font=('Arial 15 bold'))
                
                for k in range(2): # tuple
                    xtext = x_offset -self.MO + 2*k*self.MO
                    # Color in the payoff of p1 to compare if switching 
                    if(k == 0 and 
                        ((bool_top and j == parent_in.p2_top_choice and parent_in.top_signal == i) 
                      or (bool_bot and j == parent_in.p2_bot_choice and parent_in.bot_signal == i-2)
                      or (bool_top and j == parent_in.p2_bot_choice    and parent_in.top_alt    == i)
                      or (bool_bot and j == parent_in.p2_top_choice    and parent_in.bot_alt    == i-2)
                    )):
                        canvas_in.create_text(xtext, y_offset, text=str(matrix_in[i][j][k]), fill=cd.dark_red, font=('Arial 15 bold'))
                    else:
                        canvas_in.create_text(xtext, y_offset, text=str(matrix_in[i][j][k]), fill="black", font=('Arial 15 bold'))

    def draw_sep_logic(self, parent_in, root_in, canvas_in, matrix_in):
        self.write_eq_payoff(parent_in, canvas_in, matrix_in)
        # 1. Draw branch re-sets (solid curved arrows)- signals
        #- Arrows
        # Top
        print("parent_in.bot_branch:", parent_in.bot_branch)
        canvas_in.create_line(self.Atx-self.MO, self.Aty-self.MO, self.Btx-self.MO, self.Bty+self.MO, fill="lime green", width ='3')
        canvas_in.create_line(self.Btx-self.MO, self.Bty+self.MO, self.Ctx+self.MO, self.Cty+self.MO, fill="lime green", width ='3',arrow=tk.LAST)

        # Bot
        canvas_in.create_line(self.Abx-self.MO, self.Aby+self.MO, self.Bbx-self.MO, self.Bby-self.MO, fill="lime green", width ='3')
        canvas_in.create_line(self.Bbx-self.MO, self.Bby-self.MO, self.Cbx+self.MO, self.Cby-self.MO, fill="lime green", width ='3',arrow=tk.LAST)

        # 2. Draw P2 payoffs given signal choices 
        # (solid colored arrows) and (highlight rectangles)
        ## TOP MAGENTA
        canvas_in.create_line(self.Dtx, self.Dty-self.MO+self.TJP2*self.MO, self.Etx , self.Ety-self.MO+self.TJP2*self.MO, fill=cd.rglr_magnta, width ='8',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (self.Etx-self.MO)+self.TSJ*self.MO, self.Ety-self.TH, 
            (self.Etx-2*(self.EO-self.MO/2))+self.TSJ*(2*(self.EO-self.MO/2)), self.Ety+self.TH, 
            outline='red', width = '3')

        ## TOP-ALT
        canvas_in.create_line(self.Ftx, self.Fty-self.MO+self.TJP2*self.MO, self.Gtx , self.Gty-self.MO+self.TJP2*self.MO, fill=cd.pale_magnta, width ='5',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (self.Gtx-self.MO)+self.TSJ*self.MO,                        self.Gty-self.TH, 
            (self.Gtx-2*(self.EO-self.MO/2))+self.TSJ*(2*(self.EO-self.MO/2)),    self.Gty+self.TH, 
            outline=cd.pale_red, width = '2')

        ## BOT MAGENTA
        canvas_in.create_line(self.Dbx, self.Dby-self.MO+self.BJP2*self.MO, self.Ebx , self.Eby-self.MO+self.BJP2*self.MO, fill=cd.rglr_magnta, width ='8',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (self.Ebx-self.MO)+self.BSJ*self.MO, self.Eby-self.TH, 
            (self.Ebx-2*(self.EO-self.MO/2))+self.BSJ*(2*(self.EO-self.MO/2)), self.Eby+self.TH, 
            outline='red', width = '3')

        ## BOT-ALT
        canvas_in.create_line(self.Fbx, self.Fby-self.MO+self.BJP2*self.MO, self.Gbx , self.Gby-self.MO+self.BJP2*self.MO, fill=cd.pale_magnta, width ='5',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (self.Gbx-self.MO)+self.BSJ*self.MO, self.Gby-self.TH, 
            (self.Gbx-2*(self.EO-self.MO/2))+self.BSJ*(2*(self.EO-self.MO/2)), self.Gby+self.TH, 
            outline=cd.pale_red, width = '2')
        # 3. Label or draw if P1 decides to swithc signals
        # (Dotted rectangles) and (highlight rectangles)
        ## Use text to indeicate no switch
        ## Highlight payoofs being compared.
        ## Use text and arrows to indeicate switch
        
        if(parent_in.p1_top_switch):
            canvas_in.create_line(self.SA_tx, self.Sty, self.SB_tx, self.Sty, fill=cd.rglr_gold, width ='5',arrow=tk.LAST, arrowshape=(14,15,8))
        else:
            canvas_in.create_text(self.SA_tx + 2*self.sigT_offset, self.Sty, text="No Deviation",fill=cd.rglr_gold, font=('Arial 15 bold'))
        if(parent_in.p1_bot_switch):
            canvas_in.create_line(self.SA_bx, self.Sby, self.SB_bx, self.Sby, fill=cd.rglr_gold, width ='5',arrow=tk.LAST, arrowshape=(14,15,8))
        else:
            canvas_in.create_text(self.SA_bx + 2*self.sigB_offset, self.Sby, text="No Deviation",fill=cd.rglr_gold, font=('Arial 15 bold'))
        
        ## Write out text to indicate if this is a successful seperating equlibrium and store in self class
        if(not parent_in.p1_top_switch and  not parent_in.p1_bot_switch):
            canvas_in.create_rectangle(
            parent_in.cen_x-self.EO*2, parent_in.bB-self.MO, 
            parent_in.cen_x+self.EO*2, parent_in.bB+self.TO, 
            outline='orange', width = '3')
            canvas_in.create_text(parent_in.cen_x, parent_in.bB, text="Seperating",fill="orange", font=('Arial 15 bold'))
            canvas_in.create_text(parent_in.cen_x, parent_in.bB+self.MO, text="Equilibrium",fill="orange", font=('Arial 15 bold'))
        else:
            canvas_in.create_rectangle(
            parent_in.cen_x-self.EO*2, parent_in.bB-self.MO, 
            parent_in.cen_x+self.EO*2, parent_in.bB+self.TO, 
            outline='orange', width = '3')
            canvas_in.create_text(parent_in.cen_x, parent_in.bB, text="Not Seperating",fill="orange", font=('Arial 15 bold'))
            canvas_in.create_text(parent_in.cen_x, parent_in.bB+self.MO, text="Equilibrium",fill="orange", font=('Arial 15 bold'))

    def draw_pool_logic(self, parent_in, root_in, canvas_in, matrix_in):
        pass
