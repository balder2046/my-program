#!/usr/bin/python
# coding = utf-8
from tkinter import *
import re
import os
import mmsitedao
import mmsite
import task
import picturemanager
from PIL import Image
from PIL import ImageTk

COMMAND_LABEL_STRING = '下载地址'
COMMAND_BUTTON_STRING = '下载'
UPDATE_BUTTON_STRING = '更新最新目录'
OUTPUT_LABEL_STRING = '下载输出:'
TASK_LABEL_STRING = '任务输出:'


class OutputLogWidget(Frame):
    def __init__(self, master=None, cnf={}, **kwargs):
        cnf['relief'] = 'sunken'
        cnf['bd'] = 2
        if kwargs is not None:
            for key in kwargs:
                cnf[key] = kwargs[key]
        Frame.__init__(self, master, cnf)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.textbox = Text(self, padx=5, pady=5, wrap='none')
        self.textbox.grid(row=0, column=0, sticky=N + S + E + W)
        xscrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.textbox.xview)
        xscrollbar.grid(row=1, column=0, sticky=E + W)
        yscrollbar = Scrollbar(self, orient=VERTICAL, command=self.textbox.yview)
        yscrollbar.grid(row=0, column=1, sticky=N + S)
        xscrollbar.config(command=self.textbox.xview)
        yscrollbar.config(command=self.textbox.yview)

        self.textbox.config(xscrollcommand=xscrollbar.set)
        self.textbox.config(yscrollcommand=yscrollbar.set)

    def output_debug(self, content):
        pass

    def output_info(self, content):
        self.textbox.insert(END, content)
        self.textbox.insert(END, '\n')
        pass

    def output_warning(self, content):
        pass

    def output_error(self, content):
        pass


DATABASE_THREAD_NAME = 'database'


class MainApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.picturemanager = picturemanager.PictureManager()
        self.inittaskmanager()

        # bind for the FocusIn message ,get the clipeboard
        self.bind("<FocusIn>", self.app_got_focus)

        self.minsize(400, 300)
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

    def inittaskmanager(self):
        self.taskmanager = task.TaskManager(3)
        self.taskmanager.create_async_queue(DATABASE_THREAD_NAME)
        self.taskmanager.add_name_task(DATABASE_THREAD_NAME, self.initdatabase)
        self.after(500, self.__update_main_tasks)

    def __update_main_tasks(self):
        self.taskmanager.run_main_tasks(0)
        self.after(500, self.__update_main_tasks)

    def initdatabase(self):
        database = mmsitedao.PictureDatabase('album.db')
        self.database = database
        self.albumdao = mmsitedao.AlbumSummeryDao(database)
        self.tagdao = mmsitedao.AlbumTagsDao(database)
        self.picturedao = mmsitedao.AlbumPicturesDao(database)
        albums = self.albumdao.all_picture_details()
        self.picturemanager.reload(albums)
        self.text.output_info("读取 %d 个图集" % len(albums))

    def initmenu(self):
        pass

    def log(self, content):
        self.taskmanager.add_main_task(lambda: self.text.output_info(content))

    def initcontrols(self):
        # add a command entry
        # add a run command
        # add the output method
        btnUpdate = Button(self, text=UPDATE_BUTTON_STRING, command=self.updatesite)
        btnUpdate.pack(side=TOP)
        frame_command = Frame(self)
        Label(frame_command, text=COMMAND_LABEL_STRING).pack(side='left', fill=NONE)
        downloadentry = Entry(frame_command)
        downloadentry.pack(side='left', expand=YES, fill=BOTH, padx=20)
        self.downloadentry = downloadentry
        btnRun = Button(frame_command, text=COMMAND_BUTTON_STRING, command=self.on_download)
        btnRun.pack(expand=NO, fill=NONE, side="right")
        frame_command.pack(side='top', fill=X)
        Label(self, text=TASK_LABEL_STRING).pack(side='top', fill=NONE, anchor='nw', pady=10)
        self.listvar = StringVar()
        listbox = Listbox(self, listvariable=self.listvar)
        listbox.pack(side='top', fill=BOTH, expand=YES, padx=5, pady=5)
        listbox.items = []
        listbox.filepaths = []

        def openfolder(event):
            cur = self.listbox.curselection()
            paths = self.listbox.filepaths
            os.system("open '%s'" % paths[cur[0]])

        listbox.bind('<Double-Button-1>', openfolder)
        self.listbox = listbox
        Label(self, text=OUTPUT_LABEL_STRING).pack(side='top', fill=NONE, anchor='nw', pady=10)
        self.text = OutputLogWidget(self)
        self.text.pack(side='top', fill=BOTH, expand=YES, padx=5, pady=5)

        pass

    def register_command(self, name, func, description):
        pass

    def app_got_focus(self, event):
        # self.config(background="red")
        pass

    def app_lost_focus(self, event):
        # self.config(background="grey")
        pass

    test_count = 0

    def on_run_command(self):
        MainApp.test_count += 1
        # self.text.insert(END,"you clicked run " + "%d " % MainApp.test_count)
        self.text.output_info("you clicked run " + "%d \n" % MainApp.test_count)
        pass

    def setlistboxitem(self, index, text):
        items = self.listvar.get()
        self.listbox.items[index] = text
        self.listvar.set(tuple(self.listbox.items))

    def show_dialog(self):
        top = Toplevel(self)
        top.geometry('1280x900+100+100')
        image = Image.open("06.jpg")
        print(image.size)
        newsize = (1280, int(1280 * image.size[1] / float(image.size[0])))
        image = image.resize(newsize)
        imagetk = ImageTk.PhotoImage(image)
        # self.picturelabel = Label(top,image=imagetk).pack(side='top',expand= YES,fill=BOTH)
        canvas = Canvas(top)

        canvas.create_image((0, 0), anchor=NW, image=imagetk)
        print(canvas.bbox("all"))
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.pack(side=LEFT, expand=YES, fill=BOTH)
        S1 = Scrollbar(canvas, orient='vertical', command=canvas.yview)
        canvas['yscrollcommand'] = S1.set
        S1.pack(side=RIGHT, fill=Y)
        canvas.focus_get()

        canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-0.9 * event.delta), 'units'))
        top.transient(self)
        top.grab_set()

        self.wait_window(top)
        print("windows close")

    def on_download(self):
        # self.show_dialog()
        text = self.downloadentry.get()
        if len(text) == 0: return
        text = text.replace("https://www.aitaotu.com", "")
        album = self.picturemanager.get_by_url(text)

        def info(x):
            return "%s (%d/%d)" % (album.title, x, album.piccount)

        if album is not None:
            text = info(0)
            index = self.listbox.size()
            self.listbox.insert(END, text)

            self.listbox.items.append(text)
            self.listbox.filepaths.append(album.get_filepath())

            self.taskmanager.add_async_task(lambda: album.download('',
                                                                   lambda x: self.setlistboxitem(index, info(x)),
                                                                   self.log))

    def run_command(self, cmd):

        pass

    def updatesite(self):
        self.taskmanager.add_name_task(DATABASE_THREAD_NAME,
                                       lambda: mmsite.updatesite(self.albumdao, self.tagdao, self.picturedao,
                                                                 self.text.output_info))
        pass


app = MainApp()
app.geometry('800x600+100+100')
app.mainloop()
