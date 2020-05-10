# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:25:54 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

print(__doc__)

"""
This script just for akuma

Ver: 2.1
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from load import load
from frame import frame_enrich,frame_curve

def warning():
    messagebox.showerror(title='Error!', message="You should choose a Folder!!!")

def choose_loadfile():
    loadfile = askopenfilename(filetypes=(("csv file", "*.csv*"), ("Excel file", "*.xlsx*;*.xls*"), ("Text file", "*.txt*")))
    if loadfile:
        var_read.set(loadfile)
        lb.delete(0,tk.END)
#        lb_id.delete(0,tk.END)
        lb_label.delete(0,tk.END)
        lb_Ascore.delete(0,tk.END)
        lb_Dscore.delete(0,tk.END)
        cols = list(load(loadfile,nrows=0).columns)      
        var_scores.set(cols)  

def lbtolabel():
    indexes = lb.curselection()[::-1]
    for idx in indexes: 
        lb_label.insert(0,lb.get(idx))
        lb.delete(idx)

def lbtoAscore():
    indexes = lb.curselection()[::-1]
    for idx in indexes:
        lb_Ascore.insert(0,lb.get(idx))
        lb.delete(idx)

def lbtoDscore():
    indexes = lb.curselection()[::-1]
    for idx in indexes: 
        lb_Dscore.insert(0,lb.get(idx))
        lb.delete(idx)

def labeltolb():
    indexs = lb_label.curselection()[::-1]
    for idx in indexs: 
        lb.insert(0,lb_label.get(idx))
        lb_label.delete(idx)

def Ascoretolb():
    indexs = lb_Ascore.curselection()[::-1]
    for idx in indexs: 
        lb.insert(0,lb_Ascore.get(idx))
        lb_Ascore.delete(idx)

def Dscoretolb():
    indexs = lb_Dscore.curselection()[::-1]
    for idx in indexs: 
        lb.insert(0,lb_Dscore.get(idx))
        lb_Dscore.delete(idx)

def start():
    if var_read.get():
#        df = load(var_read.get())
        label = list(lb_label.get(0,tk.END))[0]
        Dscore = list(lb_Dscore.get(0,tk.END))
        Ascore = list(lb_Ascore.get(0,tk.END))
        
        res = frame_enrich(file=var_read.get(),
                           label_col=label,
                           Ascore=Ascore,
                           Dscore=Dscore,
#                           scores=feature,
#                           descending=var_int.get(),
                           ratios=[0.001,0.01,0.05,0.1]
                           )
        print(res)
        if messagebox.askyesno('Finished!','Would you want to save the result?'):
            savefile = asksaveasfilename(filetypes=(("csv file", "*.csv*"),))
            if savefile:
                res.to_csv(savefile,index_label='Ratio')
            else:
                pass
        else:
            pass
        
    else:
        warning()

def draw():
    if var_read.get():
        label = list(lb_label.get(0,tk.END))[0]
        Dscore = list(lb_Dscore.get(0,tk.END))
        Ascore = list(lb_Ascore.get(0,tk.END))
#        savefile = asksaveasfilename(filetypes=(("csv file", "*.csv*"),))
        f = frame_curve(file=var_read.get(),
                         label_col=label,
                         Ascore=Ascore,
                         Dscore=Dscore)
#                         scores=feature,)
#        f.show()
        if messagebox.askyesno('Finished!','Would you want to save the figure?'):
            savefile = asksaveasfilename(filetypes=(("Pdf file", "*.pdf*"),("Png file", "*.png*")))
            if savefile:
                try:
                    f.savefig(savefile)
                except PermissionError:
                    messagebox.showerror(title='Error!', message="Permission Denied!!!")
            else:
                pass
        else:
            pass
        
    else:
        warning()
    
    

if '__main__'==__name__:
    root = tk.Tk()
    root.geometry('600x370+500+200')
    root.resizable(0,0)  
    bbg = tk.Label(root,bg='#fae8eb',width=500,height=300)
    bbg.pack()
    root.title("FrameWork Enrich")
    
    var_read = tk.StringVar()
    var_scores = tk.StringVar()
    var_int = tk.IntVar()
    
    btn1 = tk.Button(root, text='Select data file',font=('Arial', 10),command=choose_loadfile,width=15,height=1,bg='#d6c4dd').place(x=35,y=20)
    lr = tk.Label(root, textvariable=var_read, bg='#eaf6e8', fg='#494546', font=('Arial', 10),width=45,height=1
                  ).place(x=175,y=23)
      
    lb = tk.Listbox(root,selectmode='extended',listvariable=var_scores)
    lb.place(x=35,y=60,relwidth=0.3,relheight=0.8)
    scrollbar = tk.Scrollbar(lb,command=lb.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb.config(yscrollcommand=scrollbar.set)
    
    tk.Label(root,text='Value',bg='#fae8eb').place(x=35*9, y=65)
    lb_label = tk.Listbox(root,selectmode='extended')
    lb_label.place(x=35*8, y=85, relwidth=0.2, relheight=0.1)
    scrollbar = tk.Scrollbar(lb_label,command=lb_label.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb_label.config(yscrollcommand=scrollbar.set)
    
#    tk.Label(root,text='Scores',bg='#fae8eb').place(x=35*9, y=135)
#    lb_feature = tk.Listbox(root,selectmode='extended')
#    lb_feature.place(x=35*8, y=155, relwidth=0.2, relheight=0.50)
#    scrollbar = tk.Scrollbar(lb_feature,command=lb_feature.yview)
#    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#    lb_feature.config(yscrollcommand=scrollbar.set)
    
    tk.Label(root,text='Ascending Scores',bg='#fae8eb').place(x=35*8+5, y=145+5)
    lb_Ascore = tk.Listbox(root,selectmode='extended')
    lb_Ascore.place(x=35*8, y=165+5, relwidth=0.2, relheight=0.2)
    scrollbar = tk.Scrollbar(lb_Ascore,command=lb_Ascore.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb_Ascore.config(yscrollcommand=scrollbar.set)
    
    tk.Label(root,text='Descending Scores',bg='#fae8eb').place(x=35*8+5, y=235+5)
    lb_Dscore = tk.Listbox(root,selectmode='extended')
    lb_Dscore.place(x=35*8, y=255+5, relwidth=0.2, relheight=0.2)
    scrollbar = tk.Scrollbar(lb_Dscore,command=lb_Dscore.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb_Dscore.config(yscrollcommand=scrollbar.set)
    
    theButton = tk.Button(root, text="→", command=lbtolabel, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=70+5)
    theButton = tk.Button(root, text="←", command=labeltolb, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=110+5)
    
    theButton = tk.Button(root, text="→", command=lbtoAscore, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=168+5)
    theButton = tk.Button(root, text="←", command=Ascoretolb, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=208+5)                   
    
    theButton = tk.Button(root, text="→", command=lbtoDscore, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=258+5)
    theButton = tk.Button(root, text="←", command=Dscoretolb, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=298+5)     
    
    btn2 = tk.Button(root, text='Calculate',font=('Arial', 10),command=start,width=7,height=7,bg='#d6c4dd').place(x=430,y=140)
    btn3 = tk.Button(root, text='Draw',font=('Arial', 10),command=draw,width=7,height=7,bg='#d6c4dd').place(x=520,y=140)
                     
    root.mainloop()
    
    
    
    
    
    
    
    
    
    
    
    
    