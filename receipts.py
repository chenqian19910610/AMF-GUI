# create the login page
from tkinter import *
from tkinter import ttk
from sqlite3 import dbapi2 as sqlite
from PIL import ImageTk, Image
import webbrowser

c=sqlite.connect('lmf_data.sqlite')
cur=c.cursor()

def PO_summary():
    global c, cur
    root1 = Tk()
    root1.title('Purchasing Summary')
    root1.wm_iconbitmap('logo.ico')
    # root.configure(background='#e5eef4')
    info = open('Summary.txt', 'r').read()
    t1 = Text(root1)
    t1.insert(INSERT, info)
    t1.pack()


