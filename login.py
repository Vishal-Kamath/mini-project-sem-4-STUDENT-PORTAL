from tkinter import *
from tkinter import messagebox
from database_connection import DBHelper
from detectface import detect_face
import main

class login_class():

    def doSomething(self, event):
        self.window.attributes("-fullscreen", False)

    def fullscreen(self, event):
        self.window.attributes("-fullscreen", True)

    def submit(self):
        id = self.id_entry.get()
        if self.username_entry.get() != '' and self.password_entry.get() != '' and id != '':
            db_con = DBHelper()
            student = db_con.fetch_student_info(id)
            if self.username_entry.get() == student[0][3] and self.password_entry.get() == student[0][4]:
                detected = detect_face(id)
                if detected:
                    for widget in self.window.winfo_children():
                        widget.destroy()
                    self.window.destroy()
                    main.main(Tk(), id)
                else:
                    print("not detected")
            else:
                messagebox.showerror("error", "Please fill the correct user details")
        else:
            messagebox.showerror("error", "Please fill the correct user details")


    def __init__(self, root):
        self.window = root

        self.window.title('LOGIN')
        self.window.config(bg="#321b37")
        self.window.bind("<Escape>",self.doSomething)
        self.window.bind("<f>",self.fullscreen)
        self.window.attributes("-fullscreen", True)

        Title = Label(self.window, text="STUDENT PORTAL LOGIN", font=('Varela Round', 25), width=150, height=1,bg="#4c2853", fg='white', anchor=W)
        Title.place(x=0,y=0)

        self.login_frame = Frame(self.window, width=800, height= 500, bg="#4c2853")

        title_label = Label(self.login_frame, text="Enter your info", font=("Varela Round", 25),bg="#4c2853",fg='white')
        title_label.grid(sticky=W, row=0, column=0,columnspan=2)

        username_label = Label(self.login_frame, text="Username: ",font=('Varela Round', 20), bg="#4c2853", fg='white', width=15, anchor=W)
        username_label.grid(row=1, column=0)
        self.username_entry = Entry(self.login_frame,font=('Varela Round', 17))
        self.username_entry.grid(row=1, column=1)

        password_label = Label(self.login_frame, text="Password: ",font=('Varela Round', 20), bg="#4c2853",fg='white', width=15, anchor=W)
        password_label.grid(row=2, column=0)
        self.password_entry = Entry(self.login_frame,font=('Varela Round', 17),show="*")
        self.password_entry.grid(row=2, column=1)

        id_label = Label(self.login_frame, text="ID: ",font=('Varela Round', 20), bg="#4c2853",fg='white', width=15, anchor=W)
        id_label.grid(row=3, column=0)
        self.id_entry = Entry(self.login_frame,font=('Varela Round', 17))
        self.id_entry.grid(row=3, column=1)

        submit_button = Button(self.login_frame, text="Submit",font=('Varela Round', 20), bg="#4c2853",fg='white', width=33, command=self.submit)
        submit_button.grid(row=6, column=0, columnspan=2)

        self.login_frame.grid(row=0, column=0, sticky="")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0,weight=1)

        self.window.mainloop()

if __name__ == "__main__":
    root = Tk()
    login_class(root)