from tkinter import *
from tkinter.ttk import *
import time

import main



class progress_main():
    def __init__(self,root, student_id):
        def doSomething(event):
            window.attributes("-fullscreen", False)

        def fullscreen(event):
            window.attributes("-fullscreen", True)

        def start_main(student_id):
            GB = 50
            download = 0
            speed = 1
            while (download < GB):
                window.title('STUDENT PORTAL')
                window.config(bg="#4c2853")
                window.bind("<Escape>", doSomething)
                window.bind("<f>", fullscreen)
                window.attributes("-fullscreen", True)

                time.sleep(0.05)
                bar['value'] += (speed / GB) * 100
                download += speed
                percent.set(str(int((download / GB) * 100)) + "%")
                if download < 25:
                    text.set("please wait")
                else:
                    text.set("SUBMITTING")
                window.update_idletasks()

            for widget in window.winfo_children():
                widget.destroy()
            window.destroy()
            main.main(Tk(), student_id)

        window = root

        window.title('STUDENT PORTAL')
        window.config(bg="#4c2853")
        window.bind("<Escape>", doSomething)
        window.bind("<f>", fullscreen)
        window.attributes("-fullscreen", True)

        percent = StringVar()
        text = StringVar()

        bar = Progressbar(window, orient=HORIZONTAL, length=1200)
        bar.pack()

        percen_label = Label(window, textvariable=percent)
        percen_label.pack()

        task_label = Label(window, textvariable=text)
        task_label.pack()


        start_main(student_id)

        window.mainloop()



if __name__ == "__main__":
    root = Tk()
    pro = progress_main(root, 1)
