from Tkinter import *
import tkMessageBox
import json

#First Window
LogWindow = Tk()
LogWindow.title("AskTrivia")
LogWindow.geometry("500x300")
FrameColor = "light blue"
LogWindow.configure(bg=FrameColor)

LogUser = Label(LogWindow,text = "Username: ",bg=FrameColor,font="Arial").grid()
Username1 = Entry(LogWindow)
Username1.grid(row=0,column=1)
LogPass = Label (LogWindow,text="Password: ",bg=FrameColor,font="Arial").grid()
Password1 = Entry(LogWindow,show = "*")
Password1.grid(row=1,column=1)

#SecondWindow
RegWindow = Tk()
RegWindow.title("Register")
RegWindow.geometry("500x300")
RegWindow.configure(bg = FrameColor)

RegUser = Label (RegWindow,text="Username: ",bg=FrameColor,font="Arial").grid()
Username2 = Entry(RegWindow)
Username2.grid(row=0,column=1)
RegPass = Label(RegWindow,text="Password: ",bg=FrameColor,font="Arial").grid()
Password2 = Entry(RegWindow,show="*")
Password2.grid(row=1,column=1)
RegWindow.withdraw()
data = 0
def Submit():
	users[0]["Username"]=Username2.get()
	users[0]["Password"]=Password2.get()
	with open ("save.json","w") as save:
		json.dump(users,save)
	print users
	
def Back():
    RegWindow.withdraw()
    LogWindow.deiconify()

def Register():
    RegWindow.deiconify()
    LogWindow.withdraw()
	
def Login(): 
	with open ("save.json","r") as save:
		json.load(save)
	if users["0"]["Username"] == Username1.get() or users["0"]["Password"]==Password1.get():
		print "yes"
	else:
		print"no"

users = {}
users[0] = {}
ButtonColor = "light green"
submitButton = Button (RegWindow,text = "Submit",command=Submit).grid()
backButton=Button(RegWindow,text ="Back",command=Back,bg=ButtonColor,activebackground = "white",activeforeground ="black").grid()
registerButton=Button(LogWindow,text="Register",command=Register,bg=ButtonColor,activebackground = "white",activeforeground="black").grid()
loginButton = Button(LogWindow,text = "Login",command=Login).grid()
LogWindow.mainloop()