# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 21:12:12 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

__doc__="""This script may only be suit for my kouhai"""


print(__doc__)

from load import load
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from CV_shap import CV_shap
from Draw import Draw

def warning():
    messagebox.showerror(title='Error!', message="You should choose a Folder!!!")
    

    
def choose_loadfile():
    loadfile = askopenfilename(filetypes=(("csv file", "*.csv*"), ("Excel file", "*.xlsx*;*.xls*"), ("Text file", "*.txt*")))
    if loadfile:
        var_read.set(loadfile)
        lb.delete(0,tk.END)
#        lb_id.delete(0,tk.END)
        lb_label.delete(0,tk.END)
        lb_feature.delete(0,tk.END)
        cols = list(load(loadfile).columns)      
        var_scores.set(cols)  
        
def lbtolabel():
    indexes = lb.curselection()[::-1]
    for idx in indexes: 
        lb_label.insert(0,lb.get(idx))
        lb.delete(idx)

def lbtofeature():
    indexes = lb.curselection()[::-1]
    for idx in indexes:
        lb_feature.insert(0,lb.get(idx))
        lb.delete(idx)

def labeltolb():
    indexs = lb_label.curselection()[::-1]
    for idx in indexs: 
        lb.insert(0,lb_label.get(idx))
        lb_label.delete(idx)

def featuretolb():
    indexs = lb_feature.curselection()[::-1]
    for idx in indexs: 
        lb.insert(0,lb_feature.get(idx))
        lb_feature.delete(idx)
        
def get_shap_cv():
    if var_read.get():
        label = list(lb_label.get(0,tk.END))[0]
        feature = list(lb_feature.get(0,tk.END))
        cv_shap = CV_shap(var_read.get(),label,feature,var_loop.get())
        data = cv_shap.get_cv_shap()
        var_shap_data.set(data.to_dict())
        if messagebox.askyesno('Finished!','Would you want to save the result?'):
            savefile = asksaveasfilename(filetypes=(("csv file", "*.csv*"),))
            if savefile:
                print('------------------------------')
                print('>>> Saving')
                data.to_csv(savefile,index=False)
                print('>>> Saved')
                print('------------------------------\n')
            else:
                pass
        else:
            pass
    else:
        warning()
    
    
def draw():
    def hist():
        savedir = asksaveasfilename(filetypes=(("png file", "*.png*"),))
        top = var_top_4.get()
        d.draw_hist(top,savedir,dpi=300)
    
    def scatter():
        savedir = asksaveasfilename(filetypes=(("png file", "*.png*"),))
        label = cmb.get()
        d.draw_scatter(label,savedir,dpi=300)
    
    def violin():
        savedir = asksaveasfilename(filetypes=(("png file", "*.png*"),))
        top = var_top.get()
        d.draw_violin(top,savedir,dpi=300)
    
    def summary():
        savedir = asksaveasfilename(filetypes=(("png file", "*.png*"),))
        top = var_top_2.get()
        cols = list(lb_feature.get(0,tk.END))
        d.draw_summary(top,cols,savedir,dpi=300)
    
    def force():
        savedir = asksaveasfilename(filetypes=(("png file", "*.png*"),))
        idx = var_top_3.get()
        cols = list(lb_feature.get(0,tk.END))
        d.draw_force(idx,cols,savedir,dpi=300)
    
    
    if var_read.get():
        print('------------------------------')
        print('>>> Loading...')
        if var_int.get():
            shap_file = askopenfilename(filetypes=(("csv file", "*.csv*"), ("Excel file", "*.xlsx*;*.xls*"), ("Text file", "*.txt*")))
            print(shap_file)
            if shap_file:
                d = Draw(var_read.get(), loading=True, shap_data=shap_file)
            else:
                d = None
        else:
            import pandas as pd
            d = Draw(var_read.get(), loading=False, shap_data=pd.DataFrame(eval(var_shap_data.get())))
        
        
        
        if d:
            d.get_abs_mean()            
            win = tk.Toplevel(root)
            bbg = tk.Label(win,bg='#fae8eb',width=500,height=300)
            bbg.pack()
            
            win.geometry('600x370+900+300')
            win.resizable(0,0)
            win.title('Draw')
            win.wm_attributes("-topmost", 1)
            cmb = ttk.Combobox(win)
            cmb.place(x=200,y=95)
            cmb['value'] = list(lb_feature.get(0,tk.END))

            var_top_4 = tk.IntVar(value=10)
            btn1 = tk.Button(win, text='Draw hist',width=14,height=2,command=hist,bg='#cd1041',font=('Arial', 10))
            btn1.place(x=60,y=30)
            e4 = tk.Entry(win, show=None, font=('Arial', 10), textvariable=var_top_4,width=14)
            e4.place(x=200, y=50)
            
            btn2 = tk.Button(win, text='Draw scatter',width=14,height=2,command=scatter,bg='#cd1041',font=('Arial', 10))
            btn2.place(x=60,y=90)
            
            var_top = tk.IntVar(value=10)
            btn3 = tk.Button(win, text='Draw violin',width=14,height=2,command=violin,bg='#cd1041',font=('Arial', 10))
            btn3.place(x=60,y=150)
            e2 = tk.Entry(win, show=None, font=('Arial', 10), textvariable=var_top,width=14)
            e2.place(x=200, y=170)
            
            var_top_2 = tk.IntVar(value=10)
            btn4 = tk.Button(win, text='Draw summary',width=14,height=2,command=summary,bg='#cd1041',font=('Arial', 10))
            btn4.place(x=60,y=210)
            e4 = tk.Entry(win, show=None, font=('Arial', 10), textvariable=var_top_2,width=14)
            e4.place(x=200, y=230)
            
            var_top_3 = tk.IntVar(value=0)
            btn4 = tk.Button(win, text='Draw force',width=14,height=2,command=force,bg='#cd1041',font=('Arial', 10))
            btn4.place(x=60,y=270)
            e4 = tk.Entry(win, show=None, font=('Arial', 10), textvariable=var_top_3,width=14)
            e4.place(x=200, y=290)
        else:
            pass
        
    else:
        messagebox.showerror(title='Error!', message="You should choose a Folder!!!")
    print('>>> Finished')
    print('------------------------------\n')
 
