# create the login page
from tkinter import *
from sqlite3 import dbapi2 as sqlite
import webbrowser
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta,date


c=sqlite.connect('lmf_data.sqlite')
cur=c.cursor()



"""-----------------------quality check---------------------------------------------"""

column_name_qc=['DeliveryID','POID','ElementID','Family and Type','Quality','Action']
def qualitycheck():
    global flag, c,cur,qcheck,value_qc,column_name_qc,lb1,lb2,lb3,lb4
    flag='quality'
    value_qc=['']*len(column_name_qc)
    qcheck=Tk()
    qcheck.title('Quality Check')
    qcheck.wm_iconbitmap('logo.ico')

    Label(qcheck,text='Choose element').grid(row=0,column=0)
    Button(qcheck,width=25,text='Main Menu',command=mainmenu).grid(row=0,column=1)
    Button(qcheck,width=25,text='Shearwall POs',command=wallPO).grid(row=1,column=0)
    Button(qcheck, width=25, text='Column POs', command=colPO).grid(row=1, column=1)
    Button(qcheck, width=25, text='Slab POs', command=slabPO).grid(row=1, column=2)

    for i in range(4):
        Label(qcheck, text=column_name_qc[i]).grid(row=2, column=i)

    def scrollbarv(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)

    scbar=Scrollbar(orient='vertical',command=scrollbarv)
    lb1 = Listbox(qcheck, yscrollcommand=scbar.set)
    lb2 = Listbox(qcheck, yscrollcommand=scbar.set)
    lb3 = Listbox(qcheck, yscrollcommand=scbar.set)
    lb4 = Listbox(qcheck, yscrollcommand=scbar.set)

    lb1.grid(row=3, column=0)
    lb1.configure(width=0,height=10)
    lb2.grid(row=3, column=1)
    lb2.configure(width=0, height=10)
    lb3.grid(row=3, column=2)
    lb3.configure(width=0, height=10)
    lb4.grid(row=3, column=3)
    lb4.configure(width=0, height=10)
    scbar.grid(row=3,column=4,stick=N+S)

    Label(qcheck, text='Choose PO ID').grid(row=4, column=0)
    value_qc[1] = Entry(qcheck)
    value_qc[1].grid(row=4, column=1)

    Label(qcheck,text='Input Quality with RFID scanner').grid(row=5, column=0)
    value_qc[4] = Entry(qcheck)
    value_qc[4].grid(row=5, column=1)

    Label(qcheck, text='Input Quality with RFID scanner').grid(row=6, column=0)
    value_qc[5] = Entry(qcheck)
    value_qc[5].grid(row=6, column=1)

    Button(qcheck, width=25, text='Update information',command=updateqc).grid(row=7,column=0)

    qcheck.resizable(width=False, height=False)
    qcheck.mainloop()

def wallPO():
    global c,cur,c,cur,qcheck,value_qc,column_name_qc,lb1,lb2,lb3,lb4
    cur.execute('select * from BIM_Dynamo_coreshearwall')

    lb1.delete(0, END)
    lb2.delete(0, END)
    lb3.delete(0, END)
    lb4.delete(0, END)

    for i in cur:
        lb1.insert(1, i[1])
        lb2.insert(1, i[2])
        lb3.insert(1, i[0])
        lb4.insert(1, i[6])

    c.commit()


def colPO():
    global c, cur, c, cur, qcheck, value_qc, column_name_qc, lb1, lb2, lb3, lb4
    cur.execute('select * from BIM_Dynamo_column')

    lb1.delete(0, END)
    lb2.delete(0, END)
    lb3.delete(0, END)
    lb4.delete(0, END)

    for i in cur:
        lb1.insert(1, i[1])
        lb2.insert(1, i[2])
        lb3.insert(1, i[0])
        lb4.insert(1, i[6])

    c.commit()

def slabPO():
    global c, cur, c, cur, qcheck, value_qc, column_name_qc, lb1, lb2, lb3, lb4
    cur.execute('select * from BIM_Dynamo_slab')

    lb1.delete(0, END)
    lb2.delete(0, END)
    lb3.delete(0, END)
    lb4.delete(0, END)

    for i in cur:
        lb1.insert(1, i[1])
        lb2.insert(1, i[2])
        lb3.insert(1, i[0])
        lb4.insert(1, i[6])

    c.commit()

