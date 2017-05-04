from Tkinter import *
from win1 import win1
from win2 import win2

window1 = Tk();
window1.title("AskTriva");
window1.geometry("640x480");
window1.minsize(height = 0,width = 100);

x = win1(window1);
x.ShowWindow();

window1.mainloop();



