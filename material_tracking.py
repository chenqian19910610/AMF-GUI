# create the login page
from tkinter import *
from sqlite3 import dbapi2 as sqlite
import webbrowser
import pandas as pd
import numpy as np
from datetime import timedelta

c=sqlite.connect('lmf_data.sqlite')
cur=c.cursor()

"""--------------------------------tracking schedules and look ahead plans----------------------------------------"""
column_name_lookahead=['WBScode','Start_Date','Finish_Date','Duration','FlowMaturityIndex','Constraints']
def lookahead():
    global pjschedule, c, cur, column_name_lookahead,flag, value_WBS,value_look,lb1,lb2,lb3,lb4,lb5,lb6
    flag='lookahead'
    value_WBS=['']*len(column_name_lookahead)
    pjschedule=Tk()
    pjschedule.title('Look Ahead Plan & Schedules')
    pjschedule.wm_iconbitmap('logo.ico')

    Button(pjschedule,width=25,text='overall baseline schedule',command=show_all).grid(row=0,column=0)
    Button(pjschedule, width=25, text='main menu', command=mainmenu).grid(row=0, column=1)
    for i in range(4):
        Label(pjschedule,text=column_name_lookahead[i]).grid(row=1,column=i)

    Label(pjschedule,text='Choose WBS to update').grid(row=3,column=0)
    value_WBS[0]=Entry(pjschedule)
    value_WBS[0].grid(row=3,column=1)
    Label(pjschedule, text='Input new constraint').grid(row=4, column=0)
    value_WBS[5] = Entry(pjschedule)
    value_WBS[5].grid(row=4, column=1)
    Label(pjschedule, text='Input new FMI').grid(row=5, column=0)
    value_WBS[4] = Entry(pjschedule)
    value_WBS[4].grid(row=5,column=1)
    Label(pjschedule, text='Input new start_date').grid(row=6, column=0)
    value_WBS[1] = Entry(pjschedule)
    value_WBS[1].grid(row=6, column=1)

    Button(pjschedule,width=25,text='update schedule',command=update_sched).grid(row=7,column=0) # create a copy of the original baseline schedule and update

    Label(pjschedule,text='detailed look ahead plan', fg='green').grid(row=8, column=0)
    Label(pjschedule,text='Choose start_date').grid(row=9,column=0)
    value_look=['']*len(column_name_lookahead)
    value_look[1] = Entry(pjschedule)
    value_look[1].grid(row=9,column=1)
    Label(pjschedule, text='Choose finish_date').grid(row=10, column=0)
    value_look[2] = Entry(pjschedule)
    value_look[2].grid(row=10, column=1)

    Button(pjschedule, width=25, text='show look ahead tasks', command=check_look).grid(row=11, column=0)
    for i in range(len(column_name_lookahead)):
        Label(pjschedule, text=column_name_lookahead[i]).grid(row=12, column=i)
        Label(pjschedule, text=column_name_lookahead[i]).grid(row=15, column=i)

    def scrollbarv(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)


    scbar=Scrollbar(orient='vertical',command=scrollbarv)
    lb1 = Listbox(pjschedule, yscrollcommand=scbar.set)
    lb2 = Listbox(pjschedule, yscrollcommand=scbar.set)
    lb3 = Listbox(pjschedule, yscrollcommand=scbar.set)
    lb4 = Listbox(pjschedule, yscrollcommand=scbar.set)
    lb5 = Listbox(pjschedule, yscrollcommand=scbar.set)
    lb6 = Listbox(pjschedule, yscrollcommand=scbar.set)

    lb1.grid(row=13, column=0)
    lb1.configure(width=0, height=10)
    lb2.grid(row=13, column=1)
    lb2.configure(width=0, height=10)
    lb3.grid(row=13, column=2)
    lb3.configure(width=0, height=10)
    lb4.grid(row=13, column=3)
    lb4.configure(width=0, height=10)
    lb5.grid(row=13, column=4)
    lb5.configure(width=0, height=10)
    lb6.grid(row=13, column=5)
    lb6.configure(width=0, height=10)
    scbar.grid(row=13,column=6,stick=N+S)

    Label(pjschedule, text='Choose WBS').grid(row=14, column=0)
    value_look[0] = Entry(pjschedule)
    value_look[0].grid(row=14, column=1)
    Button(pjschedule, width=25, text='show task info', command=check_wbs).grid(row=14, column=2)

    show_all()
    pjschedule.resizable(width=False,height=False)
    pjschedule.mainloop()