if '__main__'==__name__:
    root = tk.Tk()
    root.geometry('600x370+200+300')
    root.resizable(0,0)  
    bbg = tk.Label(root,bg='#fae8eb',width=500,height=300)
    bbg.pack()
    root.title("Explaining your xgb model with SHAP (Ziyi ver.)")
    
    var_read = tk.StringVar()
    var_scores = tk.StringVar()
    var_loop = tk.IntVar(value=10)
    var_shap_data = tk.StringVar()
    var_int = tk.IntVar()
    
    btn1 = tk.Button(root, text='Select data file',font=('Arial', 10),command=choose_loadfile,width=15,height=1,bg='#d6c4dd').place(x=35,y=20)
    lr = tk.Label(root, textvariable=var_read, bg='#eaf6e8', fg='#494546', font=('Arial', 10),width=45,height=1
                  ).place(x=175,y=23)
      
    lb = tk.Listbox(root,selectmode='extended',listvariable=var_scores)
    lb.place(x=35,y=60,relwidth=0.3,relheight=0.8)
    scrollbar = tk.Scrollbar(lb,command=lb.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb.config(yscrollcommand=scrollbar.set)
    
    tk.Label(root,text='Label',bg='#fae8eb').place(x=35*9, y=65)
    lb_label = tk.Listbox(root,selectmode='extended')
    lb_label.place(x=35*8, y=85, relwidth=0.2, relheight=0.1)
    scrollbar = tk.Scrollbar(lb_label,command=lb_label.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb_label.config(yscrollcommand=scrollbar.set)
    
    tk.Label(root,text='Features',bg='#fae8eb').place(x=35*9, y=135)
    lb_feature = tk.Listbox(root,selectmode='extended')
    lb_feature.place(x=35*8, y=155, relwidth=0.2, relheight=0.50)
    scrollbar = tk.Scrollbar(lb_feature,command=lb_feature.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb_feature.config(yscrollcommand=scrollbar.set)
    
    theButton = tk.Button(root, text="→", command=lbtolabel, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=70+5)
    theButton = tk.Button(root, text="←", command=labeltolb, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=110+5)
    
    theButton = tk.Button(root, text="→", command=lbtofeature, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=198+5)
    theButton = tk.Button(root, text="←", command=featuretolb, bg='#cd1041', height=1)
    theButton.place(x=30*8,y=238+5)       
    
    tk.Label(root,text='Loop times',bg='#fae8eb',font=('Arial', 10)).place(x=430, y=100)
    e1 = tk.Entry(root, show=None, font=('Arial', 10), textvariable=var_loop,width=6)
    e1.place(x=500, y=100)

    btn2 = tk.Button(root, text='Get SHAP CV',font=('Arial', 10),command=get_shap_cv,width=14,height=2,bg='#d6c4dd').place(x=450,y=180)
    btn3 = tk.Button(root, text='Draw Sth',font=('Arial', 10),command=draw,width=14,height=2,bg='#d6c4dd').place(x=450,y=240)
    
    c1 = tk.Checkbutton(root, text='Load', variable=var_int, onvalue=1, offvalue=0, bg='#fae8eb')
    c1.place(x=450, y=285+30)
#    btn2 = tk.Button(root, text='START',font=('Arial', 10),command=start,width=7,height=7,bg='#d6c4dd').place(x=470,y=140)
#    
#    c1 = tk.Checkbutton(root, text='Descending', variable=var_int, onvalue=0, offvalue=1, bg='#fae8eb')
#    c1.place(x=450, y=285+30)               
                     
    root.mainloop()

    