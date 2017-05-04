from Tkinter import *

class win2(Frame):
	w = "";
	def __init__(self,win):
		Frame.__init__(self);
		self.w = win;
		
	def ShowWindow(self):
		RankingButton = Button(self.w,text = "Win2",command = self.Ranking);
		RankingButton.grid(row = 0,column = 0,ipady = 10,ipadx = 10,padx = 10,pady = 10,columnspan = 3);

	def Ranking(self):
		print(23);
