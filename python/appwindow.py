from tkinter import *

COMMAND_LABEL_STRING = '命令'
COMMAND_BUTTON_STRING = '运行'
OUTPUT_LABEL_STRING = '命令输出:'

# This is the list of all default command in the "Text" tag that modify the text
commandsToRemove = (
"<Control-Key-h>",
"<Meta-Key-Delete>",
"<Meta-Key-BackSpace>",
"<Meta-Key-d>",
"<Meta-Key-b>",
"<<Redo>>",
"<<Undo>>",
"<Control-Key-t>",
"<Control-Key-o>",
"<Control-Key-k>",
"<Control-Key-d>",
"<Key>",
"<Key-Insert>",
"<<PasteSelection>>",
"<<Clear>>",
"<<Paste>>",
"<<Cut>>",
"<Key-BackSpace>",
"<Key-Delete>",
"<Key-Return>",
"<Control-Key-i>",
"<Key-Tab>",
"<Shift-Key-Tab>"
)



class ROText(Text):
    tagInit = False

    def init_tag(self):
        """
        Just go through all binding for the Text widget.
        If the command is allowed, recopy it in the ROText binding table.
        """
        for key in self.bind_class("Text"):
            if key not in commandsToRemove:
                command = self.bind_class("Text", key)
                self.bind_class("ROText", key, command)
        ROText.tagInit = True


    def __init__(self, *args, **kwords):
        Text.__init__(self, *args, **kwords)
        if not ROText.tagInit:
            self.init_tag()

        # Create a new binding table list, replace the default Text binding table by the ROText one
        bindTags = tuple(tag if tag!="Text" else "ROText" for tag in self.bindtags())
        self.bindtags(bindTags)

class OutputLogWidget(Frame):

    def __init__(self, master = None,cnf={},**kwargs):
        cnf['relief'] = 'sunken'
        cnf['bd'] = 2
        if kwargs is not None:
            for key in kwargs:
                cnf[key] = kwargs[key]
        Frame.__init__(self,master,cnf)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.textbox = Text(self, padx=5, pady=5, wrap='none')
        self.textbox.grid(row=0, column=0, sticky=N + S + E + W)
        xscrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.textbox.xview)
        xscrollbar.grid(row=1, column=0, sticky=E + W)
        yscrollbar = Scrollbar(self, orient=VERTICAL, command=self.textbox.yview)
        yscrollbar.grid(row=0, column=1, sticky=N + S)
        xscrollbar.config(command = self.textbox.xview)
        yscrollbar.config(command = self.textbox.yview)


        self.textbox.config(xscrollcommand = xscrollbar.set)
        self.textbox.config(yscrollcommand = yscrollbar.set)



    def output_debug(self,content):
        pass
    def output_info(self,content):
        self.textbox.insert(END,content)
        pass
    def output_warning(self,content):
        pass
    def output_error(self,content):
        pass
class MainApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.minsize(400,300)
        self.initcontrols()
        # self.bind("<FocusIn>", self.app_got_focus)
        # self.bind("<FocusOut>", self.app_lost_focus)
        # btn = Button(self,text = "click")
        # btn.pack()
        # def onclick(event):
        #     print(event)
        #     s = Label(self,text = self.entry.get(),background="green")
        #     s.pack()
        #     self.entry['show'] = ''
        #     self.btn['text'] = "you already clicked"
        #     self.btn.unbind("<Button-1>")
        #
        # btn.bind("<Button-1>",onclick)
        # self.bind("<KeyPress-Prior>",onclick)
        # self.btn = btn
        # self.entry = Entry(self)
        # self.entry['show'] = '*'
        # self.entry.pack()
        # self.btn['width'] = self.entry['width']
        # self.geometry('200x200+200+200')
        # frame = self
        #
        # frame.columnconfigure(0, weight=1)
        # frame.rowconfigure(0,weight=0)
        # frame.rowconfigure(1, weight=1)
        # label = Label(frame,text='A',bg='red').grid(row=0,column=0,sticky='nsew')
        # Label(frame, text='B', bg='green').grid(row=1, column=0, sticky='nsew')


       # Label(frame,text='D',bg='yellow').pack(side=LEFT,expand=NO,fill = Y)




    def initmenu(self):
        pass
    def initcontrols(self):
        # add a command entry
        # add a run command
        # add the output method

        frame_command = Frame(self)
        Label(frame_command,text=COMMAND_LABEL_STRING).pack(side='left',fill=NONE)
        commandEntry = Entry(frame_command)
        commandEntry.pack(side='left',expand=YES,fill = BOTH,padx = 20)
        btnRun = Button(frame_command, text = COMMAND_BUTTON_STRING,command=self.on_run_command)
        btnRun.pack(expand = NO,fill = NONE,side="right")
        frame_command.pack(side='top',fill=X)
        Label(self,text= OUTPUT_LABEL_STRING).pack(side='top',fill=NONE,anchor='nw',pady = 10)
        self.text = OutputLogWidget(self)
        self.text.pack(side='top',fill=BOTH,expand=NO,padx = 5,pady = 5)



        pass
    def register_command(self,name,func,description):
        pass

    def app_got_focus(self, event):
        # self.config(background="red")
        print("app_got_focus")

    def app_lost_focus(self, event):
        # self.config(background="grey")
        print("app_lost_focus")
    test_count = 0
    def on_run_command(self):
        MainApp.test_count += 1
       # self.text.insert(END,"you clicked run " + "%d " % MainApp.test_count)
        self.text.output_info("you clicked run " + "%d \n" % MainApp.test_count)
        pass
    def run_command(self,cmd):

        pass


app = MainApp()
app.geometry('800x600+100+100')
app.mainloop()