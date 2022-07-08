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
from sympy import symbols, Eq, solve



def draw_eq_base(parent_in,  matrix_in, eq_type):
    subroot = tk.Tk()
    subcan = Canvas(subroot, bg='white')
    subroot.geometry(str(parent_in.width) + "x" + str(parent_in.height))
    inst = EQ_GUI(parent_in)
    
    cg.create_spider_grid(parent_in, subroot, subcan)
    cg.draw_labels(parent_in, subroot, subcan)
    cg.label_grid(parent_in, subroot, subcan)
    quit_btn = tk.Button(subroot, text="Exit", width = 24, height = 4, bg = cd.lite_ornge, command = lambda: cb.quit_game(parent_in, subroot))
    inst.draw_logic_sequence(parent_in, subcan, matrix_in, eq_type)
    subcan.create_window(parent_in.cen_x, parent_in.bot+60, window=quit_btn)
    inst.draw_logic_sequence(parent_in, subcan, matrix_in, eq_type)

def eq_setup(parent_in, matrix_in, top_signal, bot_signal):
    parent_in.top_sig_alt = 0 if (top_signal == 1) else 1
    parent_in.bot_sig_alt = 0 if (bot_signal == 1) else 1

    parent_in.top_signal = top_signal
    parent_in.bot_signal = bot_signal
    
    parent_in.top_branch = top_signal + parent_in.top_index_offset
    parent_in.bot_branch = bot_signal + parent_in.bot_index_offset
    if parent_in.debug_on:
        print("top_branch:", parent_in.top_branch)
        print("bot_branch:", parent_in.bot_branch)        
    parent_in.top_alt = parent_in.top_sig_alt + parent_in.top_index_offset
    parent_in.bot_alt = parent_in.bot_sig_alt + parent_in.bot_index_offset
    cn.get_entries_into_matrix(parent_in, matrix_in)
    cn.get_nature_entries_into_Natrix(parent_in, parent_in.nature_mat)
    parent_in.p2_top_choice = -1
    parent_in.p2_top_alt = -1
    parent_in.p2_bot_choice = -1
    parent_in.p2_bot_alt = -1
    parent_in.p1_top_switch = False
    parent_in.p1_bot_switch = False
    parent_in.eq_success    = False

