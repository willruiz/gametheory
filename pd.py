from tkinter import *



def main():

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


    root = Tk()
    canvas = Canvas(root, bg='white')
    canvas.pack(fill=BOTH, expand=1)

    # Top
    canvas.create_line(left, top, right, top, fill="black", width ='5')
    # Left
    canvas.create_line(left, top, left, bot, fill="black", width ='5')
    # Right
    canvas.create_line(right, top, right, bot, fill="black", width ='5')
    # Bot
    canvas.create_line(left, bot, right, bot, fill="black", width ='5')
    # Cross-v
    canvas.create_line(cenv, top, cenv, bot, fill="black", width ='5')
    # Cross-h
    canvas.create_line(left, cenh, right, cenh, fill="black", width ='5')
    
    root.geometry(str(height) + "x" + str(width))
    root.mainloop()


if __name__ == '__main__':
    main()