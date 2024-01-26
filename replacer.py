from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os
import json

DEFAULT_INSTALL_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\Fear & Hunger\www\data"

directory = DEFAULT_INSTALL_DIR

def set_directory():
    global directory
    directory = fd.askdirectory(
        title="Choose your fear and hunger install", 
        initialdir=directory)
    directory_label.config(text=directory)

def loop_through_and_replace():
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            find_and_replace_text(filepath)

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

directory_label = ttk.Label(mainframe, text=directory)
set_directory_button = ttk.Button(mainframe, text="Set Directory", 
                           command=set_directory)
execute_button = ttk.Button(mainframe, text="Replace Text", 
                       command=loop_through_and_replace)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
