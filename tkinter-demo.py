import tkinter as tk
from tkinter.filedialog import askopenfilename
import csv
import pandas
import time
import os
import statistics


top = tk.Tk()
top.dat=[]
top.filename = None

def click():
    top.filename=askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.csv")))
    print (top.filename)
    df = open(top.filename,"r")
    data=df.readlines()
    top.dat=data[0].split(",")
    
n=0

def processing():
    while(1):
        temp=top.dat[n:n+10]
        entry1Text.set(str(temp))
        entry2Text.set(str(statistics.mean(temp)))
        entry3Text.set(str(max(temp))
        entry4Text.set(str(min(temp)))
        time.sleep(1)
        n=n+10


def changeText():
    entry1Text.set( "Hello World" )
    processing()

button1 = tk.Button(top, text ="Start",command=processing)
button1.place(x = 20, y = 60, width=120, height=25)

button2 = tk.Button(top, text ="Pick File",command=click)
button2.place(x = 20, y = 30, width=120, height=25)


entry1Text=tk.StringVar()
entry2Text=tk.StringVar()
entry3Text=tk.StringVar()
entry4Text=tk.StringVar()


entry1 = tk.Entry(top, state='disabled', textvariable=entry1Text )
entry1.place(x = 40, y = 150, width=700, height=25)

entry2 = tk.Entry(top, state='disabled', textvariable=entry2Text)
entry2.place(x = 70, y = 250, width=80, height=25)

entry3 = tk.Entry(top, state='disabled', textvariable=entry3Text)
entry3.place(x = 70, y = 280, width=80, height=25)

entry4 = tk.Entry(top, state='disabled', textvariable=entry4Text)
entry4.place(x = 70, y = 310, width=80, height=25)

label1 = tk.Label(top, text="Average:")
label1.place(x = 20, y = 250, width=50, height=25)

label2 = tk.Label(top, text="Highest:")
label2.place(x = 20, y = 280, width=50, height=25)

label3 = tk.Label(top, text="Lowest:")
label3.place(x = 20, y = 310, width=50, height=25)



top.geometry("800x400")

top.mainloop()
