from Tkinter import *
from tkFileDialog import *
from shutil import *
import json
import os
import os.path
import threading 

#########################################
# Variable Start here
#########################################
root = Tk();
root.title("AskTriva");
root.geometry("640x480");
root.minsize(height = 0,width = 100);

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

def SetPath():
	"""Set the path of PROFILE_PIC_LINK and DATAFILEPATH"""
	# Get Current directory
	global currfilePath;
	global currdir;
	global parentDir;
	global PROFILE_PIC_LINK;
	global DATAFILEPATH;

	currfilePath = os.path.abspath(__file__);
	currdir = os.path.abspath(os.path.join(currfilePath,os.pardir));
	temp = currdir;
	# Keep go back to parent until grandfather of the program
	while (temp.split("\\")[-1] != MAINFOLDER):
		temp = os.path.abspath(os.path.join(temp,os.pardir)); # this will return parent directory.			

	# Initiazation
	parentDir = temp;
	PROFILE_PIC_LINK = parentDir + "\pic\profile.gif";
	DATAFILEPATH = parentDir + "\data\users.json";


def ShowWindow():
	"""To Initializating the element """
	#########################################
	# Text Initializating Start here
	#########################################
	# Read the information of user from data
	global TitleLabel;
	global Profile_Pic;
	global NameLabel;
	global DesTitleLabel;
	global DesLabel;
	global SaveDesButton;
	global PlayButton;
	global RandomQuesButton;
	global RankingButton;
	global PROFILE_HEIGHT;
	global PROFILE_WIDTH;
	global PROFILE_PIC_LINK;
	global DATAFILEPATH;
	global root;
	global framenumber;

	name = data['user1']['username'];
	level = data['user1']['level'];
	description = data['user1']['description'];
	# Create Name text and descption text
	TitleLabel = Label(root,text = "Profile",font = ("Arial",22),anchor = W); 
	NameLabel = Label(root,text = name + " Lvl " + level + "",font = ("Arial",14),anchor = W);
	DesTitleLabel = Label(root,text = "Description",font = ("Arial",10),anchor = W);
	DesLabel = Text(root,font = ("Arial",11),width = 60, height = 4);
	# Insert Previous Data
	DesLabel.insert(INSERT,description);
	# Create Button
	SaveDesButton = Button(root,text = "Save",command = SaveDes);
	RandomQuesButton = Button(root,text = "Get a Random Question",command = RandomQues);
	PlayButton = Button(root,text = "Play Now!",command = Play);
	RankingButton = Button(root,text = "View Ranking",command = Ranking);

	#########################################
	# Profile Picture Initializating Start here
	#########################################

	# Read profile picture
	fileformat = "gif -index 0"; # A format to read the frame of gif
	loaded_img = PhotoImage(file = PROFILE_PIC_LINK,format=fileformat);
	# Resize the profile picture to proper size
	img = loaded_img.subsample(loaded_img.width() / PROFILE_WIDTH,loaded_img.height() / PROFILE_HEIGHT);
	# Create profile picture
	Profile_Pic = Button(root,bd = 0,command = ChoosePicture ,image = img,bg = "white",height = img.height(),width = img.width());

	#########################################
	# Position Part
	#########################################
	# Place label on suitable position
	root.rowconfigure(0, weight=1);
	root.rowconfigure(1, weight=1);
	root.rowconfigure(2, weight=1);
	root.rowconfigure(3, weight=1);
	root.rowconfigure(4, weight=1);
	root.columnconfigure(0, weight=1);
	root.columnconfigure(1, weight=1);
	root.columnconfigure(2, weight=2);
	
	# Row 0
	TitleLabel.grid(row = 0,column = 0,ipady = 10,ipadx = 10,padx = 10,pady = 10,columnspan = 3);
	# Row 1
	Profile_Pic.grid(row = 1,column = 0,sticky = W,ipady = 10,ipadx = 10,padx = 30,pady = 20);
	NameLabel.grid(row = 1,column = 1,ipady = 10,ipadx = 10,padx = 20,pady = 10,sticky = 'ESNW',columnspan = 2);
	# Row 2
	DesTitleLabel.grid(row = 2,column = 0,padx = 12,sticky = W,columnspan = 3);
	# Row 3
	DesLabel.grid(row = 3,column = 0,padx = 10,columnspan = 2);
	SaveDesButton.grid(row = 3,column = 2,sticky = 'W');
	# Row 4
	PlayButton.grid(row = 4,column = 0,padx = 15,pady = 20,sticky = 'WE');
	RandomQuesButton.grid(row = 4,column = 1,padx = 15,pady = 20,sticky = 'WE');
	RankingButton.grid(row = 4,column = 2,padx = 15,pady = 20,sticky = 'WE');

	# Animate the profile pic to move
	framenumber = GetFrame(PROFILE_PIC_LINK);
	Animate(Profile_Pic,PROFILE_PIC_LINK,0.1);


