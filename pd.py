from tkinter import *
import tkinter as tk
import math
import numpy as np

rows = 3
cols = 3

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

colA = math.floor((cenv+left)/2)
colB = math.floor((cenv+right)/2)

rowA = math.floor((cenh+top)/2)
rowB = math.floor((cenh+bot)/2)

root = tk.Tk()
A1_string=tk.StringVar()
A2_string=tk.StringVar()

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
    
    width = cols*200+100
    height = rows*200+100
    left = width * 0.2
    right = width * 0.8
    top = height * 0.2
    bot = height * 0.8
    unit_width = (right-left)/cols_in
    unit_height = (bot-top)/rows_in
    cenv = width * 0.5
    cenh = height * 0.5



def submit(entry_list):
    
    for i in entry_list:
        for j in i: # iterate through tuple
            name=j.get()
            
            print("The name is : " + name)
            
            j.set("")

def create_matrix(canvas, root, rows, cols):
    

    update_dimensions(rows, cols)
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

def create_entry_boxes(canvas, root, rows, cols):

    entry_list = []
    entry_windows = []

    for i in range(rows):
        entry_row = []
        for j in range(cols):
            entry_row.append((tk.StringVar(), tk.StringVar()))
        entry_list.append(entry_row)

    math.floor((cenv+left)/2)

    initH_offset = top+unit_height/2
    initW_offset = left+unit_width/2
    for i in range(rows):
        for j in range(cols):
            entryA0 = tk.Entry (root, textvariable=entry_list[i][j][0], width= 4)
            canvas.create_window(initW_offset+(unit_width*(j))-offset, initH_offset+(unit_height*(i)), window=entryA0)
            entryA1 = tk.Entry (root, textvariable=entry_list[i][j][1], width= 4)
            canvas.create_window(initW_offset+(unit_width*(j))+offset, initH_offset+(unit_height*(i)), window=entryA1)
                

    # entryA1 = tk.Entry (root, textvariable=entry_list[0][0], width= 4)
    # entryA2 = tk.Entry (root, textvariable=entry_list[0][1], width= 4)
    
    # canvas.create_window(colA-offset, rowA, window=entryA1)
    # canvas.create_window(colA+offset, rowA, window=entryA2)
    sub_btn=tk.Button(root,text = 'Submit', command = lambda: submit(entry_list))
    canvas.create_window(180, 380, window=sub_btn)
    


def main():
    
    
    canvas = Canvas(root, bg='white')
    
    create_matrix(canvas, root, rows, cols)
    create_entry_boxes(canvas, root, rows, cols)
    root.geometry(str(width) + "x" + str(height))

    root.mainloop()



if __name__ == '__main__':
    main()