def pooling_eq(parent_in, matrix_in, nature_in, top_signal, bot_signal):
    """
        1. Choose case - (need input p and q (signal probablilties determined by nature))
        2. Find Bayesian payoffs U_p2 of each action of player 2 (F or R) (Fight or Retreat)
        3. Check for p1 deviation > if deviate, not pooling [DONE]
        4. If no deviation, find oppoisite signal probability
        5. Find the deviation point for oppositie signal probability
    """
    # Step 1: Case is determined by parameter signal inputs
    assert(top_signal == bot_signal)
    eq_setup(parent_in, matrix_in, top_signal, bot_signal)

    # Step 2: Find Bayesian payoffs - start with saving nature entries [DONE]
    p  = nature_in[0][0]
    pn = nature_in[0][1]
    p2_pool1_top = matrix_in[parent_in.top_branch][parent_in.action1_p2][parent_in.index_p2]
    p2_pool1_bot = matrix_in[parent_in.bot_branch][parent_in.action1_p2][parent_in.index_p2]
    p2_pool2_top = matrix_in[parent_in.top_branch][parent_in.action2_p2][parent_in.index_p2]
    p2_pool2_bot = matrix_in[parent_in.bot_branch][parent_in.action2_p2][parent_in.index_p2]
    parent_in.p2_pool1 = (p2_pool1_top*p) + (p2_pool1_bot*pn)
    parent_in.p2_pool2 = (p2_pool2_top*p) + (p2_pool2_bot*pn)
    

    parent_in.p2_pool_action = 0 if (parent_in.p2_pool1 >= parent_in.p2_pool2) else 1
    parent_in.p2_top_choice = parent_in.p2_pool_action
    parent_in.p2_bot_choice = parent_in.p2_pool_action
    parent_in.p2_top_alt = 0 if (parent_in.p2_pool_action == 1) else 1
    parent_in.p2_bot_alt = parent_in.p2_top_alt

    if parent_in.debug_on:
        print("p2_pool1:", parent_in.p2_pool1)
        print("p2_pool2:", parent_in.p2_pool2)
        print("p2_pool_action:", parent_in.p2_pool_action)
    
    # Steo 3: Check to see if p1 will deviate
    p1_pool_top = matrix_in[parent_in.top_branch][parent_in.p2_pool_action][parent_in.index_p1]
    p1_pool_bot = matrix_in[parent_in.bot_branch][parent_in.p2_pool_action][parent_in.index_p1]
    

    p2_pool1_alt_top = matrix_in[parent_in.top_alt][parent_in.action1_p2][parent_in.index_p2]
    p2_pool1_alt_bot = matrix_in[parent_in.bot_alt][parent_in.action1_p2][parent_in.index_p2]
    p2_pool2_alt_top = matrix_in[parent_in.top_alt][parent_in.action2_p2][parent_in.index_p2]
    p2_pool2_alt_bot = matrix_in[parent_in.bot_alt][parent_in.action2_p2][parent_in.index_p2]
    parent_in.p2_pool1_alt = (p2_pool1_alt_top*p) + (p2_pool1_alt_bot*pn)
    parent_in.p2_pool2_alt = (p2_pool2_alt_top*p) + (p2_pool2_alt_bot*pn)

    parent_in.p2_pool_act_alt = 0 if (parent_in.p2_pool1_alt >= parent_in.p2_pool2_alt) else 1

    p1_alt_top  = matrix_in[parent_in.top_alt][parent_in.p2_pool_act_alt][parent_in.index_p1]
    p1_alt_bot  = matrix_in[parent_in.bot_alt][parent_in.p2_pool_act_alt][parent_in.index_p1]

    parent_in.p1_top_switch = (p1_alt_top > p1_pool_top) 
    parent_in.p1_bot_switch = (p1_alt_bot > p1_pool_bot)
    parent_in.p1_pool_deviation = parent_in.p1_top_switch or parent_in.p1_bot_switch 
    
    # Step 4: If no deviation, find probability q
    
    if (not parent_in.p1_pool_deviation):
        p2_alt1_top  = matrix_in[parent_in.top_alt][parent_in.action1_p2][parent_in.index_p2]
        p2_alt1_bot  = matrix_in[parent_in.bot_alt][parent_in.action1_p2][parent_in.index_p2]
        p2_alt2_top  = matrix_in[parent_in.top_alt][parent_in.action2_p2][parent_in.index_p2]
        p2_alt2_bot  = matrix_in[parent_in.bot_alt][parent_in.action2_p2][parent_in.index_p2]
        q = symbols('q')
        exprA = q*p2_alt1_top + (1-q)*p2_alt1_bot
        exprB = q*p2_alt2_top + (1-q)*p2_alt2_bot

        
        raw_sol = solve(Eq(exprA, exprB),q)
        parent_in.solution = 0.0
        parent_in.solution_flag = False
        if(bool(raw_sol)):
            parent_in.solution = round(float(raw_sol[0]),3) 
            parent_in.solution_flag = True
        else:
            if (parent_in.msg_on):
                print("[Undefined alternate probability solution]")
        if parent_in.debug_on:
            print(exprA)
            print(exprB)
            print(parent_in.solution)

    draw_eq_base(parent_in, matrix_in, parent_in.POOL_INDEX)

