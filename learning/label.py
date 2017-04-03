from Tkinter import *
import tkMessageBox as tm

class RegisterFrame(Frame, object):
	def __init__(self, master):
		super(self.__class__, self).__init__()

		
		self.label_1 = Label(self, text="Username")
		self.label_2 = Label(self, text="Password")

		self.entry_1 = Entry(self)
		self.entry_2 = Entry(self, show="*")

		self.label_1.grid(row=0, sticky=E)
		self.label_2.grid(row=1, sticky=E)
		self.entry_1.grid(row=0, column=1)
		self.entry_2.grid(row=1, column=1)

		self.checkbox = Checkbutton(self, text="Keep me logged in")
		self.checkbox.grid(columnspan=2)

		self.logbtn = Button(self, text="Login", command = self.login)
		self.logbtn.grid(columnspan=2)

		self.pack()


	def login(self):
		username = self.entry1.get()
		password = self.entry2.get()

		if username == "john" and password == "password" :
			tm.showinfo("Login info", "Welcome John")
		else:
			tm.showerror("Login error", "Incorrect username")

root = Tk()
lf = RegisterFrame(root)
root.mainloop()