def ChoosePicture():
	"""Popup a file window to ask user to choose a gif file, and change it to the Profile_Pic"""
	global framenumber;
	global frame_count;
	global Profile_Pic;
	global PROFILE_PIC_LINK;
	global animaterun;

	animaterun = False;
	filename = askopenfilename(title='Profile Picture',
						 filetypes= [('gif', '*.gif')] ,
						initialdir="/");
	if(filename != ""):
		# Reset the frame count
		frame_count = 0;
		dest = parentDir + "\pic";
		# Rmove the old profile picture file
		os.remove(PROFILE_PIC_LINK);
		# Copy the new one to the directory
		copy(filename,dest);
		# Rename the file to profile.gif
		destpicname = dest + "\\" + filename.split('/')[-1];
		os.rename(destpicname,PROFILE_PIC_LINK);
		# Update the framenumber of new profile gif
		framenumber = GetFrame(PROFILE_PIC_LINK);
	
	animaterun = True;
	Animate(Profile_Pic,PROFILE_PIC_LINK,0.1);

def ReadData(filepath):
	"""To Read the data from json file"""
	global data;
	# Open file and read
	with open(filepath,'r') as f:
		data = json.load(f);

def IsAnimate(filename,index):
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

def GetFrame(filename):
	"""Check one frame by one frame to count how many frame in a gif,
	return the number of frame in the end"""
	count = 0;
	while IsAnimate(filename,count):
		count = count + 1;
	return count;


def Animate(object,filename,speed = 0.1):
	"""So function will keep running to animate a gif"""
	# Increase the counter every time loop and change it back to original position after frame finish
	global framenumber;
	global frame_count;
	global animaterun;
	global PROFILE_WIDTH;
	global PROFILE_HEIGHT

	if(animaterun == True):
		try:
			frame_count = frame_count + 1;
			if(frame_count >= framenumber):
				frame_count = 0;

			# Read the correct frame
			fileformat = "gif -index " + str(frame_count);
			loaded_img = PhotoImage(file = filename,format=fileformat);

			# Resize it to proper size
			img = loaded_img.subsample(loaded_img.width() / PROFILE_WIDTH,loaded_img.height() / PROFILE_HEIGHT);
	
			# Replace with the new frame
			object.configure(image = img);
			object.image = img;
			# Keep run this function every {speed} second
			threading.Timer(speed,Animate,[object,filename]).start();  
		except:
			print "";

def SaveDes():
	"""Get the description from box and write it into the file"""
	# Get the input
	temp = DesLabel.get(1.0,END);
	# Remove the \n and edit the data
	des = temp.replace("\n","");
	data["user1"]["description"] = des;
	# Write it into the json file
	with open(DATAFILEPATH, 'w') as outfile:
		json.dump(data, outfile);


def RandomQues():
	print("Random Question");

def Play():
	print("Play");

def Ranking():
	print("Ranking");


#####################################
# Code below here is for testing purpose, it will be deleted in main.py after combined
#####################################

SetPath();
ReadData(DATAFILEPATH);
ShowWindow();


root.mainloop();
