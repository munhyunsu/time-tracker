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
        super().__init__(master)
        self.path = path
        self.data = self.get_data(self.path)
        self.master = master
        self.component = {}
        self.frame = self.create_frame(master, self.component)
        self.frame.pack(expand=1, fill='both')

    def create_frame(self, master, component):
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
        value_stime = tk.Label(master=frame, text='2020-01-01\n00:00:00')
        value_stime.grid(row=0, column=1, columnspan=2, sticky=tk.NSEW)
        # button: Start time reset
        button_stime = tk.Button(master=frame, text='Reset')
        button_stime.grid(row=0, column=3, sticky=tk.NSEW)
        # label: Category
        label_category = tk.Label(master=frame, text='Category')
        label_category.grid(row=1, column=0, sticky=tk.NSEW)
        # textbox: Category
        text_category = tk.Entry(master=frame)
        text_category.grid(row=1, column=1, columnspan=3, sticky=tk.EW)
        component['text_category'] = text_category
        # label: Task
        label_task = tk.Label(master=frame, text='Task')
        label_task.grid(row=2, column=0, sticky=tk.NSEW)
        # textbox: Category
        text_task = tk.Entry(master=frame)
        text_task.grid(row=2, column=1, columnspan=3, sticky=tk.EW)
        component['text_task'] = text_task
        # button: Record
        button_record = tk.Button(master=frame, text='Record')
        button_record.grid(row=3, column=0, columnspan=4, sticky=tk.NSEW)

        return frame

    def get_category(self):
        value = self.component['text_category'].get()
        if DEBUG:
            print(f'{value}')

    def text_task(self):
        value = self.component['text_task'].get()
        if DEBUG:
            print(f'{value}')

    def get_data(self, path):
        if os.path.exists(path):
            data = pd.read_pickle(path)
        else:
            data = pd.DataFrame()
        return data

    def set_data(self, path, data):
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
    app = Application(FLAGS.data, master=root)
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