def seperating_eq(parent_in, matrix_in, top_signal, bot_signal):
    """
    Process for seperating equilibrium:
    X. Select case (A) [Strong > Reveal] [Weak > Hide]
    1. Nature chooses {Strong}
    2. Player 1 then chooses signal {Reveal}
    3. Player 2 chooses Fight or Quit with the best payoff P2   
    4. Player 1 then analyses P2's choice and the decides 
    if he has a higher payoff if he switches his signal
    """
    # Top
    # 1. Nature chooses Strong > matrix[0 or 1]
    # 2. Player 1 chooses Reveal > matrix[1] ~[0+1]
    # 3. Player 2 Finds maximization matrix[1][0] vs matrix[1][1]
    assert(top_signal != bot_signal)
    eq_setup(parent_in, matrix_in, top_signal, bot_signal)

    p2_sepr1_top = matrix_in[parent_in.top_branch][parent_in.action1_p2][parent_in.index_p2]
    p2_sepr1_bot = matrix_in[parent_in.bot_branch][parent_in.action1_p2][parent_in.index_p2]
    p2_sepr2_top = matrix_in[parent_in.top_branch][parent_in.action2_p2][parent_in.index_p2]
    p2_sepr2_bot = matrix_in[parent_in.bot_branch][parent_in.action2_p2][parent_in.index_p2]

    parent_in.p2_top_choice = 0 if (p2_sepr1_top >= p2_sepr2_top) else 1
    parent_in.p2_top_alt = 1 if (parent_in.p2_top_choice == 0) else 1

    parent_in.p2_bot_choice = 0 if (p2_sepr1_bot >= p2_sepr2_bot) else 1
    parent_in.p2_bot_alt = 1 if (parent_in.p2_bot_choice == 0) else 1
    
    # 4a. TOP: Player 1 then analyses TOP if this is profitable to stay with signal
    # Take the P2's OTHER choice to opposite signal to see if P1 changing current top signal is profitable 
    top_branch_val = matrix_in[parent_in.top_branch][parent_in.p2_top_choice][parent_in.index_p1]
    top_alt_val = matrix_in[parent_in.top_alt][parent_in.p2_bot_choice][parent_in.index_p1]
    bot_branch_val = matrix_in[parent_in.bot_branch][parent_in.p2_bot_choice][parent_in.index_p1]
    bot_alt_val = matrix_in[parent_in.bot_alt][parent_in.p2_top_choice][parent_in.index_p1]

    parent_in.p1_top_switch = top_branch_val < top_alt_val
    parent_in.p1_bot_switch = bot_branch_val < bot_alt_val
    draw_eq_base(parent_in, matrix_in, parent_in.SEPR_INDEX)


