from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os
import json
import threading

DEFAULT_INSTALL_DIR = "C:/Program Files (x86)/Steam/steamapps/common/Fear & Hunger/www/data"

directory = DEFAULT_INSTALL_DIR

def set_directory():
    global directory
    global status_label
    directory = fd.askdirectory(
        title="Choose your F&H install's /www/data folder", 
        initialdir=directory)
    if directory:
        directory_label.config(text=directory)
    status_label.config(text="")

def start_loop_through_and_replace():
    global directory
    global status_label
    if not directory.endswith("/www/data"):
        status_label.config(text="This doesn't look like F&H /www/data folder...")
        return

    thread = threading.Thread(target=loop_through_and_replace)
    status_label.config(text="Processing, do not close the window...")
    thread.start()

def loop_through_and_replace():
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith(".json"):
            find_and_replace_text(filepath)
    status_label.config(text="done")

def find_and_replace_text(filepath):
    with open(filepath, 'rb') as file:
        try:
            file_content = file.read()
            for new_value, old_value in open_json():
                if old_value == "": continue
                file_content = file_content.replace(old_value.encode(), new_value.encode())
                print(f"replacing '{old_value}' with '{new_value}'")
            with open(filepath, 'wb') as output_file:
                output_file.write(file_content)
        except Exception as e:
            print(f"Error processing file '{file}': {str(e)}")

def open_json():
    with open("replacements.json", 'r') as json_file:
        data = json.load(json_file)
    for entry in data:
        yield entry["new"], entry["old"]

root = Tk()
root.title("Fear and Hunger Text Replacer")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.minsize(width=400, height=120)

directory_label = ttk.Label(mainframe, text=directory)
set_directory_button = ttk.Button(mainframe, text="Set F&H /www/data Directory", 
                           command=set_directory)
execute_button = ttk.Button(mainframe, text="Replace Text", 
                       command=start_loop_through_and_replace)
status_label = ttk.Label(mainframe, text="")

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