def show_all():
    global c, cur, column_name_lookahead, flag, value_WBS, value_look
    cur.execute('select * from P2_procure_lookahead')

    def scrollbarv_a(*args):
        lba1.yview(*args)
        lba2.yview(*args)
        lba3.yview(*args)
        lba4.yview(*args)

    scbar = Scrollbar(orient='vertical',command=scrollbarv_a)
    lba1 = Listbox(pjschedule,  selectmode=MULTIPLE)
    lba2 = Listbox(pjschedule,  selectmode=MULTIPLE)
    lba3 = Listbox(pjschedule,  selectmode=MULTIPLE)
    lba4 = Listbox(pjschedule,  selectmode=MULTIPLE)

    lba1.grid(row=2, column=0)
    lba1.configure(width=0, height=5, yscrollcommand=scbar.set)
    lba2.grid(row=2, column=1)
    lba2.configure(width=0, height=5, yscrollcommand=scbar.set)
    lba3.grid(row=2, column=2)
    lba3.configure(width=0, height=5, yscrollcommand=scbar.set)
    lba4.grid(row=2, column=3)
    lba4.configure(width=0, height=5, yscrollcommand=scbar.set)
    scbar.grid(row=2, column=4, stick=N + S)

    for i in cur:
        lba1.insert(1, i[0])
        lba2.insert(1, i[1])
        lba3.insert(1, i[2])
        lba4.insert(1, i[3])
    c.commit()

def update_sched():
    global pjschedule, c, cur, column_name_lookahead, flag, value_WBS, value_look, lb1, lb2, lb3, lb4, lb5, lb6
    const=str(value_WBS[5].get())
    fmi=str(value_WBS[4].get())
    std=str(value_WBS[1].get())
    wbs=str(value_WBS[0].get())

    cur.execute('DROP TABLE IF EXISTS P2_procure_lookahead_copy')
    cur.execute('create table P2_procure_lookahead_copy as select * from P2_procure_lookahead')

    def fnd(): # fnd is local variable, cannot be directly computed for use in cur.update
        cur.execute('select * from P2_procure_lookahead_copy where WBScode=?', [wbs])
        for i in cur:
            n=float(i[3][:-3].strip().replace(' ',''))
            fnd=str(pd.to_datetime(std)+timedelta(days=n))
        return fnd
    fnd=fnd()

    cur.execute('update P2_procure_lookahead_copy set Constraints=?,FlowMaturityIndex=?,Start_Date=?, Finish_Date=? where P2_procure_lookahead_copy.WBScode=?',(const,fmi,std,wbs,fnd))

    c.commit()

def check_look():
    global c, cur, column_name_lookahead,flag, value_WBS,value_look,lb1,lb2,lb3,lb4,lb5,lb6
    a=cur.execute('select * from P2_procure_lookahead_copy')

    checkstd=pd.to_datetime(str(value_look[1].get()))
    checkfnd=pd.to_datetime(str(value_look[2].get()))

    lb1.delete(0, END)
    lb2.delete(0, END)
    lb3.delete(0, END)
    lb4.delete(0, END)
    lb5.delete(0, END)
    lb6.delete(0, END)

    for i in cur:
        a=pd.to_datetime(i[1])
        b=pd.to_datetime(i[2])
        if a>checkstd and a<checkfnd:
            lb1.insert(1, i[0])
            lb2.insert(1, i[1])
            lb3.insert(1, i[2])
            lb4.insert(1, i[3])
            lb5.insert(1, i[4])
            lb6.insert(1, i[5])
        else:
            pass

    c.commit()

