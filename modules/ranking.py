from Tkinter import *
import json
import os
import ttk
from datetime import datetime
from threading import Timer
from multiprocessing import Process
import time
import methods
import urllib

######################
# Functions required during UI rendering
######################

# The Sort by exp function, takes the argument (type of exp displayed, users json file)
def sort_exp(typeof, users):
    sorted_array = sorted(users, key=lambda x: int((users[str(x)][typeof])), reverse=True)
    i = 1
    info_array = {}
    for id in sorted_array:
        info_array[i]={}
        info_array[i]["name"] = users[id]["name"]
        info_array[i][typeof] = users[id][typeof]
        i = i + 1
    return info_array

# The reset weekly exp function, resets the weekly exp to 0
def reset_weeklyexp():    
    users = methods.readData("users.json")
    for i in range(0, len(users)):
        users[str(i)]["weeklyexp"] = 0  
    methods.writeData(users, "users.json")
    
# This reset at functions, take the argument of what time to reset, and add 7 days consequently for future resets
def reset_after(days = 7):
    reset_time = datetime(2017, 04, 30, 00, 00, 00)
    if datetime.now() >= reset_time:
        excess_days = int(str(datetime.now() - reset_time).split(" ")[0])
        if excess_days % 7 == 0:
            reset_weeklyexp()


##################
# Define the UI and show the UI
##################
#UI
def show_ranking():
    
    #Initialize users JSON

    url = "http://52.36.70.190:5002/public/"
    # Read JSON data from url
    error = 0;
    try:
        response = urllib.urlopen(url)
        try:
            users = json.loads(response.read())
        except ValueError:
            error = 1;
    except IOError:
        error = 1;

    if ( error == 1 ) :
        users = methods.readData("users.json")

    ###UI positioning###
    
    root = methods.defineWindow("AskTrivia Leaderboard", "320x400")
    root.rowconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)
    root.rowconfigure(2, weight = 1)
    tabs = ttk.Notebook(root)
    exp_frame = ttk.Frame(tabs)
    weeklyexp_frame = ttk.Frame(tabs)
    tabs.add(exp_frame, text = "Overall Ranking")
    tabs.add(weeklyexp_frame, text = "Ranking by week")
    tabs.grid(row = 1)
    
    leaderboard_text = Label(root, text = "Leaderboard",
                    font = "Times",
                    fg = "Black")
    leaderboard_text.grid(row=0, padx = 100)
    
    ##Overall ranking##
    rank_text = Label(exp_frame, text = "Rank")
    name_text = Label(exp_frame, text = "Name")
    exp_text = Label(exp_frame, text = "EXP")


    rank_text.grid(row=2,column = 0, columnspan = 2, pady = 10)
    name_text.grid(row=2,column = 2, columnspan = 2)
    exp_text.grid(row=2,column = 4, columnspan = 2)
    
    rank_by_exp = sort_exp("exp",users)
    if len(rank_by_exp) >= 1:
        for i in range(1, len(rank_by_exp)+1):
            if i == 11:
                break
            rank = Label(exp_frame, text = str(i)).grid(row = i + 2, column = 0, columnspan = 2)
            name = Label(exp_frame, text = rank_by_exp[i]["name"]).grid(row = i + 2, column = 2, columnspan = 2, sticky = W)
            exp = Label(exp_frame, text = rank_by_exp[i]["exp"]).grid(row = i + 2, column = 4, columnspan = 2, sticky = E)
            
    #ranking by week        
    rank_text = Label(weeklyexp_frame, text = "Rank")
    name_text = Label(weeklyexp_frame, text = "Name")
    exp_text = Label(weeklyexp_frame, text = "EXP")

    rank_text.grid(row=2,column = 0, columnspan = 2, pady = 10)
    name_text.grid(row=2,column = 2, columnspan = 2)
    exp_text.grid(row=2,column = 4, columnspan = 2)

    rank_by_exp = sort_exp("weekly_exp",users)
    if len(rank_by_exp) >= 1:
        for i in range(1, len(rank_by_exp)+1):
            if i == 11:
                break
            rank = Label(weeklyexp_frame, text = str(i)).grid(row = i + 2, column = 0, columnspan = 2)
            name = Label(weeklyexp_frame, text = rank_by_exp[i]["name"]).grid(row = i + 2, column = 2, columnspan = 2, sticky = W)
            exp = Label(weeklyexp_frame, text = rank_by_exp[i]["weekly_exp"]).grid(row = i + 2, column = 4, columnspan = 2, sticky = E)
            

    root.mainloop()
    
reset_after()


