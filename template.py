from Tkinter import *

###########################################
# Every function inside class must have argument (self)
# Every variable that want to use that outside function but inside class need use self.
###########################################

class ClassName(Frame):
	#########################################
	# Variable Start here
	#########################################
	
	# ...

	#########################################
	# Constant Variable Start here
	#########################################
	
	# ...

	#########################################
	# Function Start here
	#########################################
	def __init__(self):
		Frame.__init__(self)
		self.InitElement();
		self.pack();

	def ShowWindow(self):
		# Initialize your Element and pack it here

#####################################
# Code below here is for testing purpose, it will be deleted in main.py after combined
#####################################
root = Tk();
root.title("AskTriva");
root.geometry("640x480");
root.minsize(height = 0,width = 100);
x = ClassName();
x.ShowWindow();

root.mainloop();
