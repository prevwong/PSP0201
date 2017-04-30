from Tkinter import *
import json
import threading  

class Profile(Frame):
    """Profile Gui"""
    #########################################
    # Variable Start here
    #########################################
    data = 0;
    frame_count = 1;    # As a counter for gif frame later
    fileformat = "gif -index 1"; # A format to read the frame of gif

    #########################################
    # Constant Variable Start here
    #########################################
    PROFILE_HEIGHT = 90;
    PROFILE_WIDTH = 90;
    PROFILE_PIC_LINK = "pic/profile.gif";

    #########################################
    # Function Start here
    #########################################
    def __init__(self, datafilename, master=None):
        """Class Initializating Function"""
        Frame.__init__(self, master)
        self.filename = datafilename;
        self.ReadData();
        self.InitElement();
        self.ShowElement();
        #########################################
        # Other
        #########################################
        # Animate the profile pic to move
        self.Animate(self.profile_pic,self.PROFILE_PIC_LINK,self.GetFrame(self.PROFILE_PIC_LINK),0.06);
        self.pack();

    def InitElement(self):
        """To Initializating the element """
        #########################################
        # Text Initializating Start here
        #########################################
        # Read the information of user from data
        name = self.data['user1']['username'];
        level = self.data['user1']['level'];
        description = self.data['user1']['description'];
        # Create Name text and descption text
        self.NameLabel = Label(self,text = name + " Lvl " + level + "",font = ("Arial",14),anchor = W);
        self.DesLabel = Label(self,text = description,font = ("Arial",11),justify = LEFT,wraplength = 540);
        #########################################
        # Profile Picture Initializating Start here
        #########################################
        # Read profile picture
        self.loaded_img = PhotoImage(file = self.PROFILE_PIC_LINK,format=self.fileformat);
        # Resize the profile picture to proper size
        self.img = self.loaded_img.subsample(self.loaded_img.width() / self.PROFILE_WIDTH,self.loaded_img.height() / self.PROFILE_HEIGHT);
        # Create profile picture
        self.profile_pic = Label(self, image = self.img,bg = "white",height = self.img.height(),width = self.img.width());

    def ShowElement(self):
        """To show and position the element"""
        #########################################
        # Position Part
        #########################################
        # Place label on suitable position
        self.columnconfigure(0, weight=2);
        self.rowconfigure(0, weight=3);
        self.rowconfigure(1, weight=1);
        self.profile_pic.grid(row = 0,column = 0,sticky = W,pady = 10,padx = 10);
        self.NameLabel.grid(row = 0,column = 1,pady = 10,padx = 10);
        self.DesLabel.grid(row = 1,column = 0,columnspan = 2,sticky = W, padx = 10, pady = 10);

    def ReadData(self):
        """To Read the data from json file"""
        # Open file and read
        with open(self.filename,"r") as f:
            self.data = json.load(f);

    def IsAnimate(self,filename,index):
        """To check it is the frame in gif exists,
        if then return true,
        if not return false""" 

        # Set the format of reading gif
        f = "gif -index " + str(index);
        # Use exception since it will trigger error while frame not exists
        try:
            # Trying to open the frame of gif
            img = PhotoImage(file = filename,format=f);
            return True;
        except:
            return False;

    def GetFrame(self,filename):
        """Check one frame by one frame to count how many frame in a gif,
        return the number of frame in the end"""
        count = 1;
        while self.IsAnimate(filename,count):
            count = count + 1;
        return count;

    def Animate(self,object,filename,framenumber,speed = 0.06):
        """So function will keep running to animate a gif"""
        # Increase the counter every time loop and change it back to original position after frame finish
        Profile.frame_count = Profile.frame_count + 1;
        if(Profile.frame_count >= framenumber):
            Profile.frame_count = 1;

        # Read the correct frame
        fileformat = "gif -index " + str(Profile.frame_count);
        loaded_img = PhotoImage(file = filename,format=fileformat);

        # Resize it to proper size
        scale_width = loaded_img.width() / self.PROFILE_WIDTH;
        scale_height = loaded_img.height() / self.PROFILE_HEIGHT;
        img = loaded_img.subsample(scale_width,scale_height);

        # Replace with the new frame
        object.configure(image = img);
        object.image = img;

        # Keep run this function every {speed} second
        threading.Timer(speed, self.Animate,[object,filename,framenumber]).start();

root = Tk();
root.title("AskTriva");
root.geometry("640x480");
root.minsize(height = 0,width = 100);
x = Profile("data/users.json",root);

root.mainloop();
