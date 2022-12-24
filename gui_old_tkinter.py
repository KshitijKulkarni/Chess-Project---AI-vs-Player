import Game_Manager
from tkinter import Label, Tk, Canvas, Entry, Text, Button, PhotoImage
#region Functions
def Start():
    print("Start")
    Game_Manager.Start(1)

def RetakeReferenceFrame():
    print("RetakeReferenceFrame")
    Game_Manager.ReTakePicture()

def OnUserPlay():
    print("OnUserPlay")
    Game_Manager.OnUserPlayed()
#endregion

def SetupMatch(Skill):
    print(Skill)
    borderwidth = 5
    height, width = 5,20
    tk = Tk()
    tk.title("Chess")
    tk.geometry("800x480")

    Label(tk, text="AutoChess").pack()
    Button(tk, text="Start", command=lambda: Start(), borderwidth=borderwidth, width=width, height=height).pack()
    Button(tk, text="Confirm Move", command=lambda: OnUserPlay(), borderwidth=borderwidth, width=width, height=height).pack()
    Button(tk, text="Retake Reference Frame", command=lambda: RetakeReferenceFrame(), borderwidth=borderwidth, width=width, height=height).pack()

    tk.mainloop()

SetupMatch(100)