def updateqc():
    global c, cur, c, cur, qcheck, value_qc, column_name_qc, lb1, lb2, lb3, lb4
    quality=str(value_qc[4])
    action=str(value_qc[5])
    po=str(value_qc[1])

    cur.execute('DROP TABLE IF EXISTS P3_POIDs_WBS_prefabcol_copy')
    cur.execute('create table P3_POIDs_WBS_prefabcol_copy as select * from P3_POIDs_WBS_prefabcol')
    cur.execute(
        'update P3_POIDs_WBS_prefabcol_copy set Quality=?,Action=? where P2_procure_lookahead_copy.POID=?',
        (quality,action,po))

    c.commit()


"""-----------------------material status---------------------------------------------"""

column_name_st=['Delivery ID','PO ID','Manufacturer','Quality','Action']
def materialstatus():
    global flag, c, cur, matstat, value_ms, column_name_st, lbm1, lbm2, lbm3, lbm4,lbm5
    flag = 'status'
    value_ms = [''] * len(column_name_qc)
    matstat = Tk()
    matstat.title('Material Status')
    matstat.wm_iconbitmap('logo.ico')

    Button(matstat, width=20, text='Main Menu',command=mainmenu).grid(row=0, column=0)

    Label(matstat, text='Choose RFID tag').grid(row=1, column=0)
    value_ms[0]=Entry(matstat)
    value_ms[0].grid(row=1,column=1)
    Button(matstat, width=20, text='Show information',command=checkdel).grid(row=1, column=2)

    Label(matstat, text='Choose PO ID').grid(row=2, column=0)
    value_ms[1]=Entry(matstat)
    value_ms[1].grid(row=2,column=1)
    Button(matstat, width=20, text='Show information', command=checkpo).grid(row=2, column=2)


    def scrollbarv(*args):
        lbm1.yview(*args)
        lbm2.yview(*args)
        lbm3.yview(*args)
        lbm4.yview(*args)
        lbm5.yview(*args)

    scbar = Scrollbar(orient='vertical', command=scrollbarv)
    lbm1 = Listbox(matstat, yscrollcommand=scbar.set)
    lbm2 = Listbox(matstat, yscrollcommand=scbar.set)
    lbm3 = Listbox(matstat, yscrollcommand=scbar.set)
    lbm4 = Listbox(matstat, yscrollcommand=scbar.set)
    lbm5 = Listbox(matstat, yscrollcommand=scbar.set)

    lbm1.grid(row=3, column=0)
    lbm1.configure(width=0, height=10)
    lbm2.grid(row=3, column=1)
    lbm2.configure(width=0, height=10)
    lbm3.grid(row=3, column=2)
    lbm3.configure(width=0, height=10)
    lbm4.grid(row=3, column=3)
    lbm4.configure(width=0, height=10)
    lbm5.grid(row=3, column=4)
    lbm5.configure(width=0, height=10)
    scbar.grid(row=3, column=5, stick=N + S)

    matstat.resizable(width=False, height=False)
    matstat.mainloop()

def checkdel():
    global c, cur, matstat, value_ms, column_name_st, lbm1, lbm2, lbm3, lbm4, lbm5
    deli=value_ms[0]

    cur.execute('select * from P3_POIDs_WBS_prefabcol_copy where DeliveryID=?',[deli])
    lbm1.delete(0, END)
    lbm2.delete(0, END)
    lbm3.delete(0, END)
    lbm4.delete(0, END)
    lbm5.delete(0, END)

    for i in cur:
        lbm1.insert(1, i[1])
        lbm2.insert(1, i[2])
        lbm3.insert(1, i[14])
        lbm4.insert(1, i[25])
        lbm5.insert(1, i[26])
    c.commit()

def checkpo():
    global c, cur, matstat, value_ms, column_name_st, lbm1, lbm2, lbm3, lbm4, lbm5
    poid=value_ms[1]

    cur.execute('select * from P3_POIDs_WBS_prefabcol_copy where POID=?',[poid])
    lbm1.delete(0, END)
    lbm2.delete(0, END)
    lbm3.delete(0, END)
    lbm4.delete(0, END)
    lbm5.delete(0, END)

    for i in cur:
        lbm1.insert(1, i[1])
        lbm2.insert(1, i[2])
        lbm3.insert(1, i[14])
        lbm4.insert(1, i[25])
        lbm5.insert(1, i[26])

    c.commit()

def mainmenu():
    if flag=='quality':
        qcheck.destroy()
    elif flag=='status':
        matstat.destroy()
