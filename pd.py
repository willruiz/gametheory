from tkinter import *
import tkinter as tk

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

root = tk.Tk()
name_var=tk.StringVar()



def create_matrix(canvas, root):
    canvas.create_line(left, top, right, top, fill="black", width ='5')
    canvas.create_line(left, top, left, bot, fill="black", width ='5')
    canvas.create_line(right, top, right, bot, fill="black", width ='5')
    canvas.create_line(left, bot, right, bot, fill="black", width ='5')
    canvas.create_line(cenv, top, cenv, bot, fill="black", width ='5')
    canvas.create_line(left, cenh, right, cenh, fill="black", width ='5')

    
def submit():
 
    name=name_var.get()
     
    print("The name is : " + name)
     
    name_var.set("")

def main():
    
    root.geometry(str(height) + "x" + str(width))
    canvas = Canvas(root, bg='white')
    
    create_matrix(canvas, root)
    canvas.pack(fill=BOTH, expand=1)
    
    entryA = tk.Entry (root, textvariable=name_var, width= 4)
    sub_btn=tk.Button(root,text = 'Submit', command = submit)
    canvas.create_window(180, 180, window=entryA)
    canvas.create_window(180, 380, window=sub_btn)

    

    
    root.mainloop()



if __name__ == '__main__':
    main()