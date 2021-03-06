from Tkinter import *
from tkFileDialog import *
from shutil import *
import json
import os
import os.path
import threading
import methods
import quiz
import authentication
import tkMessageBox
from random import *
#########################################
# Variable Start here
#########################################

session_id = "0"
quiz.session_id = session_id
frame_count = 0;    # As a counter for gif frame later
framenumber = 0;
animaterun = True;

#########################################
# Constant Variable Start here
#########################################
PROFILE_HEIGHT = 90;
PROFILE_WIDTH = 90;
PROFILE_PIC_LINK = methods.read_data("pic/profile.gif");  # Initialization in SetPathTitleLabel = "";
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

def show_window():
        '''To initialize window'''

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
        #SetPath();
        #ReadData(DATAFILEPATH);
        root = methods.define_window("AskTrivia", "640x480")
        root.minsize(height = 0,width = 100);
        data = methods.get_user_data(session_id);
        name = data['name'];
        level = data['level'];
        description = data['description'];
        # Create Name text and descption text
        TitleLabel = Label(root,text = "Profile",font = ("Arial",22),anchor = W); 
        NameLabel = Label(root,text = name + " Lvl " + `level` + "",font = ("Arial",14),anchor = W);
        DesTitleLabel = Label(root,text = "Description",font = ("Arial",10),anchor = W);
        DesLabel = Text(root,font = ("Arial",11),width = 60, height = 4);
        # Insert Previous Data
        DesLabel.insert(INSERT,description);
        # Create Button
        SaveDesButton = Button(root,text = "Save",command = save_des);
        RandomQuesButton = Button(root,text = "Get a Random Question",command = random_ques);
        PlayButton = Button(root,text = "Play Now!",command = play);
        RankingButton = Button(root,text = "View Ranking",command = ranking);
        LogoutButton = Button(root,text = "Logout",command = lambda: logout(data["name"]));

        #########################################
        # Profile Picture Initializating Start here
        #########################################

        # Read profile picture
        fileformat = "gif -index 0"; # A format to read the frame of gif
        loaded_img = PhotoImage(file = PROFILE_PIC_LINK,format=fileformat);
        # Resize the profile picture to proper size
        img = loaded_img.subsample(loaded_img.width() / PROFILE_WIDTH,loaded_img.height() / PROFILE_HEIGHT);
        # Create profile picture
        Profile_Pic = Button(root,bd = 0,command = choose_picture ,image = img,bg = "white",height = img.height(),width = img.width());

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
        root.columnconfigure(2, weight=1);
        root.columnconfigure(3, weight=1);
        
        # Row 0
        TitleLabel.grid(row = 0,column = 0,ipady = 10,ipadx = 10,padx = 10,pady = 10,columnspan = 4);
        # Row 1
        Profile_Pic.grid(row = 1,column = 0,sticky = W,ipady = 10,ipadx = 10,padx = 30,pady = 20);
        NameLabel.grid(row = 1,column = 1,ipady = 10,ipadx = 10,padx = 20,pady = 10,sticky = 'ESNW',columnspan = 3);
        # Row 2
        DesTitleLabel.grid(row = 2,column = 0,padx = 12,sticky = W,columnspan = 4);
        # Row 3
        DesLabel.grid(row = 3,column = 0,padx = 10,columnspan = 3);
        SaveDesButton.grid(row = 3,column = 3,sticky = 'W');
        # Row 4
        PlayButton.grid(row = 4,column = 0,padx = 15,pady = 20,sticky = 'WE');
        RandomQuesButton.grid(row = 4,column = 1,padx = 15,pady = 20,sticky = 'WE');
        RankingButton.grid(row = 4,column = 2,padx = 15,pady = 20,sticky = 'WE');
        LogoutButton.grid(row = 4,column = 3,padx = 15,pady = 20,sticky = 'WE');

        # Animate the profile pic to move
        framenumber = get_frame(PROFILE_PIC_LINK);
        animate(Profile_Pic,PROFILE_PIC_LINK,0.1);

        root.mainloop();

def choose_picture():
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
        dest = os.path.dirname(PROFILE_PIC_LINK);
        # Rmove the old profile picture file
        os.remove(PROFILE_PIC_LINK);
        # Copy the new one to the directory
        copy(filename,dest);
        # Rename the file to profile.gif
        destpicname = dest + "\\" + filename.split('/')[-1];
        os.rename(destpicname,PROFILE_PIC_LINK);
        # Update the framenumber of new profile gif
        framenumber = get_frame(PROFILE_PIC_LINK);
    
    animaterun = True;
    animate(Profile_Pic,PROFILE_PIC_LINK,0.1);

def is_animate(filename,index):
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

def get_frame(filename):
    """Check one frame by one frame to count how many frame in a gif,
    return the number of frame in the end"""
    count = 0;
    while is_animate(filename,count):
            count = count + 1;
    return count;


def animate(object,filename,speed = 0.1):
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
            threading.Timer(speed,animate,[object,filename]).start();  
        except:
            print "";

def save_des():
    """Get the description from box and write it into the file"""
    users = methods.read_data("users.json")
    # Get the input
    temp = DesLabel.get(1.0,END);
    # Remove the \n and edit the data
    des = temp.replace("\n","");
    users[str(session_id)]["description"] = des;
    # Write it into the json file
    methods.write_data(users, "users.json")

    methods.post_remote("updateDescription", { "id" : session_id, "description" : des })


def random_ques():
    quiz.session_id = session_id
    root.destroy();
    quiz.quizUI(randint(9,32),1) 
    
def play():
    quiz.session_id = session_id
    root.destroy()
    quiz.selection()
def ranking():
    import ranking
    ranking.show_ranking()

def logout(name):
    result = tkMessageBox.askquestion("Logout Confirmation", "Are you sure you want to logout?", icon='warning')
    if result == 'yes':
        message = "See you again, " + name + "!"
        tkMessageBox.showinfo("Thank you", message)
        root.destroy()
        authentication.show_window()

    