def check_wbs():
    global c, cur, column_name_lookahead, flag, value_WBS, value_look
    wbsname=value_look[0].get()
    cur.execute('select * from P2_procure_lookahead_copy where WBScode=?',[wbsname])

    def scrollbarv_w(*args):
        lbw1.yview(*args)
        lbw2.yview(*args)
        lbw3.yview(*args)
        lbw4.yview(*args)
        lbw5.yview(*args)
        lbw6.yview(*args)

    scbar = Scrollbar(orient='vertical', command=scrollbarv_w)
    lbw1 = Listbox(pjschedule, selectmode=MULTIPLE)
    lbw2 = Listbox(pjschedule, selectmode=MULTIPLE)
    lbw3 = Listbox(pjschedule, selectmode=MULTIPLE)
    lbw4 = Listbox(pjschedule, selectmode=MULTIPLE)
    lbw5 = Listbox(pjschedule, selectmode=MULTIPLE)
    lbw6 = Listbox(pjschedule, selectmode=MULTIPLE)

    lbw1.grid(row=16, column=0)
    lbw1.configure(width=0, height=0, yscrollcommand=scbar.set)
    lbw2.grid(row=16, column=1)
    lbw2.configure(width=0, height=0, yscrollcommand=scbar.set)
    lbw3.grid(row=16, column=2)
    lbw3.configure(width=0, height=0, yscrollcommand=scbar.set)
    lbw4.grid(row=16, column=3)
    lbw4.configure(width=0, height=0, yscrollcommand=scbar.set)
    lbw5.grid(row=16, column=4)
    lbw5.configure(width=0, height=0, yscrollcommand=scbar.set)
    lbw6.grid(row=16, column=5)
    lbw6.configure(width=0, height=0, yscrollcommand=scbar.set)
    scbar.grid(row=16, column=6, stick=N + S)

    for i in cur:
        lbw1.insert(1, i[0])
        lbw2.insert(1, i[1])
        lbw3.insert(1, i[2])
        lbw4.insert(1, i[3])
        lbw5.insert(1, i[4])
        lbw6.insert(1, i[5])
    c.commit()



"""-------------------------Tracking material POs and building elements---------------------------------"""
column_name_PO=['POID','FromBuildingElement','Quantity',
                'Manufacturer','trans_lead','manu_lead','releasedate',
                'manudate','needdate','Baseline_releasedate',
                'AlertAction']
column_name_track=['elementID','POID','DeliveryID','WBScode','FamilyandType']

