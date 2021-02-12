import os
import tkinter as tk
import time

import numpy as np
import pandas as pd

DEBUG = False
FLAGS = _ = None


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
        self.text_category = None
        self.text_task = None
        self.button_record = None
        # create GUI
        self.data = get_data(self.path)
        self.create_frame(self.master)
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
        label_stime.grid(row=0, column=0, sticky=tk.NSEW)
        # label: Start time value
        self.value_stime = tk.Label(master=frame, text='2020-01-01\n00:00:00')
        self.value_stime.grid(row=0, column=1, columnspan=2, sticky=tk.NSEW)
        # button: Start time reset
        button_stime = tk.Button(master=frame, text='Reset')
        button_stime.grid(row=0, column=3, sticky=tk.NSEW)
        # label: Category
        label_category = tk.Label(master=frame, text='Category')
        label_category.grid(row=1, column=0, sticky=tk.NSEW)
        # textbox: Category
        self.text_category = tk.Entry(master=frame)
        self.text_category.grid(row=1, column=1, columnspan=3, sticky=tk.EW)
        # label: Task
        label_task = tk.Label(master=frame, text='Task')
        label_task.grid(row=2, column=0, sticky=tk.NSEW)
        # textbox: Category
        self.text_task = tk.Entry(master=frame)
        self.text_task.grid(row=2, column=1, columnspan=3, sticky=tk.EW)
        # button: Record
        self.button_record = tk.Button(master=frame, text='Record')
        self.button_record.grid(row=3, column=0, columnspan=4, sticky=tk.NSEW)
        # pack
        frame.pack(expand=1, fill='both')

    def get_info(self):
        now = time.time()
        category = self.text_category.get()
        task = self.text_task.get()
        if DEBUG:
            print(f'{now} {category} {task}')
        return now, category, task

    def is_tasking(self):
        return len(self.data) != 0 and pd.isna(self.data.loc[self.data.index[-1]]['To'])

    def tic_tic(self):
        if DEBUG:
            print(f'is_tasking: {self.is_tasking()}')
            print(f'{self.data}')
        if self.is_tasking():
            self.value_stime.config(text=self.data.loc[self.data.index[-1]]['From'])
            self.button_record.config(text='To', command=self.event_record_to)
        else:
            self.value_stime.config(text='Press From Button')
            self.button_record.config(text='From', command=self.event_record_from)
        

    def event_record_from(self):
        now = time.time()
        category = self.text_category.get()
        task = self.text_task.get()
        if DEBUG:
            print(f'FROM {now} {category} {task}')
        self.data = self.data.append({'From': now, 'Category': category, 'Task': task}, 
                                     ignore_index=True)
        self.tic_tic()

    def event_record_to(self):
        now = time.time()
        if DEBUG:
            print(f'TO {now}')
        self.data.loc[self.data.index[-1], 'To'] = now
        self.tic_tic()


def get_data(path):
    if os.path.exists(path):
        data = pd.read_pickle(path)
    else:
        data = pd.DataFrame(columns=['From', 'To', 'Category', 'Task'])
    return data

def set_data(path, data):
    data.to_pickle(path)


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
