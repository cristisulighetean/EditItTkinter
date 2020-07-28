from tkinter import *
from tkinter import ttk
import math
import sys

myApp = Tk()
myApp.title(" Program ")
myApp.geometry("1000x1200")

tasktabs=ttk.Notebook(myApp)

TabOne=ttk.Frame(tasktabs)
tasktabs.add(TabOne,text="Tab One")

TabOne=ttk.Frame(tasktabs)
tasktabs.add(TabOne,text="Tab Two")

def deletetab():
    tasktabs.forget(tasktabs.select())

DelButton=Button(myApp,text=' Delete  ', command=deletetab)
DelButton.grid(row=0,column=3, sticky="W")


tasktabs.grid(row=0,column=0,sticky="W")

myApp.mainloop()