def POs():
    global c, cur, PO_info, column_name_PO,column_name_track,value_PO,value_track,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb10,lb11,lb12
    flag = 'POs'
    value_PO=['']*len(column_name_PO)
    value_track=['']*len(column_name_track)
    PO_info = Tk()
    PO_info.title('Purchasing Orders')
    PO_info.wm_iconbitmap('logo.ico')

    Label(PO_info,text='Choose Construction Method',fg='green').grid(row=0,column=0)
    Button(PO_info,width=25,text='Insitu Material_POs',command=show_insitu).grid(row=0,column=1)
    Button(PO_info, width=25, text='Prefabricated Material_POs', command=show_prefab).grid(row=0, column=2)
    for i in range(len(column_name_PO)):
        Label(PO_info, text=column_name_PO[i]).grid(row=2, column=i+1)

    def scrollbarv_po(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)
        lb7.yview(*args)
        lb8.yview(*args)
        lb9.yview(*args)
        lb10.yview(*args)
        lb11.yview(*args)
        lb12.yview(*args)

    scbar=Scrollbar(orient='vertical',command=scrollbarv_po)
    lb1 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb2 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb3 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb4 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb5 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb6 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb7 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb8 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb9 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb10 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb11 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb12 = Listbox(PO_info, yscrollcommand=scbar.set)
    lb1.grid(row=3, column=0)
    lb1.configure(width=0,height=10)
    lb2.grid(row=3, column=1)
    lb2.configure(width=0, height=10)
    lb3.grid(row=3, column=2)
    lb3.configure(width=0, height=10)
    lb4.grid(row=3, column=3)
    lb4.configure(width=0, height=10)
    lb5.grid(row=3, column=4)
    lb5.configure(width=0, height=10)
    lb6.grid(row=3, column=5)
    lb6.configure(width=0, height=10)
    lb7.grid(row=3, column=6)
    lb7.configure(width=0, height=10)
    lb8.grid(row=3, column=7)
    lb8.configure(width=0, height=10)
    lb9.grid(row=3,column=8)
    lb9.configure(width=0, height=10)
    lb10.grid(row=3, column=9)
    lb10.configure(width=0, height=10)
    lb11.grid(row=3, column=10)
    lb11.configure(width=0, height=10)
    lb12.grid(row=3, column=11)
    lb12.configure(width=0, height=10)
    scbar.grid(row=3,column=12,stick=N+S)


    Label(PO_info,text='Choose PO_ID').grid(row=4,column=0)
    value_PO[0] = Entry(PO_info)
    value_PO[0].grid(row=4, column=1)
    Button(PO_info, width=25, text='Related Elements', command=show_element).grid(row=4, column=2)

    for i in range(len(column_name_track)):
        Label(PO_info, text=column_name_track[i]).grid(row=5, column=i)

    PO_info.resizable(width=False, height=False)
    PO_info.mainloop()

def show_insitu():
    Button(PO_info, width=25, text='Insitu Concrete', command=show_concrete).grid(row=1, column=0)
    Button(PO_info, width=25, text='Insitu Concrete', command=show_rebar).grid(row=1, column=1)

def show_prefab():
    Button(PO_info, width=25, text='Prefabricated elements', command=show_prefab1).grid(row=1, column=2)

def show_concrete():
    global c, cur, PO_info, column_name_PO,column_name_track,value_PO,value_track,\
        lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb10,lb11,lb12
    cur.execute('select * from P3_POIDs_WBS_sum_concrete')

    Label(PO_info,text='---concrete---',fg='blue').grid(row=2,column=0)

    lb1.delete(0, END)
    lb2.delete(0, END)
    lb3.delete(0, END)
    lb4.delete(0, END)
    lb5.delete(0, END)
    lb6.delete(0, END)
    lb7.delete(0, END)
    lb8.delete(0, END)
    lb9.delete(0, END)
    lb10.delete(0, END)
    lb11.delete(0, END)
    lb12.delete(0, END)

    for i in cur:
        lb1.insert(1, i[2])
        lb2.insert(1, i[3])
        lb3.insert(1, i[1])
        lb4.insert(1, str(i[4])+'m3')
        lb5.insert(1, i[5])
        lb6.insert(1, i[6])
        lb7.insert(1, i[7])
        lb8.insert(1, i[8])
        lb9.insert(1, i[9])
        lb10.insert(1, i[10])
        lb11.insert(1, i[11])
        lb12.insert(1, i[12])

def show_prefab1():
    global c, cur, PO_info, column_name_PO,column_name_track,value_PO,value_track,\
        lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb10,lb11,lb12
    cur.execute('select * from P3_POIDs_WBS_prefabcol')

    Label(PO_info,text='Prefab Column',fg='blue').grid(row=2,column=0)

    lb1.delete(0, END)
    lb2.delete(0, END)
    lb3.delete(0, END)
    lb4.delete(0, END)
    lb5.delete(0, END)
    lb6.delete(0, END)
    lb7.delete(0, END)
    lb8.delete(0, END)
    lb9.delete(0, END)
    lb10.delete(0, END)
    lb11.delete(0, END)
    lb12.delete(0, END)

    for i in cur:
        lb1.insert(1, i[2])
        lb2.insert(1, i[3])
        lb3.insert(1, i[1])
        lb4.insert(1, str(i[4])+'ea.')
        lb5.insert(1, i[5])
        lb6.insert(1, i[6])
        lb7.insert(1, i[7])
        lb8.insert(1, i[8])
        lb9.insert(1, i[9])
        lb10.insert(1, i[10])
        lb11.insert(1, i[11])
        lb12.insert(1, i[12])

