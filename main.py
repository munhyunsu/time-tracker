import os
import datetime
import tkinter as tk
from tkinter import ttk
import time

import numpy as np
import pandas as pd

DEBUG = False
FLAGS = _ = None
TZ_SEOUL = datetime.timezone(datetime.timedelta(hours=9))
TZ_UTC = datetime.timezone(datetime.timedelta())

class Application(tk.Frame):
    ROWS = 4
    COLUMNS = 4
    
    def __init__(self, path, master=None):
        # Init root
        super().__init__(master)
        self.path = path
        self.master = master
        # Init GUI handler
        self.value_stime = None
        self.combo_category = None
        self.text_task = None
        self.button_record = None
        # create GUI
        self.data = get_data(self.path)
        self.create_frame(self.master)
        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        # tic
        self.tic_tic()

    def create_frame(self, master):
        # master Frame
        frame = tk.Frame(master=master, relief=tk.RAISED, borderwidth=1)
        for i in range(self.ROWS):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(self.COLUMNS):
            frame.grid_columnconfigure(i, weight=1)
        # label: Start time
        label_stime = tk.Label(master=frame, text='Start time')
        label_stime.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        # label: Start time value
        self.value_stime = tk.Label(master=frame, text='2020-01-01\n00:00:00')
        self.value_stime.grid(row=0, column=1, padx=10, pady=10, columnspan=2, sticky=tk.NSEW)
        # button: Start time reset
        button_stime = tk.Button(master=frame, text='Reset', command=self.event_reset)
        button_stime.grid(row=0, column=3, padx=10, pady=10, sticky=tk.NSEW)
        # label: Category
        label_category = tk.Label(master=frame, text='Category')
        label_category.grid(row=1, column=0, sticky=tk.NSEW)
        # combobox: Category
        self.combo_category = ttk.Combobox(master=frame)
        self.combo_category.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky=tk.EW)
        # label: Task
        label_task = tk.Label(master=frame, text='Task')
        label_task.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=10)
        # textbox: Task
        self.text_task = tk.Text(master=frame, width=1, height=1)
        self.text_task.grid(row=2, column=1, columnspan=3, sticky=tk.NSEW, padx=10, pady=10)
        # button: Record
        self.button_record = tk.Button(master=frame, text='Record')
        self.button_record.grid(row=3, column=0, columnspan=4, sticky=tk.NSEW, padx=10, pady=10)
        
        # pack
        frame.pack(expand=2, fill='both',  side=tk.LEFT)

    def quit(self):
        if DEBUG:
            print(f'QUIT')
        set_data(self.path, self.data)
        self.master.destroy()

    def is_tasking(self):
        return len(self.data) != 0 and pd.isna(self.data.loc[self.data.index[-1]]['To'])

    def tic_tic(self):
        if DEBUG:
            print(f'is_tasking: {self.is_tasking()}')
            if len(self.data) > 0:
                print(f'{self.data.loc[self.data.index[-10:]]}')
        self.combo_category.config(values=sorted(list(self.data['Category'].unique())))
        if self.is_tasking():
            self.value_stime.config(text=get_time(self.data.loc[self.data.index[-1]]['From']))
            self.combo_category.set(self.data.loc[self.data.index[-1]]['Category'])
            self.text_task.delete('1.0', 'end')
            self.text_task.insert('1.0', self.data.loc[self.data.index[-1]]['Task'])
            self.button_record.config(text='To', command=self.event_record_to)
        else:
            self.value_stime.config(text='Press From Button')
            self.combo_category.set('')
            self.text_task.delete('1.0', 'end')
            self.text_task.insert('1.0', '')
            self.button_record.config(text='From', command=self.event_record_from)

    def event_record_from(self):
        now = time.time()
        category = self.combo_category.get().strip()
        task = self.text_task.get('1.0', 'end').strip()
        if DEBUG:
            print(f'\nFROM {now} {category} {task}')
        self.data = self.data.append({'From': now, 'Category': category, 'Task': task}, 
                                     ignore_index=True)
        self.tic_tic()

    def event_record_to(self):
        now = time.time()
        category = self.combo_category.get().strip()
        task = self.text_task.get('1.0', 'end').strip()
        if DEBUG:
            print(f'\nTO {now} {category} {task}')
        if category != '' and task != '':
            self.data.loc[self.data.index[-1], 'Category'] = category
            self.data.loc[self.data.index[-1], 'Task'] = task
            self.data.loc[self.data.index[-1], 'To'] = now
            self.tic_tic()

    def event_reset(self):
        if DEBUG:
            print('\nRESET')
        if self.is_tasking():
            self.data = self.data.drop(self.data.index[-1])
        self.tic_tic()


def get_data(path):
    if os.path.exists(path):
        data = pd.read_pickle(path)
    else:
        data = pd.DataFrame(columns=['From', 'To', 'Category', 'Task'])
    return data


def set_data(path, data):
    data.to_pickle(path)


def get_time(timestamp, tz=TZ_SEOUL):
    dt = datetime.datetime.fromtimestamp(timestamp, tz=tz)
    return dt.strftime('%Y-%m-%d(%a)\n%H:%M:%S(%z)')


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    root = tk.Tk()
    root.geometry('256x256')
    root.title('Time Tracker')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = Application(path=FLAGS.data, master=root)
    app.mainloop()


if __name__ == '__main__':
    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--data', type=str, default='./data.pkl',
                        help='The path for data')

    FLAGS, _ = parser.parse_known_args()
    FLAGS.data = os.path.abspath(os.path.expanduser(FLAGS.data))
    DEBUG = FLAGS.debug
    
    main()
