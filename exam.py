from tkinter import *
from tkinter import ttk
from database_connection import DBHelper
import progress_main

class exam():
    def doSomething(self, event):
        self.window.attributes("-fullscreen", False)

    def fullscreen(self, event):
        self.window.attributes("-fullscreen", True)

    def submit(self):
        answer = self.db_con.answer
        ques_num = 1
        for ans in answer:
            self.db_con.attempt(self.student_id, self.exam_id, ques_num, ans)
            ques_num += 1

        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.destroy()
        progress_main.progress_main(Tk(), self.student_id)

    def __init__(self,root, exam_id, student_id):
        self.window = root
        self.exam_id = exam_id
        self.student_id = student_id

        self.db_con = DBHelper()
        title = self.db_con.exam_name(self.exam_id)
        self.window.title(title)
        self.window.config(bg="#4c2853")
        self.window.bind("<Escape>",self.doSomething)
        self.window.bind("<f>",self.fullscreen)
        self.window.attributes("-fullscreen", True)

        Title = Label(self.window, text=title.upper(), font=('Varela Round', 25), width=50, height=1,bg="#4c2853", fg='white', anchor=W)
        Title.place(x=0,y=0)

        style = ttk.Style(self.window)
        style.theme_create('abc', settings={
            "TNotebook": {
                "configure": {
                    "background": '#321b37',
                    "tabmargins": [2, 5, 2, 0],
                    "tabposition": 'wn',
                    "borderwidth": 0
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "background": '#321b37',
                    "foreground": 'white',
                    "padding": [5,0],
                    "width": 8
                },
                "map": {
                    "background": [("selected",'#4c2853')],
                    "expand": [("selected",[1,1,1,1])]
                }
            }
        })

        style.theme_use('abc')


        notebook = self.db_con.create_ques_note(self.window, self.exam_id)
        notebook.config(width=1852, height=960)
        notebook.place(x=0,y=50)

        submit_button = Button(self.window, text="SUBMIT", font=('Varela Round', 15), width=159, height=2,bg="#4c2853", fg='white', command=self.submit)
        submit_button.place(x=1,y=1010)

        self.window.mainloop()

if __name__ == "__main__":
    root = Tk()
    exam(root, 1, 1)