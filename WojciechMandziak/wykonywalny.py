from tkinter import *
from tkinter import ttk 
import tkinter as tk
import simplex
from tkinter import messagebox
from locale import _strip_padding
from distutils.dist import command_re
root=Tk()

r=0
c=0

def wypiszTablice(tab):
    print("-----------------")
    for row in tab:
        print(row)
    print("-----------------")

def fFile():
    num=[]
    num1=[]

    file = open("testowedane.txt", "r")
    for line in file:
        fs = [float(f) for f in line.split(",")]
        num.append(fs)
    z=num[0][0]
    c=num[1][0]  
    for x in range(2, len(num)):
        num1.append(num[x])   
    simplex.simplex(num1)   
    messagebox.showinfo("Simplex", "Wczytano z testowedane.txt, zapisano result.txt") 
         
def hello(dawword,daw3,daw,daw2,b_in,a_in,self):
    daw4=[]
    for i in range(len(daw)):
        aaaa=daw[i].get()
        daw4.append(aaaa)    
    daw.clear()
    for j in range(len(daw4)):
        bbbb=daw4[j]
        daw.append(bbbb)
    daw4.clear()
    for ii in range(len(daw2)):
        aa=daw2[ii].get()
        daw4.append(aa)
    daw2.clear()
    for jj in range(len(daw4)):
        bb=daw4[jj]
        daw2.append(bb)
    daw4.clear()       
    daw3.append(daw)
    daw3.extend(split_list(daw2, b_in))
     
    for row in dawword:
            if row.get() == "max":
               for g in range(len(daw3[0])-a_in):
                   daw3[0][g]=daw3[0][g]*-1
                   
            if row.get() == ">=":
                print(row)
                print(row.get())
                print(dawword.index(row))
                for g in range(len(daw3[1])-a_in):
                    daw3[dawword.index(row)][g]=daw3[dawword.index(row)][g]*-1       
       
    simplex.simplex(daw3)   
    daw.clear()
    daw2.clear()
    daw3.clear()
    dawword.clear()  
    self.destroy()
    messagebox.showinfo("Simplex", "Wyniki zapisano w pliku result.txt") 
       
def split_list(alist, wanted_parts):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

def disallow():
        window.bell()

def validate2(value_if_allowed,text):
        if text in "0123456789.'0.0'":
            return True
        else:
            disallow()
            return False    
def validate(value_if_allowed,text):
        if text in '0123456789.':
            return True
        else:
            disallow()
            return False
def close_window(self): 
    self.destroy()  
              
def adder(*args): # adder()
    def wypiszTablice(tab):
        print("-----------------")
        for row in tab:
            print(row)
        print("-----------------")
    
    try:      
        a_in=a.get()
        b_in=b.get()
        window1 = tk.Toplevel(root)
        vcmd2 = (window1.register(validate2),'%P', '%S')
        entry = {}
        entry2 = {}
        daw=[]
        daw2=[]
        daw3=[]
        dawword=[]
        label = {}
        i = 1
        j = 0
        items2 = ["min","max"]

        
        lb1=Label(window1, text='Funkcja celu:')
        lb1.grid(row=0, column=1,sticky = W)
        cb1_val = StringVar()
        cb1 = ttk.Combobox(window1, textvariable=cb1_val, height=4)
        cb1['values'] = items2 
        cb1.grid(row=1,column=1) 
        dawword.append(cb1_val)
            
        f=DoubleVar();
        f.set(0.0);
        daw.append(f);
        for index in range(a_in):
            e_val = DoubleVar()
            e = Entry(window1,textvariable=e_val,validate="key", validatecommand=vcmd2,width=10)
            
            e.grid(sticky=(W,E))
            e.grid(row=1, column=index+2)
            entry[index] = e

            daw.append(e_val)
            
            lb = Label(window1, text='x'+str(i))
            lb.grid(row=2, column=index+2)
            label[index] = lb
            i += 1   
        for iii in range(a_in):
            daw.append(f)
        items = ["<=",">=","="]
   
        lb1=Label(window1, text='Ograniczenia:')
        lb1.grid(row=4, column=1,sticky = W) 
        jedyn=DoubleVar()
        jedyn.set(1.0)
        l_j=0
        for index2 in range(b_in):
            cb_val = StringVar()
            cb = ttk.Combobox(window1, textvariable=cb_val, height=4)
            
            cb['values'] = items 
            cb.grid(row=5+index2,column=1) 
            dawword.append(cb_val)
            for index1 in range(a_in+1):
                e_val2 = DoubleVar()
                e1 = Entry(window1,textvariable=e_val2,validate="key", validatecommand=vcmd2,width=10)
                e1.grid(sticky=(W,E))
                e1.grid(row=5+index2, column=index1+2)
                entry2[index1] = e1
                daw2.append(e_val2)
                lb = Label(window1, text='x'+str(index1))
                lb.grid(row=6+index2, column=index1+2)
                label[index1] = lb
            for jjj in range(a_in):
                if(jjj==l_j):               
                    daw2.append(jedyn)
                else:
                    daw2.append(f)
            l_j+=1    
        ttk.Button(window1,text="START",command=lambda: hello(dawword,daw3,daw,daw2,b_in,a_in,window1)).grid(row=6+b_in+1,
column=a_in+1,sticky=E) 
        ttk.Button(window1,text="EXIT",command=lambda: close_window(window1)).grid(row=6+b_in+1,column=a_in+2,sticky=E)   
    except ValueError:
        pass

root.title("Simpex Python") 
window=ttk.Frame(root,padding="12 12 12 12") 
window.grid(column=0,row=0,sticky=(N,S))
window.columnconfigure(0,weight=1) 
window.rowconfigure(0,weight=1)    



txtin=StringVar() 
txtout=StringVar() 
a=IntVar() 
b=IntVar()


vcmd = (window.register(validate),'%P', '%S')
txt_entry=ttk.Entry(window,width=7,textvariable=txtin)

ttk.Label(window,text="Podaj liczbe zmiennych w modelu:").grid(row=1,
column=2,sticky=(W,E))

ttk.Label(window,text="zm = ").grid(row=2,column=1,sticky=E)
a_entry=ttk.Entry(window,width=3,validate="key", validatecommand=vcmd,textvariable=a)

a_entry.grid(row=2,column=2,sticky=(W,E))

ttk.Label(window,text="Podaj liczbe ograniczen:").grid(row=3,
column=2,sticky=(W,E))

ttk.Label(window, text="ogr = ").grid(row=4,column=1,sticky=E)
b_entry=ttk.Entry(window,width=3,validate="key", validatecommand=vcmd,textvariable=b)
b_entry.grid(row=4,column=2,sticky=(W,E))

ttk.Button(window,text="OK",command=adder).grid(row=6,
column=2,sticky=E) 
ttk.Button(window,text="Z Pliku...",command=fFile).grid(row=7,
column=2,sticky=E)

root.mainloop() 
root.destroy() 
