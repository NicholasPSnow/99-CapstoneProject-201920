# Put whatever you want in this module and do whatever you want with it.
# It exists here as a place where you can "try out" things without harm.

from tkinter import *
from tkinter.ttk import *

tk=Tk()
progress=Progressbar(tk,orient=HORIZONTAL,length=100,mode='determinate')

def bar():
    import time
    progress['value']=0
    tk.update_idletasks()
    time.sleep(1)
    progress['value']=20
    tk.update_idletasks()
    time.sleep(1)
    progress['value']=50
    tk.update_idletasks()
    time.sleep(1)
    progress['value']=80
    tk.update_idletasks()
    time.sleep(1)
    progress['value']=100

progress.pack()
Button(tk,text='foo',command=bar).pack()
mainloop()