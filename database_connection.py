
import mysql.connector as connector
from tkinter import *
from tkinter import ttk
import time
import datetime

class DBHelper:
    def __init__(self):
        self.con = connector.connect(host='localhost',
                                     port='3306',
                                     user='mysqluser',
                                     password='password',
                                     database='student_portal')

        self.answer = []
    # Exam num fetch
    def exam_num(self):
        exam_num = 0
        try:
            for index in range(1, 11):
                query = "select * from exam where exam_id = {}".format(index)
                cur = self.con.cursor()
                cur.execute(query)
                if cur.fetchall() != []:
                    exam_num += 1

            return exam_num

        except Exception as e:
            print(e)

    def lec_num(self):
        lec_num = 0
        try:
            for index in range(1, 11):
                query = "select * from lecture where lecture_id = {}".format(index)
                cur = self.con.cursor()
                cur.execute(query)
                if cur.fetchall() != []:
                    lec_num += 1

            return lec_num

        except Exception as e:
            print(e)

    # fetch name of the exam
    def exam_name(self, exam_id):
        try:
            query = "select * from Exam where exam_id = {}".format(exam_id)
            cur = self.con.cursor()
            cur.execute(query)
            exam_name = cur.fetchall()[0][1]
            return exam_name

        except Exception as e:
            print(e)

    def lec_name(self, lec_id):
        try:
            query = "select * from lecture where lecture_id = {}".format(lec_id)
            cur = self.con.cursor()
            cur.execute(query)
            lec_name = cur.fetchall()[0][1]
            return lec_name

        except Exception as e:
            print(e)
    # Question num
    def question_num(self, exam_id):
        question_num = 0
        try:
            query = "select * from Exam where exam_id = {}".format(exam_id)
            cur = self.con.cursor()
            cur.execute(query)
            for rows in cur:
                question_num += 1

            return question_num

        except Exception as e:
            print(e)



    # fetch student info
    def fetch_student_info(self, student_id):
        try:
            query = "select * from student where student_id = {}".format(student_id)
            cur = self.con.cursor()
            cur.execute(query)
            student = cur.fetchall()
            return student

        except Exception as e:
            print(e)

    def create_student_tab(self, student_id, notebook):
        student = self.fetch_student_info(student_id)
        frame = Frame(notebook, bg="white", width=1250, height=1000, padx=50, pady=50)
        title = Label(frame, text= "USER INFO",font=('Varela Round', 25),anchor=W, bg="white")
        title.grid(sticky=W,row=0, column=0, columnspan=2)

        fullname = Label(frame, text = "NAME:",font=('Varela Round', 20),anchor=W, bg="white")
        fullname.grid(sticky=W,row=1,column=0)
        fullname_2 = Label(frame, text= student[0][1] + " " + student[0][2],font=('Varela Round', 20),anchor=W, bg="white")
        fullname_2.grid(sticky=W,row=1, column=1)

        username = Label(frame, text="USERNAME:", font=('Varela Round', 20),anchor=W, bg="white")
        username.grid(sticky=W,row=2, column=0)
        username_2 = Label(frame, text=student[0][3], font=('Varela Round', 20),anchor=W, bg="white")
        username_2.grid(sticky=W,row=2, column=1)

        email = Label(frame, text="EMAIL:", font=('Varela Round', 20),anchor=W, bg="white")
        email.grid(sticky=W,row=3, column=0)
        email_2 = Label(frame, text=student[0][5], font=('Varela Round', 20),anchor=W, bg="white")
        email_2.grid(sticky=W,row=3, column=1)

        phone = Label(frame, text="PHONE NUMBER:", font=('Varela Round', 20),anchor=W, bg="white")
        phone.grid(sticky=W,row=4, column=0)
        phone_2 = Label(frame, text=student[0][6], font=('Varela Round', 20),anchor=W, bg="white")
        phone_2.grid(sticky=W,row=4, column=1)

        return frame



    # create quetion
    def create_ques_note(self, tk, exam_id):
        num_of_ques = self.question_num(exam_id)
        style = ttk.Style(tk)
        style.theme_create('note', settings={
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
                    "padding": [5, 5],
                    "width": 8
                },
                "map": {
                    "background": [("selected", '#4c2853')],
                    "expand": [("selected", [1, 1, 1, 1])]
                }
            }
        })

        style.theme_use('note')

        note = ttk.Notebook(tk, style='TNotebook')
        for index in range(num_of_ques):
            self.answer.append(' ')
            frame = self.create_ques_frame(note, exam_id, index)
            frame.config(width=1852, height=960, bg='white')
        return note

    def create_ques_frame(self, notebook, exam_id, ques_num):
        def select():
            self.answer.pop(ques_num)
            self.answer.insert(ques_num, ans.get())

        frame = Frame(notebook)

        query = "select * from Exam where exam_id = {}".format(exam_id)
        cur = self.con.cursor()
        cur.execute(query)
        row = cur.fetchall()[ques_num]
        question = row[5]
        op_1 = row[6]
        op_2 = row[7]
        op_3 = row[8]
        op_4 = row[9]

        ans = StringVar()
        question_label = Label(frame, text=question, font=('Varela Round', 25), height=1)
        question_label.pack()
        op_1_radio = Radiobutton(frame, text=op_1, variable=ans, value='A', padx=5, font=('Varela Round', 25),
                                     bg='white', fg='black', activebackground='#4c2853', command=select)
        op_1_radio.pack(anchor=W)

        op_2_radio = Radiobutton(frame, text=op_2, variable=ans, value='B', padx=5, font=('Varela Round', 25),
                                     bg='white', fg='black', activebackground='#4c2853', command=select)
        op_2_radio.pack(anchor=W)

        op_3_radio = Radiobutton(frame, text=op_3, variable=ans, value='C', padx=5, font=('Varela Round', 25),
                                     bg='white', fg='black', activebackground='#4c2853', command=select)
        op_3_radio.pack(anchor=W)

        op_4_radio = Radiobutton(frame, text=op_4, variable=ans, value='D', padx=5, font=('Varela Round', 25),
                                     bg='white', fg='black', activebackground='#4c2853', command=select)
        op_4_radio.pack(anchor=W)
        notebook.add(frame,text="Q"+str(ques_num + 1))
        return frame


    def mark_lec(self, student_id, lecture_id):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "insert into lec_attendance values({}, {}, '{}')".format(student_id,lecture_id,now)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()

    def mark_exam(self, student_id, exam_id):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "insert into exam_attendance values({}, {}, '{}')".format(student_id,exam_id,now)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()

    def attempt(self, student_id, exam_id, ques_id, ans):
        query= "insert into exam_attempt(student_id,exam_id,question_num,ans) values({},{},{},'{}');".format(student_id,exam_id,ques_id,ans)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()

    def check_attempt(self, student_id, exam_id):
        query = "select * from exam_attendance where student_id = {} and exam_id = {}".format(student_id,exam_id)
        cur = self.con.cursor()
        cur.execute(query)
        if cur.fetchall() != []:
            return True

    def check_lec(self, lec_id):
        query = "select * from lecture where lecture_id = {}".format(lec_id)
        cur = self.con.cursor()
        cur.execute(query)
        lec_time = cur.fetchall()
        start_time = lec_time[0][3]
        end_time = lec_time[0][4]
        now = datetime.datetime.now()
        if now < start_time:
            return (1,start_time)
        elif now > end_time:
            return (2,end_time)
        else:
            return (3,start_time)

    def lec_link(self, lec_id):
        query = "select * from lecture where lecture_id = {}".format(lec_id)
        cur = self.con.cursor()
        cur.execute(query)
        lec_link = cur.fetchall()
        return lec_link[0][2]

    def check_marks(self, student_id, exam_id):
        query = "select * from exam where exam_id = {}".format(exam_id)
        cur = self.con.cursor()
        cur.execute(query)
        correct_answer = 0
        exam_ans = cur.fetchall()
        query = "select * from exam_attempt where student_id = {} and exam_id = {}".format(student_id,exam_id)
        cur = self.con.cursor()
        cur.execute(query)
        student_ans = cur.fetchall()


        counter = 0
        for ans in exam_ans:
            if student_ans[counter][4] == ans[10]:
                correct_answer += 1

            counter += 1

        return correct_answer

    def generate_chat(self, sender, receiver):
        sender1 = sender
        sender2 = sender
        receiver1 = receiver
        receiver2 = receiver
        query = "select * from chat where sender = {} and receiver = {} or sender = {} and receiver = {};".format(sender1, receiver1,receiver2,sender2)
        cur = self.con.cursor()
        cur.execute(query)
        chat = cur.fetchall()
        return chat

    def send_msg(self, sender, receiver, chat_msg):
        query = "insert into chat(sender, receiver,chat_msg) values({},{},'{}');".format(sender, receiver, chat_msg)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()






