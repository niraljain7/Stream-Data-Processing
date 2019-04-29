import tkinter as tk
from tkinter.filedialog import askopenfilenames
import csv
import pandas
import time
import os
import statistics
import threading
import numpy as np
import lxml
import xml.etree.ElementTree as ET 
import xmltodict



root = tk.Tk()

root.title("Stream Data Processing")

def childStart():
    pass

def childInitialising(filenm):
        child = tk.Tk() 
        child.title(filenm)
        child.geometry("800x400")

        child.dat=[]
        child.n=0

        child.df = open(filenm,"r")
        child.file_xml=bytearray(child.df.read(),'utf8')
        child.file_dict=xmltodict.parse(child.file_xml)
        child.window_size=child.file_dict['stream-processing']['window-size']
        if child.file_dict['stream-processing']['window-type'] == 'sliding':
                child.shift=child.file_dict['stream-processing']['velocity']
        else:
                child.shift=child.file_dict['stream-processing']['window-size']
        child.source_file=child.file_dict['stream-processing']['file']
        child.unit=child.file_dict['stream-processing']['unit']
        child.buffer_size=int(child.file_dict['stream-processing']['buffer-size'])
        child.list_min=[None]*child.buffer_size
        child.list_max=[None]*child.buffer_size
        child.list_avg=[None]*child.buffer_size

        child.sfile = open("xmls/datastreams/"+child.source_file,"r")
        child.data=child.sfile.readlines()
        child.dat=child.data[0].split(",")

        


        child.entry1Text=tk.StringVar()
        child.entry2Text=tk.StringVar()
        child.entry3Text=tk.StringVar()
        child.entry4Text=tk.StringVar()
        child.entry5Text=tk.StringVar()
        child.entry6Text=tk.StringVar()
        child.entry7Text=tk.StringVar()

        if 'minimum' in child.file_dict['stream-processing']['queries']['query']:
                child.label3 = tk.Label(child, text="Lowest:")
                child.label3.place(x = 20, y = 310, width=50, height=25)
                child.entry4 = tk.Entry(child, state='disabled', textvariable=child.entry4Text)
                child.entry4.place(x = 70, y = 310, width=80, height=25)
#                label4 = tk.Label(top, text=top.unit)
#                label4.place(x = 105, y = 310, width=50, height=25)
                child.entry5 = tk.Entry(child, state='disabled', textvariable=child.entry5Text)
                child.entry5.place(x = 220, y = 310, width=180, height=25)

        if 'maximum' in child.file_dict['stream-processing']['queries']['query']:
                child.label2 = tk.Label(child, text="Highest:")
                child.label2.place(x = 20, y = 280, width=50, height=25)
                child.entry3 = tk.Entry(child, state='disabled', textvariable=child.entry3Text)
                child.entry3.place(x = 70, y = 280, width=80, height=25)
#                label4 = tk.Label(top, text=top.unit)
#                label4.place(x = 105, y = 280, width=50, height=25)
                child.entry6 = tk.Entry(child, state='disabled', textvariable=child.entry6Text)
                child.entry6.place(x = 220, y = 280, width=180, height=25)

        if 'average' in  child.file_dict['stream-processing']['queries']['query']:
                child.label1 = tk.Label(child, text="Average:")
                child.label1.place(x = 20, y = 250, width=50, height=25)
                child.entry2 = tk.Entry(child, state='disabled', textvariable=child.entry2Text)
                child.entry2.place(x = 70, y = 250, width=80, height=25)
#                label4 = tk.Label(top, text=top.unit)
#                label4.place(x = 105, y = 250, width=50, height=25)
                child.entry7 = tk.Entry(child, state='disabled', textvariable=child.entry7Text)
                child.entry7.place(x = 220, y = 250, width=180, height=25)

        child.entry1 = tk.Entry(child, state='disabled', textvariable=child.entry1Text )
        child.entry1.place(x = 40, y = 150, width=700, height=25)




        def streamThread():
                while(1):
                        print(filenm)
                        child.temp=child.dat[child.n:child.n+int(child.window_size)]
                        child.tem = np.array(child.temp).astype(np.int64)
                        child.tem_min=child.tem.min()
                        child.tem_max=child.tem.max()
                        child.tem_avg=child.tem.mean()
                        child.entry1Text.set(str('  '.join(child.temp)))
                        child.entry2Text.set(str(str(child.tem_avg)+" "+child.unit))
                        child.entry3Text.set(str(str(child.tem_max)+" "+child.unit))
                        child.entry4Text.set(str(str(child.tem_min)+" "+child.unit))
                        child.n=child.n+int(child.shift)
                        time.sleep(1)
                        child.list_min.insert(0,child.tem_min)
                        child.list_min.pop()
                        child.list_max.insert(0,child.tem_max)
                        child.list_max.pop()
                        child.list_avg.insert(0,child.tem_avg)
                        child.list_avg.pop()
                        child.entry5Text.set(str(child.list_min))
                        child.entry6Text.set(str(child.list_max))
                        child.entry7Text.set(str(child.list_avg))
        
        Sthread = threading.Thread(target=streamThread)
        Sthread.start()

        child.mainloop()
        child.entry1Text=tk.StringVar()
        child.entry1 = tk.Entry(child, state='disabled', textvariable=child.entry1Text)
        child.entry1.place(x = 20, y = 20, width=50, height=25)


                

        


def startProcessing():
#files = askopenfilenames(parent=root,title='Choose a file')
        files = askopenfilenames(initialdir = "/Study/Project/Stream Data/xmls",title = "Select file",filetypes = (("xml files","*.xml"),("all files","*.*")))
        for i in files:
                thread = threading.Thread(target=childInitialising,args=(i,))
                thread.start()   

button1 = tk.Button(root, text ="Start",command=startProcessing)
button1.place(x = 20, y = 20, width=120, height=25)

root.geometry("400x150")

root.mainloop()

