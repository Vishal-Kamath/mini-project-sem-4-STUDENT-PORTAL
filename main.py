
from tkinter import *
from tkinter import ttk
import textwrap
import detectface
from database_connection import DBHelper
import exam
from functools import partial
import progress_login
import webbrowser

class main():

    def doSomething(self, event):
        self.window.attributes("-fullscreen", False)

    def fullscreen(self, event):
        self.window.attributes("-fullscreen", True)

    def open_exam(self, exam_id):
        if detectface.mark_attendance_exam(self.student_id,exam_id):
            for widget in self.window.winfo_children():
                widget.destroy()
            self.window.destroy()
            exam.exam(Tk(), exam_id, self.student_id)

    def exam_frame(self, notebook):
        frame = Frame(notebook, bg="white", width=1250, height=1000, padx=10,pady=10)
        exam_num = self.db_con.exam_num()
        for index in range(exam_num):
            exam_tab = Frame(frame, bg='#4c2853', width=1175, height=200)
            exam_tab.place(x= 10, y = 10 + 250 * index)
            exam_name = Label(exam_tab, text=self.db_con.exam_name(index+1),font=('Varela Round', 20), bg='#4c2853', fg= 'white')
            exam_name.place(x=10,y=10)

            check = self.db_con.check_attempt(self.student_id, index + 1)
            if not check:
                ques_num = Label(exam_tab, text= str(self.db_con.question_num(index + 1)) + " questions",font=('Varela Round', 20), bg='#4c2853', fg= 'white')
                ques_num.place(x=10, y= 60)

                attempt_button = Button(exam_tab, text="ATTEMPT", font=('Varela Round', 15), fg='#4c2853', command= partial(self.open_exam, index + 1))
                attempt_button.place(x = 1025, y = 110)

            else:
                marks = Label(exam_tab, text="Marks: " + str(self.db_con.check_marks(self.student_id, index + 1)) +"/" + str(self.db_con.question_num(index + 1)),font=('Varela Round', 20), bg='#4c2853', fg='white')
                marks.place(x=10, y=60)

        return frame

    def open_lec(self, lec_id):
        if detectface.mark_attendance_lec(self.student_id,lec_id):
            link = self.db_con.lec_link(lec_id)
            webbrowser.open(link)

    def lec_frame(self, notebook):
        frame = Frame(notebook, bg="white", width=1250, height=1000, padx=10,pady=10)
        canvas_f1 = Canvas(frame, scrollregion=(0, 0, 450, 900))

        vertibar_f1 = Scrollbar(frame, orient=VERTICAL)
        vertibar_f1.pack(side=RIGHT, fill=Y)
        vertibar_f1.config(command=canvas_f1.yview)
        lec_num = self.db_con.lec_num()
        for index in range(lec_num):
            lec_tab = Frame(frame, bg='#4c2853', width=1175, height=200)
            lec_tab.place(x= 10, y = 10 + 250 * index)
            lec_name = Label(lec_tab, text=self.db_con.lec_name(index+1),font=('Varela Round', 20), bg='#4c2853', fg= 'white')
            lec_name.place(x=10,y=10)

            check = self.db_con.check_lec(index + 1)
            if check[0] == 1:
                lec_status = Label(lec_tab, text="Lecture will start at " + str(check[1]),font=('Varela Round', 20), bg='#4c2853', fg= 'white')
                lec_status.place(x=10, y= 60)

            elif check[0] == 2:
                lec_status = Label(lec_tab, text="Lecture ended at " + str(check[1]),font=('Varela Round', 20), bg='#4c2853', fg='white')
                lec_status.place(x=10, y=60)

            elif check[0] == 3:
                attend_button = Button(lec_tab, text="ATTEND", font=('Varela Round', 15), fg='#4c2853',command=partial(self.open_lec, index + 1))
                attend_button.place(x=1025, y=110)

        canvas_f1.config(width=450, height=900)
        canvas_f1.config(yscrollcommand=vertibar_f1.set)
        canvas_f1.pack(expand=True, side=LEFT, fill=BOTH)
        return frame

    def logout(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.destroy()
        progress_login.progress_login_class(Tk())



    def connect(self):
        self.receiver = self.chat_entry.get()
        self.generate_chat()
        self.chat_entry.delete(0, END)


    def send(self):
        chat = self.chat_entry.get()
        wrapper = textwrap.TextWrapper(width=45)

        word_list = wrapper.wrap(text=chat)
        for element in word_list:
            self.db_con.send_msg(self.student_id, self.receiver, element)
        self.generate_chat()
        self.chat_entry.delete(0, END)

    def generate_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()


        canvas = Canvas(self.chat_frame,scrollregion=(0,0,450,900))

        vertibar = Scrollbar(self.chat_frame, orient=VERTICAL)
        vertibar.pack(side=RIGHT, fill=Y)
        vertibar.config(command=canvas.yview)
        student_id = self.student_id
        receiver = self.receiver
        chat_msg = self.db_con.generate_chat(student_id,receiver )
        for msg in chat_msg:

            if msg[1] == int(receiver):
                chat_label = Label(canvas, text =msg[3], font=('Varela Round', 10), width=45, bg='white', fg="black", anchor=W)
                chat_label.pack()

            elif msg[1] == int(student_id):
                chat_label = Label(canvas, text =msg[3], font=('Varela Round', 10), width=45, bg='#B983C3', fg = "black", anchor=E)
                chat_label.pack()


        canvas.config(width=450, height=900)
        canvas.config(yscrollcommand=vertibar.set)
        canvas.pack(expand=True, side=LEFT, fill=BOTH)

        self.window.update_idletasks()


    def __init__(self, root, student_id):
        self.window = root
        self.receiver = 0
        self.student_id = student_id
        self.window.title('STUDENT PORTAL')
        self.window.config(bg="#4c2853")
        self.window.bind("<Escape>",self.doSomething)
        self.window.bind("<f>",self.fullscreen)
        self.window.attributes("-fullscreen", True)

        Title = Label(self.window, text="STUDENT PORTAL", font=('Varela Round', 25), width=50, height=1,bg="#4c2853", fg='white', anchor=W)
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
                    "padding": [5,5],
                    "width": 8
                },
                "map": {
                    "background": [("selected",'#4c2853')],
                    "expand": [("selected",[1,1,1,1])]
                }
            }
        })

        style.theme_use('abc')

        self.db_con = DBHelper()


        lecture_image_2 = PhotoImage(file='lecture.png')
        test_image_2 = PhotoImage(file='test.png')
        user_image_2 = PhotoImage(file='user.png')

        notebook = ttk.Notebook(self.window, style='TNotebook')
        f1 = self.lec_frame(notebook)


        f2 = self.exam_frame(notebook)
        f2.pack_propagate(0)
        f2_scrollBar = Scrollbar(f2, orient='vertical')
        f2_scrollBar.pack(side=RIGHT, fill=Y)
        f4 = self.db_con.create_student_tab(student_id, notebook)
        logout_button = Button(f4, text="LOGOUT",font=('Varela Round', 20), bg="white", command=self.logout)
        logout_button.grid(sticky=W,row=5, column=1)
        notebook.add(f1,text="LECTURE",image=lecture_image_2, compound=TOP)
        notebook.add(f2,text="  TEST",image=test_image_2, compound=TOP)
        notebook.add(f4, text="  USER", image=user_image_2, compound=TOP)
        notebook.place(x=0,y=50)

        self.chat_frame = Frame(self.window, bg="white", width=450, height=900)
        self.chat_frame.place(x=1400, y=50)
        self.chat_frame.pack_propagate(0)

        self.chat_entry = Entry(self.window,font=('Varela Round', 10), bg='white', width=45)
        self.chat_entry.place(x=1400, y=975)

        self.send_chat = Button(self.window,text="  SEND  ",font=('Varela Round', 10), command= self.send)
        self.send_chat.place(x=1800, y=975)

        self.connect_button = Button(self.window, text="connect", font=('Varela Round', 10), command=self.connect)
        self.connect_button.place(x=1800, y=1010)

        if self.receiver != 0:
            self.generate_chat()


        self.window.mainloop()


if __name__ == "__main__":
    root = Tk()
    main(root, 2)

