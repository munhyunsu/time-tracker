import os
import sys
import time


def main():
    print('\x1B[1m\x1B[33mTime Tracker Installer\x1B[0m')
    
    print('\x1B[47m\x1B[32mCheck the dependency\x1B[0m')
    try:
        import numpy as np
        import pandas as pd
        import tkinter as tk
        from tkinter import ttk
    except ModuleNotFoundError:
        print('\x1B[31mCheck and install dependency list\x1B[0m')
        print('\x1B[31mpip3 install --upgrade -r requirements.txt\x1B[0m')
        print('\x1B[31m(If you not use python3 with tkinter, then apt install python3-tk)\x1B[0m')
        return
    print(f'\x1B[32mnumpy version: {np.__version__}\x1B[0m')
    print(f'\x1B[32mpandas version: {pd.__version__}\x1B[0m')
    print(f'\x1B[32mtkinter version: {tk.TkVersion}\x1B[0m')
    print('\x1B[47m\x1B[32mCheck the dependency done\x1B[0m')

    print('\x1B[47m\x1B[32mCheck Python3 interpreter path\x1B[0m')
    python3_path = sys.executable
    root_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(root_dir, 'main.py')
    print(f'\x1B[32mPython3 path: {python3_path}\x1B[0m')
    print(f'\x1B[32mmain.py path: {main_path}\x1B[0m')
    print('\x1B[47m\x1B[32mCheck Python3 interpreter path done\x1B[0m')

    print('\x1B[47m\x1B[32Download Nanum Gothic font on Google fonts\x1B[0m')
    ## Need to download URL: https://fonts.google.com/download?family=Nanum%20Gothic

    if sys.platform == 'linux':
        print('\x1B[47m\x1B[32mCreate timetracker.desktop\x1B[0m')
        desktop = (f'[Desktop Entry]\n'
                   f'Name=Time Tracker\n'
                   f'Comment=Time Tracker\n'
                   f'Exec=bash -c "{python3_path} {main_path}"\n'
                   f'Terminal=false\n'
                   f'Type=Application\n'
                   f'Categories=Office;\n')
        print(f'\x1B[32m{desktop}\x1B[0m')
        desktop_path = os.path.join(root_dir, 'timetracker.desktop')
        with open(desktop_path, 'w') as f:
            f.write(desktop)
        print(f'\x1B[47m\x1B[32mln -s {desktop_path} ~/.local/share/applications/\x1B[0m')
        print(f'\x1B[47m\x1B[32mOr move timetracker.desktop to ~/.local/share/applications/\x1B[0m')
    elif sys.platform == 'cygwin':
        print('\x1B[32mNeed to execution bash on Windows\x1B[0m')


    print('\x1B[1m\x1B[33mTime Tracker Installation Complete\x1B[0m')

if __name__ == '__main__':
    main()

