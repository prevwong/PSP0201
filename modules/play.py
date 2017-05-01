from Tkinter import *
import tkMessageBox
import json

#First Window
LogWindow = Tk()
LogWindow.title("AskTrivia")
LogWindow.geometry("500x300")
FrameColor = "light blue"
LogWindow.configure(bg=FrameColor)
Welcome = Label(LogWindow,text = "Welcome to\n AskTrivia",bg=FrameColor,font="Arial")

LogUser = Label(LogWindow,text = "Username:",bg=FrameColor,font="Arial")
Username1 = Entry(LogWindow)
LogPass = Label (LogWindow,text="Password:",bg=FrameColor,font="Arial")
Password1 = Entry(LogWindow,show = "*")

#SecondWindow
RegWindow = Tk()
RegWindow.title("Register")
RegWindow.geometry("500x300")
RegWindow.configure(bg = FrameColor)
RegWord = Label (RegWindow,text="REGISTER",font = "Arial",bg=FrameColor)

RegUser = Label (RegWindow,text="Username: ",bg=FrameColor,font="Arial")
Username2 = Entry(RegWindow)
RegPass = Label(RegWindow,text="Password: ",bg=FrameColor,font="Arial")
Password2 = Entry(RegWindow,show="*")
RegWindow.withdraw()

data = 0
users = {}
users[0] = {}

def Submit():
	users[0]["Username"]=Username2.get()
	users[0]["Password"]=Password2.get()
	with open ("save.json","w") as save:
		json.dump(users,save)
	print users
	tkMessageBox.showinfo("Done","Register Successfully!")
	
def Back():
    RegWindow.withdraw()
    LogWindow.deiconify()

def Register():
    RegWindow.deiconify()
    LogWindow.withdraw()
	
def Login(): 
	with open ("save.json","r") as save:
		json.load(save)
	if users[0]["Username"] == Username1.get() and users[0]["Password"]==Password1.get():
		tkMessageBox.showinfo("Done","Login Successfully!")
		Profile.deiconify()
		LogWindow.withdraw()
	else:
		tkMessageBox.showerror("Error","Please Try Again!")
		
#Profile Window
Profile = Tk()
Profile.title("Profile")
Profile.geometry("500x300")
Profile.withdraw()
#Button
ButtonColor = "light green"

submitButton = Button (RegWindow,text = "    Submit    ",command=Submit,bg="Pink",activebackground = "white",activeforeground ="black")
backButton=Button(RegWindow,text ="    Back    ",command=Back,bg=ButtonColor,activebackground = "white",activeforeground ="black")
registerButton=Button(LogWindow,text="    Register    ",command=Register,bg=ButtonColor,activebackground = "white",activeforeground="black")
loginButton = Button(LogWindow,text = "    Login    ",command=Login,bg="Pink",activebackground = "white",activeforeground="black")

#Adjust Lining LogWindow
LogSpaceX1 = Label (LogWindow,text="                                 ",bg=FrameColor).grid(row=0,column=0)
LogSpaceY1 = Label (LogWindow,text=" ",bg=FrameColor).grid(row=1,column=0)
LogSpaceY2 = Label (LogWindow,text=" ",bg=FrameColor).grid(row=4,column=0)
Welcome.grid(row=0,column=4)
LogUser.grid(row=2,column=3)
Username1.grid(row=2,column=4)
LogPass.grid(row=3,column=3)
Password1.grid(row=3,column=4)
loginButton.grid(row=5,column=3)
registerButton.grid(row=5,column=4)

#Adjust Lining RegWindow
RegSpaceX1 = Label (RegWindow,text="                                 ",bg=FrameColor).grid(row=0,column=0)
RegSpaceY1 = Label (RegWindow,text=" ",bg=FrameColor).grid(row=1,column=0)
RegSpaceY2 = Label (RegWindow,text=" ",bg=FrameColor).grid(row=4,column=0)
RegWord.grid(row=0,column=4)
RegUser.grid(row=2,column=3)
Username2.grid(row=2,column=4)
RegPass.grid(row=3,column=3)
Password2.grid(row=3,column=4)
submitButton.grid(row=5,column=3)
backButton.grid(row=5,column=4)


LogWindow.mainloop()