class EQ_GUI:
    def __init__(self, parent_in):
        self.parent = parent_in
        self.MO  = parent_in.mini_offset
        self.HMO = parent_in.mini_offset/2
        self.EO  = parent_in.entry_offset
        self.TO  = parent_in.text_offset
        self.TH  = parent_in.text_height

        # GREEN SIGNAL
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

        # MAIN-RED
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

        # ALT-BLUE
        self.Ftx = self.Dtx          
        self.Fty = parent_in.bot_mid # want Bot
        self.Gtx = self.Etx
        self.Gty = self.Fty -parent_in.offset_leg + (parent_in.p2_top_choice*(2*parent_in.offset_leg))

        self.Fbx = self.Dbx
        self.Fby = parent_in.top_mid # want Top
        self.Gbx = self.Ebx
        self.Gby = self.Fby -parent_in.offset_leg + (parent_in.p2_bot_choice*(2*parent_in.offset_leg))

        # DEVIATION-GOLD
        self.sigT_offset = 2*self.MO - parent_in.top_signal*4*self.MO
        self.SA_tx = parent_in.left_mid + self.MO + (parent_in.top_signal*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.SB_tx = parent_in.left_mid + self.MO + (parent_in.top_sig_alt*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.Sty = (parent_in.top_mid + parent_in.tA)/2
        
        self.sigB_offset = 2*self.MO - parent_in.bot_signal*4*self.MO
        self.SA_bx = parent_in.left_mid + self.MO + (parent_in.bot_signal*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.SB_bx = parent_in.left_mid + self.MO + (parent_in.bot_sig_alt*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.Sby = (parent_in.bot_mid + parent_in.bB)/2

    def pool_adjust_vars(self, parent_in):
        self.TAJ = parent_in.top_sig_alt*2    # Top sig alt jump
        self.BAJ = parent_in.bot_sig_alt*2    # Bot sig alt jump
        self.PAAP2 = parent_in.p2_pool_act_alt * 2

        self.Ftx = parent_in.left_mid + (self.TAJ*parent_in.cf_horz_mid) # done
        self.Fty = self.Dty # done
        self.Gtx = self.Ftx -parent_in.cf_branch_leg +(self.TAJ*parent_in.cf_branch_leg) # Magenta Leg point
        self.Gty = self.Dty -parent_in.offset_leg + (parent_in.p2_pool_act_alt*(2*parent_in.offset_leg))

        self.Fbx = parent_in.left_mid + (self.BAJ*parent_in.cf_horz_mid) # done
        self.Fby = self.Dby # done
        self.Gbx = self.Ftx -parent_in.cf_branch_leg +(self.BAJ*parent_in.cf_branch_leg) # Magenta Leg point
        self.Gby = self.Fby -parent_in.offset_leg + (parent_in.p2_pool_act_alt*(2*parent_in.offset_leg))

        self.sigT_offset = 2*self.MO - parent_in.top_signal*4*self.MO
        self.SA_tx = parent_in.left_mid + self.MO + (parent_in.top_signal*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.SB_tx = parent_in.left_mid + self.MO + (parent_in.top_sig_alt*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        self.Sty = (parent_in.top_mid + parent_in.tA)/2
        
        # self.sigB_offset = 2*self.MO - parent_in.bot_signal*4*self.MO
        # self.SA_bx = parent_in.left_mid + self.MO + (parent_in.bot_signal*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        # self.SB_bx = parent_in.left_mid + self.MO + (parent_in.bot_sig_alt*((2*parent_in.cf_horz_mid)-(2*self.MO)))
        # self.Sby = (parent_in.bot_mid + parent_in.bB)/2

    
    def write_eq_payoff(self, parent_in, canvas_in, matrix_in, type_in):
        canvas_in.create_text(parent_in.cen_x+parent_in.entry_offset, (parent_in.cen_y+parent_in.top_mid)/2,
            text=str(parent_in.nature_mat[0][0]), fill=cd.rglr_cyan, font=(cd.text_font))
        canvas_in.create_text(parent_in.cen_x+parent_in.entry_offset, (parent_in.cen_y+parent_in.bot_mid)/2,
            text=str(parent_in.nature_mat[0][1]), fill=cd.rglr_cyan, font=(cd.text_font))

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
                canvas_in.create_text(x_offset, y_offset, text=',', fill="black", font=(cd.text_font))
                
                for k in range(2): # tuple
                    xtext = x_offset -self.MO + 2*k*self.MO
                    pay_fill = ""
                    if(k == 0 and type_in == parent_in.SEPR_INDEX and
                        ((bool_top and j == parent_in.p2_top_choice and parent_in.top_signal  == i - parent_in.top_index_offset) 
                      or (bool_top and j == parent_in.p2_bot_choice and parent_in.top_sig_alt == i - parent_in.top_index_offset)
                      or (bool_bot and j == parent_in.p2_bot_choice and parent_in.bot_signal  == i - parent_in.bot_index_offset)
                      or (bool_bot and j == parent_in.p2_top_choice and parent_in.bot_sig_alt == i - parent_in.bot_index_offset)
                    )):
                        pay_fill = cd.dark_red
                    elif(k == 0 and type_in == parent_in.POOL_INDEX and
                        ((bool_top and j == parent_in.p2_top_choice and parent_in.top_signal  == i - parent_in.top_index_offset) 
                      or (bool_top and j == parent_in.p2_pool_act_alt and parent_in.top_sig_alt == i - parent_in.top_index_offset)
                      or (bool_bot and j == parent_in.p2_bot_choice and parent_in.bot_signal  == i - parent_in.bot_index_offset)
                      or (bool_bot and j == parent_in.p2_pool_act_alt and parent_in.bot_sig_alt == i - parent_in.bot_index_offset)
                    )):
                        pay_fill = cd.dark_red
                    elif(k == 1 and
                        ((bool_top and j == parent_in.p2_top_choice and parent_in.top_signal == i - parent_in.top_index_offset)
                      or (bool_bot and j == parent_in.p2_bot_choice and parent_in.bot_signal == i - parent_in.bot_index_offset) 
                    )):
                        pay_fill = cd.dark_purple
                    elif(k == 1 and
                        ((bool_top and j == parent_in.p2_top_alt and parent_in.top_signal == i - parent_in.top_index_offset)
                      or (bool_bot and j == parent_in.p2_bot_alt and parent_in.bot_signal == i - parent_in.bot_index_offset) 
                    )):
                        pay_fill = cd.dark_purple
                    else:
                        pay_fill = "black"
                    canvas_in.create_text(xtext, y_offset, text=str(matrix_in[i][j][k]), fill=pay_fill, font=(cd.text_font))


    def draw_sig_arrows(self, canvas_in):
        canvas_in.create_line(self.Atx-self.MO, self.Aty-self.MO, self.Btx-self.MO, self.Bty+self.MO, fill="lime green", width ='5')
        canvas_in.create_line(self.Btx-self.MO, self.Bty+self.MO, self.Ctx+self.MO, self.Cty+self.MO, fill="lime green", width ='5',arrow=tk.LAST, arrowshape=(14,15,8))

        # Bot
        canvas_in.create_line(self.Abx-self.MO, self.Aby+self.MO, self.Bbx-self.MO, self.Bby-self.MO, fill="lime green", width ='5')
        canvas_in.create_line(self.Bbx-self.MO, self.Bby-self.MO, self.Cbx+self.MO, self.Cby-self.MO, fill="lime green", width ='5',arrow=tk.LAST, arrowshape=(14,15,8))

    def draw_p2choice(self, parent_in, canvas_in, type_in):
        p2c_offset_top = 0
        p2c_offset_bot = 0
        if (type_in == parent_in.SEPR_INDEX):
            p2c_offset_top = self.TSJ
            p2c_offset_bot = self.BSJ 
            p2c_offset_alt_top = self.TJP2
            p2c_offset_alt_bot = self.BJP2
        else:
            p2c_offset_top = self.TAJ
            p2c_offset_bot = self.BAJ 
            p2c_offset_alt_top = self.PAAP2
            p2c_offset_alt_bot = self.PAAP2 

        # 2. Draw P2 payoffs given signal choices 
        ## TOP MAGENTA
        canvas_in.create_line(self.Dtx, self.Dty-self.HMO+self.TJP2*self.HMO, self.Etx , self.Ety-self.HMO+self.TJP2*self.HMO, fill=cd.reg_magnta, width ='8',arrow=tk.LAST, arrowshape=(14,15,8))
        canvas_in.create_rectangle(
            (self.Etx-self.MO)+self.TSJ*self.MO,                               self.Ety-self.TH, 
            (self.Etx-2*(self.EO-self.MO/2))+self.TSJ*(2*(self.EO-self.MO/2)), self.Ety+self.TH, 
            outline='red', width = '3')

        # ## TOP-ALT
        canvas_in.create_line(self.Ftx, self.Fty-self.HMO+p2c_offset_alt_top*self.HMO, self.Gtx , self.Gty-self.HMO+p2c_offset_alt_top*self.HMO, fill=cd.pale_blue, width ='5',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (self.Gtx-self.MO)+ p2c_offset_top*self.MO,                              self.Gty-self.TH, 
            (self.Gtx-2*(self.EO-self.MO/2))+p2c_offset_top*(2*(self.EO-self.MO/2)), self.Gty+self.TH, 
            outline='blue', width = '2')

        ## BOT MAGENTA
        canvas_in.create_line(self.Dbx, self.Dby-self.HMO+self.BJP2*self.HMO, self.Ebx , self.Eby-self.HMO+self.BJP2*self.HMO, fill=cd.reg_magnta, width ='8',arrow=tk.LAST, arrowshape=(14,15,8))
        canvas_in.create_rectangle(
            (self.Ebx-self.MO)+self.BSJ*self.MO,                               self.Eby-self.TH, 
            (self.Ebx-2*(self.EO-self.MO/2))+self.BSJ*(2*(self.EO-self.MO/2)), self.Eby+self.TH, 
            outline='red', width = '3')

        # ## BOT-ALT
        canvas_in.create_line(self.Fbx, self.Fby-self.HMO+p2c_offset_alt_bot*self.HMO, self.Gbx , self.Gby-self.HMO+p2c_offset_alt_bot*self.HMO, fill=cd.pale_blue, width ='5',arrow=tk.LAST)
        canvas_in.create_rectangle(
            (self.Gbx-self.MO)+p2c_offset_bot*self.MO,                               self.Gby-self.TH, 
            (self.Gbx-2*(self.EO-self.MO/2))+p2c_offset_bot*(2*(self.EO-self.MO/2)), self.Gby+self.TH, 
            outline='blue', width = '2')

    def check_deviation(self, parent_in, canvas_in):
        if(parent_in.p1_top_switch):
            canvas_in.create_line(self.SA_tx, self.Sty, self.SB_tx, self.Sty, fill=cd.rglr_gold, width ='5',arrow=tk.LAST, arrowshape=(14,15,8))
        else:
            canvas_in.create_text(self.SA_tx + 2*self.sigT_offset, self.Sty, text="No Deviation",fill=cd.rglr_gold, font=(cd.text_font))
        if(parent_in.p1_bot_switch):
            canvas_in.create_line(self.SA_bx, self.Sby, self.SB_bx, self.Sby, fill=cd.rglr_gold, width ='5',arrow=tk.LAST, arrowshape=(14,15,8))
        else:
            canvas_in.create_text(self.SA_bx + 2*self.sigB_offset, self.Sby, text="No Deviation",fill=cd.rglr_gold, font=(cd.text_font))
    def output_eq_result(self, parent_in, canvas_in, type_ind):
        text_type = ""
        fill_type = ""
        if(type_ind == parent_in.SEPR_INDEX):
            text_type = "Seperating"
        else: #self.POOL_INDEX
            text_type = "Pooling"
        if(not parent_in.p1_top_switch and  not parent_in.p1_bot_switch):
            parent_in.eq_success = True
            fill_type = cd.success_green
        else:
            parent_in.eq_success = False
            text_type = "Not " + text_type
            fill_type = cd.fail_red
        canvas_in.create_rectangle(
            parent_in.cen_x-self.EO*2, parent_in.bB-self.MO, 
            parent_in.cen_x+self.EO*2, parent_in.bB+self.TO, 
            outline = fill_type, width = '3')
        canvas_in.create_text(parent_in.cen_x, parent_in.bB,         text=text_type         ,fill = fill_type, font=(cd.text_font))
        canvas_in.create_text(parent_in.cen_x, parent_in.bB+self.MO, text="Equilibrium"     ,fill = fill_type, font=(cd.text_font))

    def write_pool_prob(self, parent_in, canvas_in):                                                           # signal == top_signal == bot_signal
        pool_text_x  = ((parent_in.left+parent_in.left_leg*2)/3)-self.EO*0.5 + 2*(parent_in.cf_full_leg+self.TO*2-0.4*self.MO)*parent_in.top_signal 
        pool_text_xb = ((parent_in.left+parent_in.left_leg*2)/3)+self.EO*0.4 + 2*(parent_in.cf_full_leg+self.TO*2-0.1*self.MO)*parent_in.top_signal
        top_pool_text_y  = parent_in.cen_y-self.EO*0.5
        top_pool_text_yb = parent_in.cen_y-self.MO*0.1
        bot_pool_text_y  = parent_in.cen_y+self.MO*0.1
        bot_pool_text_yb = parent_in.cen_y+self.EO*0.5

        if (parent_in.p2_pool1 >= parent_in.p2_pool2):
            canvas_in.create_rectangle(pool_text_x, top_pool_text_y, pool_text_xb, top_pool_text_yb, outline = cd.lite_red, width = '2')
            canvas_in.create_line((parent_in.left_leg*3+parent_in.left_mid)/4+self.MO + (2*(parent_in.cf_full_leg)-self.TO*2.6) *parent_in.top_signal,  parent_in.cen_y+self.MO*1.5, 
                                   parent_in.left_leg-self.MO +                         (2*(parent_in.cf_full_leg)+self.TO*1.25) *parent_in.top_signal, parent_in.cen_y-self.MO*0.75, 
                                   fill=cd.lite_magnta, width ='7',arrow=tk.LAST)
        else:
            canvas_in.create_rectangle(pool_text_x, bot_pool_text_y, pool_text_xb, bot_pool_text_yb, outline = cd.lite_red, width = '2')
            canvas_in.create_line((parent_in.left_leg*3+parent_in.left_mid)/4+self.MO + (2*(parent_in.cf_full_leg)-self.TO*2.5) *parent_in.top_signal,  parent_in.cen_y-self.MO*2, 
                                   parent_in.left_leg-self.MO                         + (2*(parent_in.cf_full_leg)+self.TO*1.25) *parent_in.top_signal, parent_in.cen_y+self.MO*0.5, 
                                  fill=cd.lite_magnta, width ='7',arrow=tk.LAST)
        
        canvas_in.create_text( ((parent_in.left+parent_in.left_leg*2)/3)-self.MO*0.2 + 2*(parent_in.cf_full_leg+self.TO*2-0.2*self.MO)*parent_in.top_signal, parent_in.cen_y-self.EO/4, 
            text=str(round(parent_in.p2_pool1,1)), fill = cd.lite_purple, font=(cd.text_font))
        canvas_in.create_text( ((parent_in.left+parent_in.left_leg*2)/3)-self.MO*0.2 + 2*(parent_in.cf_full_leg+self.TO*2-0.2*self.MO)*parent_in.top_signal, parent_in.cen_y+self.EO/4, 
            text=str(round(parent_in.p2_pool2,1)), fill = cd.lite_purple, font=(cd.text_font))

        pool_text_x_alt  = ((parent_in.left+parent_in.left_leg*2)/3)-self.EO*0.5 + 2*(parent_in.cf_full_leg+self.TO*2-0.4*self.MO)*parent_in.top_alt
        pool_text_xb_alt = ((parent_in.left+parent_in.left_leg*2)/3)+self.EO*0.4 + 2*(parent_in.cf_full_leg+self.TO*2-0.1*self.MO)*parent_in.top_alt

        if (parent_in.p2_pool1_alt >= parent_in.p2_pool2_alt):
            canvas_in.create_rectangle(pool_text_x_alt, top_pool_text_y, pool_text_xb_alt, top_pool_text_yb, outline = cd.lite_blue, width = '2')
            canvas_in.create_line((parent_in.left_leg*3+parent_in.left_mid)/4+self.MO + (2*(parent_in.cf_full_leg)-self.TO*2.6)  *parent_in.top_alt, parent_in.cen_y+self.MO*1.5, 
                                   parent_in.left_leg-self.MO +                         (2*(parent_in.cf_full_leg)+self.TO*1.25) *parent_in.top_alt, parent_in.cen_y-self.MO*0.75, 
                                   fill=cd.pale_blue, width ='7',arrow=tk.LAST)
        else:
            canvas_in.create_rectangle(pool_text_x_alt, bot_pool_text_y, pool_text_xb_alt, bot_pool_text_yb, outline = cd.lite_blue, width = '2')
            canvas_in.create_line((parent_in.left_leg*3+parent_in.left_mid)/4+self.MO + (2*(parent_in.cf_full_leg)-self.TO*2.5)  *parent_in.top_alt, parent_in.cen_y-self.MO*2, 
                                   parent_in.left_leg-self.MO                         + (2*(parent_in.cf_full_leg)+self.TO*1.25) *parent_in.top_alt, parent_in.cen_y+self.MO*0.5, 
                                  fill=cd.pale_blue, width ='7',arrow=tk.LAST)
        
        canvas_in.create_text( ((parent_in.left+parent_in.left_leg*2)/3)-self.MO*0.2 + 2*(parent_in.cf_full_leg+self.TO*2-0.2*self.MO)*parent_in.top_alt, parent_in.cen_y-self.EO/4, 
            text=str(round(parent_in.p2_pool1_alt,1)), fill = cd.lite_purple, font=(cd.text_font))
        canvas_in.create_text( ((parent_in.left+parent_in.left_leg*2)/3)-self.MO*0.2 + 2*(parent_in.cf_full_leg+self.TO*2-0.2*self.MO)*parent_in.top_alt, parent_in.cen_y+self.EO/4, 
            text=str(round(parent_in.p2_pool2_alt,1)), fill = cd.lite_purple, font=(cd.text_font))

        if((not parent_in.p1_top_switch) and (not parent_in.p1_bot_switch)):
            canvas_in.create_rectangle(
                (parent_in.cen_x*2+parent_in.right_mid)/3+self.EO*0.8, parent_in.bB-self.MO, 
                (parent_in.cen_x+parent_in.right_mid*2)/3+self.EO*1.6, parent_in.bB+self.TO, 
                outline = "orange", width = '3')
            canvas_in.create_text( ((parent_in.cen_x+parent_in.right_mid)/2+self.EO*1.2), parent_in.bB+self.MO/2, 
                text="Q = "+str(parent_in.solution),fill = "orange", font=(cd.small_font))

    def draw_logic_sequence(self, parent_in, canvas_in, matrix_in, type_in):
        if (type_in == parent_in.POOL_INDEX):
            self.pool_adjust_vars(parent_in)
        self.write_eq_payoff(parent_in, canvas_in, matrix_in, type_in)
        self.draw_sig_arrows(canvas_in)                 # 1. Draw branch ignals
        self.draw_p2choice(parent_in, canvas_in, type_in)                # 2. Draw P2 payoffs given signal choices 
        self.check_deviation(parent_in, canvas_in)      # 3. Check for deviation
        self.output_eq_result(parent_in, canvas_in, type_in)  # 4. Output result
        if (type_in == parent_in.POOL_INDEX):
            self.write_pool_prob(parent_in, canvas_in)


