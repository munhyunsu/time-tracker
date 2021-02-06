import os
import tkinter as tk

DEBUG = False
FLAGS = _ = None


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Time Tracker')
        self.frame = self.create_frame(master)

    def create_frame(self, master):
        # master Layout
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        # master Frame
        frame = tk.Frame(master=master, relief=tk.RAISED, borderwidth=1)
        # label: Category
        label_category = tk.Label(master=frame, text='Category')
        label_category.grid(row=0, column=0, sticky=tk.NSEW)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        # label: Task
        label_task = tk.Label(master=frame, text='Task')
        label_task.grid(row=1, column=0, sticky=tk.NSEW)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        # textbox: Category
        text_category = tk.Entry(master=frame)
        text_category.grid(row=0, column=1, columnspan=3, sticky=tk.EW)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
#         button = tk.Button(master=frame, text='A', command=up)
#         button.grid(row=0, column=0, sticky=tk.NSEW)
#         frame.grid_rowconfigure(0, weight=1)
#         frame.grid_columnconfigure(0, weight=1)
#         button = tk.Button(master=frame, text='B', command=down)
#         button.grid(row=1, column=1, sticky=tk.NSEW)
#         frame.grid_rowconfigure(1, weight=1)
#         frame.grid_columnconfigure(1, weight=1)
        frame.pack(expand=1, fill='both')

        return frame


def up():
    print('up')


def down():
    print('down')


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    root = tk.Tk()
    root.geometry('256x256')
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug
    
    main()
