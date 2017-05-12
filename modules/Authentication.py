from Tkinter import *
import tkMessageBox
import json
import os
import methods
import profile
import urllib
import urllib2

def encrypt(string):
        result = ""
        for i in xrange(0,len(string)):
                result += chr(ord(string[i]) - 10);
        return result

def decrypt(string):
        result = ""
        for i in xrange(0,len(string)):
                result += chr(ord(string[i]) + 10);
        return result
    
def submit(username,password,password_confirmation):

      
      if len(username) <6:
         tkMessageBox.showerror("Error","Minimum length of username is 6")
         return
      if len(password)<6:
         tkMessageBox.showerror("Error","Minimum length of password is 6")
         return
      if password_confirmation != password:
         tkMessageBox.showerror("Error","Both Passwords did not match. Try Again")
         return

      data = methods.readRemoteJson("usernames")
      # If connection to remote server failed due to internet failure or error in request
      if ( data == False ) :
         tkMessageBox.showinfo("Error","Internet connection/Server down")
      else:
         error = 0;

         # If there are users currently existing in the remote database, check:
         if ( data != None ) : 
            users = data["users"]
            for i in users:
              if username == i :
                 error = 1;
                 break;
            if ( error == 1 ) :
              print "username has been taken"
              tkMessageBox.showerror("Error","Username:"+username+" has been taken")

         else:
            # Send a POST request to adduser/ with parameters: name, password, description. These parameters will be stored in the remote database.
            newUser = methods.postRemote("adduser", { "name" : username, "password" : encrypt(password), "description" : "Set your description" })
            # Save users profile locally as well
            saveUserLocally(json.loads(newUser)["id"], username, password, "Set your description", 0, 0, 1)
            tkMessageBox.showinfo("Done","Register Successfully!")

def saveUserLocally(userId, username, password, description, exp, weekly_exp, level):
  # Save users profile locally as well
  users = methods.readData("users.json")
  users[str(userId)] = {"name" : username, "password" : encrypt(password), "description" : description, "exp" : exp, "weekly_exp" : weekly_exp, "level" : level}
  methods.writeData(users, "users.json")

def Back():
    RegWindow.withdraw()
    LogWindow.deiconify()

def Register():
    RegWindow.deiconify()
    LogWindow.withdraw()
        
def login(username, password):
   
   request = methods.postRemote("loginUser", { "name" : username })

   print request

   # If request did not fail: 
   if ( request != None ):
      data = json.loads(request);
      # If there are errors ( caused by non-existing username ) and password does not match the password stored in the database:
      if ( ( "error" in data and data["error"] == True ) or decrypt(data["password"]) != password ):
         tkMessageBox.showerror("Error","Please Try Again!")
      else:
            tkMessageBox.showinfo("Done","Login Successfully!")
            saveUserLocally(i, username, password, data["description"], data["exp"], data["weekly_exp"], data["level"])
            LogWindow.destroy()
            RegWindow.destroy()
            profile.session_id = data["id"]
            profile.show_window()
   else:
      # If request to remote server failed, log in locally
      print "logging in locally"
      users = methods.readData("users.json") 
      counter = 0;
      for i in users:
         counter = counter + 1
         if users[str(i)]["name"] == username and decrypt(users[str(i)]["password"])==password:
            tkMessageBox.showinfo("Done","Login Successfully!")
            LogWindow.destroy()
            RegWindow.destroy()
            profile.session_id = str(i)
            profile.show_window()
            break
         else:
            if (counter == len(users) - 1) :
               tkMessageBox.showerror("Error","Please Try Again!")
               break;
            else:
               continue;
         


def show_window():
        global LogWindow, RegWindow
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
        
        #Button
        ButtonColor = "light green"

        submitButton = Button (RegWindow,text = "    Submit    ",command= lambda: submit(Reg_Username.get(), Reg_Password.get(), Confirmation_Pass.get()), bg="Pink",activebackground = "white",activeforeground ="black")
        backButton=Button(RegWindow,text ="    Back    ",command=Back,bg=ButtonColor,activebackground = "white",activeforeground ="black")
        registerButton=Button(LogWindow,text="    Register    ",command= Register,bg=ButtonColor,activebackground = "white",activeforeground="black")
        loginButton = Button(LogWindow,text = "    Login    ",command= lambda: login(Log_Username.get(), Log_Password.get()),bg="Pink",activebackground = "white",activeforeground="black")

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
        


