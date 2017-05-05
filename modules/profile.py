from Tkinter import *
from tkFileDialog import *
from shutil import *
import json
import os
import os.path
import threading 

class Profile(Frame):
	"""Profile Gui"""
	#########################################
	# Variable Start here
	#########################################
	data = 0;
	frame_count = 0;    # As a counter for gif frame later
	framenumber = 0;
	animaterun = True;

	# Get the current directory and dest directory
	currfilePath = "";	# Initialization in SetPath
	currdir = "";	# Initialization in SetPath
	parentDir = "";	# Initialization in SetPath

	#########################################
	# Constant Variable Start here
	#########################################
	PROFILE_HEIGHT = 90;
	PROFILE_WIDTH = 90;
	PROFILE_PIC_LINK = "";	# Initialization in SetPath
	DATAFILEPATH = "";	# Initialization in SetPath
	MAINFOLDER = "PSP0201";

	TitleLabel = "";
	Profile_Pic = "";
	NameLabel = "";
	DesTitleLabel = "";
	DesLabel = "";
	SaveDesButton = "";
	PlayButton = "";
	RandomQuesButton = "";
	RankingButton = "";

	#########################################
	# Function Start here
	#########################################
	def __init__(self):
		"""Class Initializating Function"""
		Frame.__init__(self);
		self.SetPath();
		self.ReadData();


	def SetPath(self):
		"""Set the path of PROFILE_PIC_LINK and DATAFILEPATH"""
		# Get Current directory
		self.currfilePath = os.path.abspath(__file__);
		self.currdir = os.path.abspath(os.path.join(self.currfilePath,os.pardir));
		temp = self.currdir;

		# Keep go back to parent until grandfather of the program
		while (temp.split("\\")[-1] != self.MAINFOLDER):
			temp = os.path.abspath(os.path.join(temp,os.pardir)); # this will return parent directory.			

		# Initiazation
		self.parentDir = temp;
		self.PROFILE_PIC_LINK = self.parentDir + "/pic/profile.gif";
		self.DATAFILEPATH = self.parentDir + "/data/users.json";

	def ShowWindow(self):
		"""To Initializating the element """
		#########################################
		# Text Initializating Start here
		#########################################
		# Read the information of user from data
		name = self.data['user1']['username'];
		level = self.data['user1']['level'];
		description = self.data['user1']['description'];
		# Create Name text and descption text
		self.TitleLabel = Label(self,text = "Profile",font = ("Arial",22),anchor = W); 
		self.NameLabel = Label(self,text = name + " Lvl " + level + "",font = ("Arial",14),anchor = W);
		self.DesTitleLabel = Label(self,text = "Description",font = ("Arial",10),anchor = W);
		self.DesLabel = Text(self,font = ("Arial",11),width = 60, height = 4);
		# Insert Previous Data
		self.DesLabel.insert(INSERT,description);
		# Create Button
		self.SaveDesButton = Button(self,text = "Save",command = self.SaveDes);
		self.RandomQuesButton = Button(self,text = "Get a Random Question",command = self.RandomQues);
		self.PlayButton = Button(self,text = "Play Now!",command = self.Play);
		self.RankingButton = Button(self,text = "View Ranking",command = self.Ranking);

		#########################################
		# Profile Picture Initializating Start here
		#########################################
		# Read profile picture
		fileformat = "gif -index 0"; # A format to read the frame of gif
		loaded_img = PhotoImage(file = self.PROFILE_PIC_LINK,format=fileformat);
		# Resize the profile picture to proper size
		img = loaded_img.subsample(loaded_img.width() / self.PROFILE_WIDTH,loaded_img.height() / self.PROFILE_HEIGHT);
		# Create profile picture
		self.Profile_Pic = Button(self,bd = 0,command = self.ChoosePicture ,image = img,bg = "white",height = img.height(),width = img.width());

		#########################################
		# Position Part
		#########################################
		# Place label on suitable position
		self.rowconfigure(0, weight=1);
		self.rowconfigure(1, weight=1);
		self.rowconfigure(2, weight=1);
		self.rowconfigure(3, weight=1);
		self.rowconfigure(4, weight=1);
		self.columnconfigure(0, weight=1);
		self.columnconfigure(1, weight=1);
		self.columnconfigure(2, weight=2);
		
		# Row 0
		self.TitleLabel.grid(row = 0,column = 0,ipady = 10,ipadx = 10,padx = 10,pady = 10,columnspan = 3);
		# Row 1
		self.Profile_Pic.grid(row = 1,column = 0,sticky = W,ipady = 10,ipadx = 10,padx = 30,pady = 20);
		self.NameLabel.grid(row = 1,column = 1,ipady = 10,ipadx = 10,padx = 20,pady = 10,sticky = 'ESNW',columnspan = 2);
		# Row 2
		self.DesTitleLabel.grid(row = 2,column = 0,padx = 12,sticky = W,columnspan = 3);
		# Row 3
		self.DesLabel.grid(row = 3,column = 0,padx = 10,columnspan = 2);
		self.SaveDesButton.grid(row = 3,column = 2,sticky = 'W');
		# Row 4
		self.PlayButton.grid(row = 4,column = 0,padx = 15,pady = 20,sticky = 'WE');
		self.RandomQuesButton.grid(row = 4,column = 1,padx = 15,pady = 20,sticky = 'WE');
		self.RankingButton.grid(row = 4,column = 2,padx = 15,pady = 20,sticky = 'WE');

		# Animate the profile pic to move
		Profile.framenumber = self.GetFrame(self.PROFILE_PIC_LINK);
		self.Animate(self.Profile_Pic,self.PROFILE_PIC_LINK,0.1);
		self.pack();

	def ChoosePicture(self):
		Profile.animaterun = False;
		filename = askopenfilename(title='Profile Picture',
							 filetypes= [('gif', '*.gif')] ,
							initialdir="/");
		if(filename != ""):
			# Reset the frame count
			Profile.frame_count = 0;
			dest = self.parentDir + "\pic";
			# Rmove the old profile picture file
			os.remove(self.parentDir + "\pic\profile.gif");
			# Copy the new one to the directory
			copy(filename,dest);
			# Rename the file to profile.gif
			destpicname = dest + "\\" + filename.split('/')[-1];
			os.rename(destpicname,self.parentDir + "\pic\profile.gif");
			# Update the framenumber of new profile gif
			Profile.framenumber = self.GetFrame(self.PROFILE_PIC_LINK);
		
		Profile.animaterun = True;
		self.Animate(self.Profile_Pic,self.PROFILE_PIC_LINK,0.1);

	def ReadData(self):
		"""To Read the data from json file"""
		# Open file and read
		with open(self.DATAFILEPATH,"r") as f:
			self.data = json.load(f);

	def IsAnimate(self,filename,index):
		"""To check it is the frame in gif exists,
		if then return true,
		if not return false""" 
		try:
			# Set the format of reading gif
			f = "gif -index " + str(index);
			# Use exception since it will trigger error while frame not exists

			# Trying to open the frame of gif
			img = PhotoImage(file = filename,format=f);
			return True;
		except:
			return False;

	def GetFrame(self,filename):
		"""Check one frame by one frame to count how many frame in a gif,
		return the number of frame in the end"""
		count = 0;
		while self.IsAnimate(filename,count):
			count = count + 1;
		return count;


	def Animate(self,object,filename,speed = 0.1):
		"""So function will keep running to animate a gif"""
		# Increase the counter every time loop and change it back to original position after frame finish
		if(Profile.animaterun == True):
			try:
				Profile.frame_count = Profile.frame_count + 1;
				if(Profile.frame_count >= Profile.framenumber):
					Profile.frame_count = 0;

				# Read the correct frame
				fileformat = "gif -index " + str(Profile.frame_count);
				loaded_img = PhotoImage(file = filename,format=fileformat);

				# Resize it to proper size
				img = loaded_img.subsample(loaded_img.width() / Profile.PROFILE_WIDTH,loaded_img.height() / Profile.PROFILE_HEIGHT);
		
				# Replace with the new frame
				object.configure(image = img);
				object.image = img;
				# Keep run this function every {speed} second
				threading.Timer(speed,self.Animate,[object,filename]).start();  
			except:
				print "";

	def SaveDes(self):
		"""Get the description from box and write it into the file"""
		# Get the input
		temp = self.DesLabel.get(1.0,END);
		# Remove the \n and edit the data
		des = temp.replace("\n","");
		self.data["user1"]["description"] = des;
		# Write it into the json file
		with open(self.DATAFILEPATH, 'w') as outfile:
			json.dump(self.data, outfile);


	def RandomQues(self):
		print("Random Question");

	def Play(self):
		print("Play");

	def Ranking(self):
		print("Ranking");


#####################################
# Code below here is for testing purpose, it will be deleted in main.py after combined
#####################################
root = Tk();
root.title("AskTriva");
root.geometry("640x480");
root.minsize(height = 0,width = 100);
x = Profile();
x.ShowWindow();

root.mainloop();
