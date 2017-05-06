import json
import urllib
import methods
import random
import HTMLParser
from Tkinter import *
import ttk
import guiquizselection 
import profile
import methods

parser = HTMLParser.HTMLParser()
canvas = "";
quest = [];
root=""
questions = "";
answers={}
submitBtn = "";
window ="";
master = ""
session_id = "0"

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

def on_mousescroll(event):
    # enable scrolling; defined speed
    canvas.yview_scroll( -1 * (event.delta), "units")

def quizUI(user_id, category, number):
    global canvas,answers,submitBtn,questions,window;

    window = Tk()
    window.resizable(width=False, height=False)
    
    # Retrieve the list of questions 
    questions = retrieve(user_id, category, number)
    
    # Creating a canvas to allow scrolling
    if len(questions) == 1:
        canvas = Canvas(window, width = 520, height = 300)
    else:
        canvas = Canvas(window, width=520, height=600)
    canvas.pack(side=LEFT, padx=30)

    # Scrollbar
    scrollbar = Scrollbar(window, command=canvas.yview)
    scrollbar.pack(side=LEFT, fill='y')
    canvas.configure(yscrollcommand = scrollbar.set)
    canvas.bind('<Configure>', on_configure)
    canvas.bind_all('<MouseWheel>', on_mousescroll)

    frame = Frame(canvas, width=600, pady=40);
    frame.grid()
    canvas.create_window((0,0), window=frame, anchor='nw')



    for i in range(0, len(questions)):
        options = questions[i]["options"]

        temp = [];
        temp.append(Label(frame, 
          wraplength=500,
          text= parser.unescape(questions[i]["question"]),
          justify = LEFT,
          padx = 10))
        temp[0].pack(side="top", pady=20, anchor=W)

        answers[i] = IntVar();

        for j in range(0, len(options)):
            temp.append(Radiobutton(frame, 
                        text=parser.unescape(options[j]),
                        padx = 10, 
                        variable=answers[i], 
                        value=j))
            temp[j+1].pack(side="top", anchor=W)
        quest.append(temp);
    
    submitBtn = Button(frame, text ="Submit", command = completedQuiz);
    submitBtn.pack(side="right")
        
    # Center Window
    methods.centerWindow(window);
    mainloop()


def retrieve(user_id, category, quantity):
    url = "https://opentdb.com/api.php?amount="+ str(quantity) +"&category=" + str(category)
    # Read JSON data from url
    response = urllib.urlopen(url)
    jsonData = json.loads(response.read())
    results = jsonData["results"]
    responseCode = jsonData["response_code"]

    questions = []
    if ( responseCode == 0 ) :
        for data in results:
            # Place them all in their respective variables
            difficulty, category, question, correct_answer, incorrect_answers = data["difficulty"], data["category"], data["question"], data["correct_answer"], data["incorrect_answers"]
            
            # Append the incorrect_answers list to our options list
            options = []
            options.extend(incorrect_answers)

            # Calculate a random index to place our correct_answer in the options list
            random_index = random.randrange(len(options)+1);
            options.insert(random_index, correct_answer)

            # Append it in the form of an object/dictionary to our questions list
            questions.append({ "question" : question, "options" : options, "correct_answer" : random_index })

        # Shuffle our questions
        random.shuffle(questions, random.random)
        
        return questions;

def close():
    global window, master,quest;
    window.destroy();
    quest = []
    profile.ShowWindow()


    


def completedQuiz():
    global root,quest,answers,submitBtn;
    submitBtn.config(text="Again!",command = close);
    calculateResults();

def CalculateLevel(correct, level = 1):
    correct -= (5 + 2*level)
    if correct <= 0:
        return level
    else:
        return CalculateLevel(correct, level+1)

def calculateResults():
    global root,quest,answers,submitBtn,questions;

    correct = 0
    incorrect = []
    for i in range(0, len(questions)):
        correct_answer = questions[i]["correct_answer"]
        selected_answer = answers[i].get()
        if ( selected_answer == correct_answer ) :
            correct += 1
        else: 
            incorrect.append(i)
        
        quest[i][correct_answer+1].configure(foreground = "green")
        for x in range(0, len(questions[i]["options"])):
            if(x != correct_answer):
                quest[i][x+1].config(foreground = "red")
            

    # Calculate percentage based on the no. of corrects over the no. of questions
    percentage = (float(correct) / float(len(questions))) * 100


    #The new window and the expcalculator starts here
    root = Tk()
    root.title("Scoreboard")
    root.geometry("700x400")

    def expadder(correct):
        users = methods.readData("users.json")
        exp = correct * 25
        users[session_id]["exp"] += exp
        users[session_id]["weeklyexp"] += exp     
        users[session_id]["level"] = CalculateLevel(users[session_id]["exp"] / 25)    
        methods.writeData(users, "users.json")
        return exp 
        

    label = Label(root, text= "Score for this round:" + "\n" +str(percentage) + "%" )
    label.pack(side='top',pady=50)
    label.config(font=("Courier", 40))

    expgain = Label(root, text = "Experience for this round:" + "\n" + str(expadder(correct)))
    expgain.pack()
    expgain.config(font=("Courier",30))

    root.mainloop();
    

    
def selection():
    global master;
    categorynum = {"Random":9,"Books":10,"Film":11,"Music":12,"Musicals & Theatres":13,"Television":14,"Video Games":15,"Board Games":16,
               "Science & Nature":17,"Computers":18,"Mathematics":19,"Mythology":20,"Sports":21,"Geography":22,"History":23,"Politics":24,"Art":25,
               "Celebrities":26,"Animals":27,"Vehicles":28,"Comics":29,"Gadgets":30,"Japanese Anime & Manga":31,"Cartoon & Animations":32}
               
    master = Tk()
    master.title("Pick your choice.")
    master.geometry("400x300")
    

    category_var = StringVar(master)
    category_var.set("Random") #default value
    category = ttk.Combobox(master, textvariable = category_var, values = ["Random","Books","Film","Music","Musicals & Theatres","Television","Video Games","Board Games",
                                                                           "Science & Nature","Computers","Mathematics","Mythology","Sports","Geography","History","Politics","Art",
                                                                           "Celebrities","Animals","Vehicles","Comics","Gadgets","Japanese Anime & Manga","Cartoon & Animations"])
    category.pack()
    category.place(relx=.5,rely=.4, anchor="center")
    
    number_var = StringVar(master)
    number_var.set("5") #default value
    num = ttk.Combobox(master, textvariable = number_var, values=["5","10","15","20"])
    num.pack()
    num.place(relx=.5,rely=.5,anchor="center")

    def getinput():
        category = category_var.get()
        category = categorynum[category]
        number = number_var.get()
        master.destroy();
        quizUI("1",category, number)

    Button(master, text = "Play!", command = getinput).pack(side=BOTTOM,pady= 50)
    master.mainloop()

