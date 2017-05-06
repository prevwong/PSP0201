from Tkinter import *
import json
import os
import ttk
from datetime import datetime
from threading import Timer
import time
import methods

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
    users = methods.readData()
    for i in range(0, len(users)):
        users[str(i)]["weeklyexp"] = 0  
    methods.writeData(users)
    
# This reset at functions, take the argument of what time to reset, and add 7 days consequently for future resets
def reset_at(year = 2017, month = 04, day = 30, hour = 21, minutes = 41, seconds = 0):
    reset_time = datetime(year, month, day, hour, minutes, seconds)
    while datetime.now() < reset_time:
        time.sleep(1)
    reset_weeklyexp()

##################
# Define the UI and show the UI
##################
#UI
def show_ranking():
    
    #Initialize users JSON
    users = methods.readData()
    
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
    if len(rank_by_exp) <= 10:
        for i in range(1, len(rank_by_exp)+1):
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

    rank_by_exp = sort_exp("weeklyexp",users)
    if len(rank_by_exp) <= 10:
        for i in range(1, len(rank_by_exp)+1):
            rank = Label(weeklyexp_frame, text = str(i)).grid(row = i + 2, column = 0, columnspan = 2)
            name = Label(weeklyexp_frame, text = rank_by_exp[i]["name"]).grid(row = i + 2, column = 2, columnspan = 2, sticky = W)
            exp = Label(weeklyexp_frame, text = rank_by_exp[i]["weeklyexp"]).grid(row = i + 2, column = 4, columnspan = 2, sticky = E)
            

    root.mainloop()



show_ranking()