def show_rebar():
    global c, cur, PO_info, column_name_PO,column_name_track,value_PO,value_track,\
        lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb10,lb11,lb12
    cur.execute('select * from P3_POIDs_WBS_sum_rebar')

    Label(PO_info,text='-----rebar-----',fg='blue').grid(row=2,column=0)

    lb1.delete(0, END)
    lb2.delete(0, END)
    lb3.delete(0, END)
    lb4.delete(0, END)
    lb5.delete(0, END)
    lb6.delete(0, END)
    lb7.delete(0, END)
    lb8.delete(0, END)
    lb9.delete(0, END)
    lb10.delete(0, END)
    lb11.delete(0, END)
    lb12.delete(0, END)

    for i in cur:
        lb1.insert(1, i[2])
        lb2.insert(1, i[3])
        lb3.insert(1, i[1])
        lb4.insert(1, str(i[4])+'ton')
        lb5.insert(1, i[5])
        lb6.insert(1, i[6])
        lb7.insert(1, i[7])
        lb8.insert(1, i[8])
        lb9.insert(1, i[9])
        lb10.insert(1, i[10])
        lb11.insert(1, i[11])
        lb12.insert(1, i[12])

def show_element():
    global cur,c, column_name_track,column_name_PO,value_PO,value_track

    PO=value_PO[0].get()
    def scrollbarv_e(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)

    scbar=Scrollbar(orient='vertical',command=scrollbarv_e)
    lbe1 = Listbox(PO_info, yscrollcommand=scbar.set)
    lbe2 = Listbox(PO_info, yscrollcommand=scbar.set)
    lbe3 = Listbox(PO_info, yscrollcommand=scbar.set)
    lbe4 = Listbox(PO_info, yscrollcommand=scbar.set)
    lbe5 = Listbox(PO_info, yscrollcommand=scbar.set)

    lbe1.grid(row=6, column=0)
    lbe1.configure(width=0,height=10)
    lbe2.grid(row=6, column=1)
    lbe2.configure(width=0, height=10)
    lbe3.grid(row=6, column=2)
    lbe3.configure(width=0, height=10)
    lbe4.grid(row=6, column=3)
    lbe4.configure(width=0, height=10)
    lbe5.grid(row=6, column=4)
    lbe5.configure(width=0, height=10)
    scbar.grid(row=6,column=5,stick=N+S)

    lbe1.delete(0, END)
    lbe2.delete(0, END)
    lbe3.delete(0, END)
    lbe4.delete(0, END)
    lbe5.delete(0, END)

    if PO==['to be assigned']:
        top = Tk()
        Label(top, width=30, text='PO ID not assigned').grid(row=0, column=0)
        top.mainloop()
    else:
        # cur.execute('DROP TABLE IF EXISTS union_PO_1')
        # cur.execute('DROP TABLE IF EXISTS union_PO_2')
        # cur.execute('create table union_PO_1 as select * from BIM_Dynamo_column union select * from BIM_Dynamo_coreshearwall')
        # cur.execute('create table union_PO_2 as select * from union_PO_1 union select * from BIM_Dynamo_slab')
        # cur.execute('select * from union_PO_2 where POID=?',[PO])
        cur.execute('select * from BIM_Dynamo_column where POID=?',[PO])
        for i in cur:
            lbe1.insert(1, i[0])
            lbe2.insert(1, i[2])
            lbe3.insert(1, i[1])
            lbe4.insert(1, i[3])
            lbe5.insert(1, i[6])



def mainmenu():
    if flag=='lookahead':
        pjschedule.destroy()
    elif flag=='POs':
        PO_info.destroy()
