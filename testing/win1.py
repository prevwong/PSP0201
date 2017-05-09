from Tkinter import *
from win2 import win2

class win1(Frame):
	
	def __init__(self,win):
		#Frame.__init__(self);
		self.w = win;
		
	def ShowWindow(self):
		RankingButton = Button(self.w,text = "Window 1",command = self.Ranking);
		RankingButton.grid(row = 0,column = 0,ipady = 10,ipadx = 10,padx = 10,pady = 10,columnspan = 3);

	def Ranking(self):
		self.w.withdraw();
		window2 = Tk();
		window2.title("AskTriva");
		window2.geometry("640x480");
		window2.minsize(height = 0,width = 100);
		window2.withdraw();

		win2(window2).ShowWindow();
		window2.deiconify();

