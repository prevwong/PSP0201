from Tkinter import *
import tkMessageBox
import json
import os
cur_path = os.path.dirname(__file__)
new_path = os.path.join(cur_path, "../data/save.json")
#First Window
LogWindow = Tk()
LogWindow.title("AskTrivia")
LogWindow.geometry("500x300")
FrameColor = "light blue"
LogWindow.configure(bg=FrameColor)
Welcome = Label(LogWindow,text = "Welcome to\n AskTrivia",bg=FrameColor,font="Arial")

LogUser = Label(LogWindow,text = "Username:",bg=FrameColor,font="Arial")
Log_Username = Entry(LogWindow)
LogPass = Label (LogWindow,text="Password:",bg=FrameColor,font="Arial")
Log_Password = Entry(LogWindow,show = "*")

#SecondWindow
RegWindow = Tk()
RegWindow.title("Register")
RegWindow.geometry("500x300")
RegWindow.configure(bg = FrameColor)
RegWord = Label (RegWindow,text="REGISTER",font = "Arial",bg=FrameColor)

RegUser = Label (RegWindow,text="Username: ",bg=FrameColor,font="Arial")
Reg_Username = Entry(RegWindow)
RegPass = Label(RegWindow,text="Password: ",bg=FrameColor,font="Arial")
Reg_Password = Entry(RegWindow,show="*")
ConfirmationPass = Label(RegWindow,text="Password Confirmation: ",bg=FrameColor,font="Arial")
Confirmation_Pass = Entry(RegWindow,show="*")
RegWindow.withdraw()
users = {}
 
                
def Submit():
        
        if len(Reg_Password.get()) <6:
                
                tkMessageBox.showerror("Error","Minimum length of Password is 6")

        elif len(Reg_Username.get())<6:
                tkMessageBox.showerror("Error","Minimum length of Username is 6")
                
        elif Confirmation_Pass.get() !=Reg_Password.get():
                tkMessageBox.showerror("Error","Both Passwords did not match. Try Again")
        
        else:
                a = Reg_Password.get()
                b = list(a)
                b.reverse()
                with open (new_path) as save:
                        users  = json.load(save)
                for i in range (0,len(users)):
                        if users[str(i)]["Username"] == Reg_Username.get():
                                tkMessageBox.showerror("Error","Username:"+Reg_Username.get()+" has been taken")
                                break
                        elif i == len(users)-1:
                                new_id = len(users)
                                users[new_id] = {}
                                users[new_id]["Username"]=Reg_Username.get()
                                users[new_id]["Password"] = "".join(b)
                                users[new_id]["description"] = "Set Your Description"
                                users[new_id]["exp"]=0
                                users[new_id]["weeklyexp"]=0
                                
                                with open (new_path,"w") as save:
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
        with open (new_path) as save:
                users =json.load(save)
 

        for i in range(0,len(users)):
                c = users[str(i)]["Password"]
                d = list(c)
                d.reverse()
                if users[str(i)]["Username"] == Log_Username.get() and "".join(d)==Log_Password.get():
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
Log_Username.grid(row=2,column=4)
LogPass.grid(row=3,column=3)
Log_Password.grid(row=3,column=4)

loginButton.grid(row=5,column=3)
registerButton.grid(row=5,column=4)


#Adjust Lining RegWindow
RegSpaceX1 = Label (RegWindow,text="            ",bg=FrameColor).grid(row=0,column=0)
RegSpaceY1 = Label (RegWindow,text=" ",bg=FrameColor).grid(row=1,column=0)
RegSpaceY2 = Label (RegWindow,text=" ",bg=FrameColor).grid(row=4,column=0)
RegSpaceY3 = Label (RegWindow,text=" ",bg=FrameColor).grid(row=5,column=0)
RegWord.grid(row=0,column=4)
RegUser.grid(row=2,column=3)
Reg_Username.grid(row=2,column=4)
RegPass.grid(row=3,column=3)
Reg_Password.grid(row=3,column=4)
ConfirmationPass.grid(row=4,column=3)
Confirmation_Pass.grid(row=4,column=4)
submitButton.grid(row=6,column=3)
backButton.grid(row=6,column=4)



LogWindow.mainloop()
