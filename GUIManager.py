from tkinter import *
from turtle import bgcolor, color

bgcolor = "#16161A"
accent_color = "#f7704a"
#Setup GUI
Window = Tk()
Window.title("AutoChess")
Window.geometry("628x608")
#Set the background color to 16161A
Window.configure(background=bgcolor)
#Add a title label
TitleLabel = Label(Window, text="AutoChess", font=("Dosis", 36), bg=bgcolor, fg=accent_color)
#Move the title lable a little bit down
TitleLabel.place(x=0, y=100)
TitleLabel.pack()

Window.mainloop()