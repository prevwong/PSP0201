from Tkinter import *
import ttk



def main():
    master = Tk()
    master.title("Pick your choice.")
    master.geometry("400x300")
    
    variable = StringVar(master)
    variable.set("Category") # default value
    category = ttk.Combobox(master, textvariable = variable, values = ["Random","Books","Film","Music","Musicals & Theatres","Television","Video Games","Board Games","Science & Nature","Computers","Mathematics","Mythology","Sports","Geography","History","Politics","Art","Celebrities","Animals","Vehicles","Comics","Gadgets","Japanese Anime & Manga","Cartoon & Animations"])
    category.pack()
    category.place(relx=.5,rely=.4, anchor="center")
    
    variable1 = StringVar(master)
    variable1.set("Number of question")
    num = ttk.Combobox(master, textvariable = variable1, values=["5","10","15","20"])
    num.pack()
    num.place(relx=.5,rely=.5,anchor="center")
    
        
    master.mainloop()

if __name__ == "__main__":
    main()
