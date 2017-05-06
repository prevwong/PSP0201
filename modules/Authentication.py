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
Con_Pass = Label(RegWindow,text="Password Confirmation: ",bg=FrameColor,font="Arial")
ConPass = Entry(RegWindow,show="*")
RegWindow.withdraw()
users = {}



                
               
                
def Submit():
        
        if len(Password2.get()) <6:
                
                tkMessageBox.showerror("Error","Minimum length of Password is 6")

        elif len(Username2.get())<6:
                tkMessageBox.showerror("Error","Minimum length of Username is 6")
                
        elif ConPass.get() !=Password2.get():
                tkMessageBox.showerror("Error","Both Passwords did not match. Try Again")
        
        else:
                a = Password2.get()
                b = list(a)
                b.reverse()
                with open ("save.json", "r") as save:
                        users  = json.load(save)
                for i in range (0,len(users)):
                        if users[str(i)]["Username"] == Username2.get():
                                tkMessageBox.showerror("Error","Username:"+Username2.get()+" has been taken")
                                break
                        elif i == len(users)-1:
                                new_id = len(users)
                                users[new_id] = {}
                                users[new_id]["Username"]=Username2.get()
                                users[new_id]["Password"] = "".join(b)
                                users[new_id]["description"] = "Set Your Description"
                                users[new_id]["exp"]=0
                                users[new_id]["weeklyexp"]=0
                                
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
                users =json.load(save)
 

        for i in range(0,len(users)):
                c = users[str(i)]["Password"]
                d = list(c)
                d.reverse()
                if users[str(i)]["Username"] == Username1.get() and "".join(d)==Password1.get():
                        tkMessageBox.showinfo("Done","Login Successfully!")
                        Profile.deiconify()
                        LogWindow.withdraw()
                        break
                elif i == len(users) - 1:
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
Con_Pass.grid(row=4,column=3)
ConPass.grid(row=4,column=4)
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
