# button clicking game i made at school, using tkinter and pandas to store highscores
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import time
import pandas as pd
 
timer = time.time() 
cntr = 0
high : float = 0
player = 'noName'
try:
    score_df = pd.read_csv('D:/Codes/Python/highscores.csv', index_col='Name')
except:
    score_df = pd.DataFrame({'Score': {f'{player}' : 0}})
    score_df.index.name = 'Name'
idx = 0

def speed():
    global timer, high
    t1 = time.time()
    t = t1-timer
    spd = 1/t
    gameSpd.config(text=f'{spd:.2f} cps')
    timer = t1
    if spd > high:
        high = spd
        gameHigh.config(text=f'Your highest cps: {high:.2f}')

def updateLabel(newText : str):
    gameLabel.config(text=newText)

def updateCntr():
    global cntr
    cntr += 1
    scoreLabel.config(text=cntr)
    speed()

    match cntr:
        case 1:
            updateLabel("That's it")
        case 10:
            updateLabel('Keep Going!')
        case 50:
            updateLabel('Well Done!')
        case 90:
            updateLabel('Woah dude')
        case 100:
            updateLabel("Congratulations!")

def save():
    global idx, player
    if messagebox.askyesno('Save score', 'Do you want to store the current highest score?'):
        player = simpledialog.askstring('Name', 'Enter name to save score.')
        score_df.at[player, 'Score'] = high

        score_df.to_csv('D:/Codes/Python/highscores.csv', na_rep=f'noName{idx}')

        idx += 1

def show():
    simpledialog.Dialog(mainframe, 'TEsting')

game = Tk()
game.geometry('400x200')
game.title('Button Game')

mainframe = Frame(game, background='black')
mainframe.pack(fill='both', expand=True)

gameLabel = Label(mainframe, text = 'Button Game', font = ('Kongtext', 15), foreground = 'red', background='black')
gameLabel.pack()

scoreLabel = Label(mainframe, text=cntr, font = ('Kongtext', 40), foreground='white', background='black')
scoreLabel.pack()

gameButton = Button(mainframe, text='Press Me!', command = updateCntr, foreground='white', background='black')
gameButton.pack()

gameSpd = Label(mainframe, text='0 cps', font=('Kongtext', 15), foreground='white', background='black')
gameSpd.pack()

gameHigh = Label(mainframe, text='Your highest cps: 0.0', font=('Kongtext', 10), foreground='white', background='black')
gameHigh.pack()

buttonFrame = Frame(mainframe)
saveButton = Button(buttonFrame, text='Save score', command=save)
saveButton.grid(row=0, column=0)
showButton = Button(buttonFrame, text='Show scores', command=show)
showButton.grid(row=0, column=1)
buttonFrame.pack()

game.mainloop()
print(score_df)
