from Tkinter import *
import Tkinter as Tk
import ttk


def main():
    categorynum = {"Random":9,"Books":10,"Film":11,"Music":12,"Musicals & Theatres":13,"Television":14,"Video Games":15,"Board Games":16,
               "Science & Nature":17,"Computers":18,"Mathematics":19,"Mythology":20,"Sports":21,"Geography":22,"History":23,"Politics":24,"Art":25,
               "Celebrities":26,"Animals":27,"Vehicles":28,"Comics":29,"Gadgets":30,"Japanese Anime & Manga":31,"Cartoon & Animations":32}

    def createwindow():
        window = Tk.Toplevel(master)

    def getinput():
        category = category_var.get()
        category = categorynum[category]
        number = number_var.get()
        questions = retrieve(category, quantity)
        displayquestion(question)

    master = Tk()
    master.title("Pick your choice.")
    master.geometry("400x300")

    category_var = StringVar(master)
    category_var.set("Category") #default value
    category = ttk.Combobox(master, textvariable = category_var, values = ["Random","Books","Film","Music","Musicals & Theatres","Television","Video Games","Board Games",
                                                                           "Science & Nature","Computers","Mathematics","Mythology","Sports","Geography","History","Politics","Art",
                                                                           "Celebrities","Animals","Vehicles","Comics","Gadgets","Japanese Anime & Manga","Cartoon & Animations"])
    category.pack()
    category.place(relx=.5,rely=.4, anchor="center")
    
    number_var = StringVar(master)
    number_var.set("Number of question") #default value
    num = ttk.Combobox(master, textvariable = number_var, values=["5","10","15","20"])
    num.pack()
    num.place(relx=.5,rely=.5,anchor="center")

    Button(master, text = "Play!", command = getinput,command = createwindow).pack(side=BOTTOM,pady= 50)
    

        
    master.mainloop()




main()
