import tkinter as tk
from tkinter.filedialog import askopenfilename
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
import requests

top = tk.Tk()
top.dat=[]
top.filename = None
top.n=0

def click():
        top.filename=askopenfilename(initialdir = "/Study/Project/Stream Data",title = "Select file",filetypes = (("xml files","*.xml"),("all files","*.xml")))
        df = open(top.filename,"r")

        top.file_xml=bytearray(df.read(),'utf8')
        top.file_dict=xmltodict.parse(top.file_xml)
        top.window_size=top.file_dict['stream-processing']['window-size']
        if top.file_dict['stream-processing']['window-type'] == 'sliding':
                top.shift=top.file_dict['stream-processing']['velocity']
        else:
                top.shift=top.file_dict['stream-processing']['window-size']
        top.source_file=top.file_dict['stream-processing']['file']
        top.unit=top.file_dict['stream-processing']['unit']
        top.buffer_size=int(top.file_dict['stream-processing']['buffer-size'])
        top.output_file=top.file_dict['stream-processing']['output']
        top.list_min=[None]*top.buffer_size
        top.list_max=[None]*top.buffer_size
        top.list_avg=[None]*top.buffer_size

#    print(file_dict.keys())
#    print(type(file_dict))
#    print(file_dict['stream-processing']['queries']['query'])

def processing():
    while(1):

        r = requests.get(url = "http://13.232.145.55:5555/random/"+top.window_size).text
        

        temp=list(r[1:-1].split(","))                                       #top.dat[top.n:top.n+int(top.window_size)]
#        print(temp)
#        print("\nLowest"+min(temp))
#        print("\nHighest"+max(temp))
        top.ofile = open("/Study/Project/Stream Data/outputs/"+top.output_file,"a+")

        tem = np.array(temp).astype(np.int64)
        tem_min=tem.min()
        tem_max=tem.max()
        tem_avg=tem.mean()
        entry1Text.set(str('  '.join(temp)))
        entry2Text.set(str(str(tem_avg)+" "+top.unit))
        entry3Text.set(str(str(tem_max)+" "+top.unit))
        entry4Text.set(str(str(tem_min)+" "+top.unit))
        top.n=top.n+int(top.shift)
        time.sleep(1)
        top.list_min.insert(0,tem_min)
        
        top.list_min.pop()
        top.list_max.insert(0,tem_max)
        top.list_max.pop()
        top.list_avg.insert(0,tem_avg)
        top.list_avg.pop()

        top.ofile.write("\n"+str(tem_min)+","+str(tem_max)+","+str(tem_avg))
        top.ofile.close()

        entry5Text.set(str(top.list_min))
        entry6Text.set(str(top.list_max))
        entry7Text.set(str(top.list_avg))

t1 = threading.Thread(target=processing)

def changeText():

        sfile = open(top.source_file,"r")
        
        data=sfile.readlines()
        top.dat=data[0].split(",")

        if 'minimum' in top.file_dict['stream-processing']['queries']['query']:
                label3 = tk.Label(top, text="Lowest:")
                label3.place(x = 20, y = 310, width=50, height=25)
                entry4 = tk.Entry(top, state='disabled', textvariable=entry4Text)
                entry4.place(x = 70, y = 310, width=80, height=25)
#                label4 = tk.Label(top, text=top.unit)
#                label4.place(x = 105, y = 310, width=50, height=25)
                entry5 = tk.Entry(top, state='disabled', textvariable=entry5Text)
                entry5.place(x = 220, y = 310, width=180, height=25)

        if 'maximum' in top.file_dict['stream-processing']['queries']['query']:
                label2 = tk.Label(top, text="Highest:")
                label2.place(x = 20, y = 280, width=50, height=25)
                entry3 = tk.Entry(top, state='disabled', textvariable=entry3Text)
                entry3.place(x = 70, y = 280, width=80, height=25)
#                label4 = tk.Label(top, text=top.unit)
#                label4.place(x = 105, y = 280, width=50, height=25)
                entry6 = tk.Entry(top, state='disabled', textvariable=entry6Text)
                entry6.place(x = 220, y = 280, width=180, height=25)

        if 'average' in  top.file_dict['stream-processing']['queries']['query']:
                label1 = tk.Label(top, text="Average:")
                label1.place(x = 20, y = 250, width=50, height=25)
                entry2 = tk.Entry(top, state='disabled', textvariable=entry2Text)
                entry2.place(x = 70, y = 250, width=80, height=25)
#                label4 = tk.Label(top, text=top.unit)
#                label4.place(x = 105, y = 250, width=50, height=25)
                entry7 = tk.Entry(top, state='disabled', textvariable=entry7Text)
                entry7.place(x = 220, y = 250, width=180, height=25)

        entry1 = tk.Entry(top, state='disabled', textvariable=entry1Text )
        entry1.place(x = 40, y = 150, width=700, height=25)
        
        t1.start()                
                
# threading.Timer(1,processing).start()

button1 = tk.Button(top, text ="Start",command=changeText)
button1.place(x = 20, y = 60, width=120, height=25)

button2 = tk.Button(top, text ="Pick File",command=click)
button2.place(x = 20, y = 30, width=120, height=25)

entry1Text=tk.StringVar()
entry2Text=tk.StringVar()
entry3Text=tk.StringVar()
entry4Text=tk.StringVar()
entry5Text=tk.StringVar()
entry6Text=tk.StringVar()
entry7Text=tk.StringVar()

top.geometry("800x400")

top.mainloop()
