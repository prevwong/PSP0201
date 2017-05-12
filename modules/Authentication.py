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

      
      users = methods.readData("users.json")

      url = "http://52.36.70.190:5002/usernames/"
      # Read JSON data from url
      error = 0;
      try:
         response = urllib.urlopen(url)
         try:
            data = json.loads(response.read())
         except ValueError:
            error = 1;
      except IOError:
         error = 1;


      if ( error == 1 ) :
         '''
         for i in range (0,len(users)):
            if users[str(i)]["name"] == username:
               tkMessageBox.showerror("Error","Username:"+username+" has been taken")
               break
            elif i == len(users)-1:
               new_id = len(users)
               users[new_id] = {}
               users[new_id]["name"]= username
               users[new_id]["password"] = encrypt(password)
               users[new_id]["description"] = "Set Your Description"
               users[new_id]["exp"]=0
               users[new_id]["weeklyexp"]=0
               users[new_id]["level"] = 1
                       
               methods.writeData(users, "users.json")
               post(users)       
               tkMessageBox.showinfo("Done","Register Successfully!")
         '''
         tkMessageBox.showinfo("Error","Internet connection/Server down")
      else:
         users = data["users"]
         error = 0;
         for i in users:
            if username == i :
               error = 1;
               break;
         if ( error == 1 ) :
            print "username has been taken"
            tkMessageBox.showerror("Error","Username:"+username+" has been taken")

         else:
            newUser = methods.URLRequest("http://52.36.70.190:5002/adduser/", { "name" : username, "password" : encrypt(password), "description" : "Set your description" })
            users = methods.readData("users.json")
            users[json.loads(newUser)["id"]] = {"name" : username, "password" : encrypt(password), "description" : "Set your description", "exp" : 0, "weekly_exp" : 0, "level" : 1}
            methods.writeData(users, "users.json")
            tkMessageBox.showinfo("Done","Register Successfully!")


def Back():
    RegWindow.withdraw()
    LogWindow.deiconify()

def Register():
    RegWindow.deiconify()
    LogWindow.withdraw()
        
def login(username, password):
   
   users = methods.readData("users.json") 

   request = methods.URLRequest("http://52.36.70.190:5002/loginUser/", { "name" : username })

   print request
   if ( request != None ):
      response = json.loads(request);
      print response
      if ( ( "error" in response and response["error"] == True ) or decrypt(response["password"]) != password ):
         tkMessageBox.showerror("Error","Please Try Again!")
      else:
            tkMessageBox.showinfo("Done","Login Successfully!")
         

            LogWindow.destroy()
            RegWindow.destroy()
            profile.session_id = response["id"]
            profile.show_window()

   else:
      print "logging in locally"
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
        


