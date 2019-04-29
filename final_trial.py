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
import runpy



root = tk.Tk()

root.title("Stream Data Processing")

def childStart():
        pass

def childInitialising():
        os.system("python app-xml.py")

def startProcessing():
        t1 = threading.Thread(target=childInitialising)
        t1.start() 

button1 = tk.Button(root, text ="Start",command=startProcessing)
button1.place(x = 20, y = 20, width=120, height=25)

root.geometry("400x150")

root.mainloop()

