from Tkinter import *
import json
import os
import ttk
#ui

def show_ranking():
    
    cur_path = os.path.dirname(__file__)
    new_path = os.path.join(cur_path, "../data/test.json")
    with open(new_path) as infile:
        raw_file = json.load(infile)
        users = json.loads(raw_file)
    
    root = Tk()
    tabs = ttk.Notebook(root)
    exp_frame = ttk.Frame(tabs)
    weeklyexp_frame = ttk.Frame(tabs)
    tabs.add(exp_frame, text = "Overall Ranking")
    tabs.add(weeklyexp_frame, text = "Ranking by week")
    tabs.grid(row = 1)
    
    leaderboard_text = Label(root, text = "Leaderboard",
                    font = "Times",
                    fg = "Black")
    leaderboard_text.grid(row=0)
    
    #Overall ranking
    rank_text = Label(exp_frame, text = "Rank")
    name_text = Label(exp_frame, text = "Name")
    exp_text = Label(exp_frame, text = "EXP")


    rank_text.grid(row=2,column = 0, columnspan = 2, pady = 10)
    name_text.grid(row=2,column = 2, columnspan = 2)
    exp_text.grid(row=2,column = 4, columnspan = 2)

    rank_by_exp = sort_by_exp(users)
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

    rank_by_exp = sort_by_weeklyexp(users)
    if len(rank_by_exp) <= 10:
        for i in range(1, len(rank_by_exp)+1):
            rank = Label(weeklyexp_frame, text = str(i)).grid(row = i + 2, column = 0, columnspan = 2)
            name = Label(weeklyexp_frame, text = rank_by_exp[i]["name"]).grid(row = i + 2, column = 2, columnspan = 2, sticky = W)
            exp = Label(weeklyexp_frame, text = rank_by_exp[i]["weeklyexp"]).grid(row = i + 2, column = 4, columnspan = 2, sticky = E)
            

    root.mainloop()

#sort by exp
    
def sort_by_exp(users):
    exp_sorted = sorted(users, key=lambda x: int((users[str(x)]["exp"])), reverse=True)
    i = 1
    info_array = {}
    for id in exp_sorted:
        info_array[i]={}
        info_array[i]["name"] = users[id]["name"]
        info_array[i]["exp"] = users[id]["exp"]
        i = i + 1
    return info_array
    
#sort by weekly exp
def sort_by_weeklyexp(users):
    weeklyexp_sorted = sorted(users, key=lambda x: int((users[str(x)]["weeklyexp"])), reverse=True)
    i = 1
    info_array = {}
    for id in weeklyexp_sorted:
        info_array[i]={}
        info_array[i]["name"] = users[id]["name"]
        info_array[i]["weeklyexp"] = users[id]["weeklyexp"]
        i = i + 1
    return info_array


show_ranking()
