from tkinter import *

class MainApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.bind("<FocusIn>", self.app_got_focus)
        self.bind("<FocusOut>", self.app_lost_focus)


    def initcontrols(self):
        # add a command entry
        # add a run command
        # add the output method
        pass

    def app_got_focus(self, event):
        # self.config(background="red")
        print("app_got_focus")

    def app_lost_focus(self, event):
        # self.config(background="grey")
        print("app_lost_focus")



app = MainApp()

app.mainloop()