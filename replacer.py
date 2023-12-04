import os
import json
import tkinter as tk
from tkinter import filedialog

def get_directory_from_user():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select a directory
    return filedialog.askdirectory(title="Select /www/data folder of Fear and Hunger")

def open_json():
    with open("replacements.json", 'r') as json_file:
        data = json.load(json_file)
    for entry in data:
        yield entry["new"], entry["old"]

def find_and_replace_text(filepath):
    with open(filepath, 'rb') as file:
        try:
            # Read the raw bytes from the file
            print(f"reading contents of file {file.name}")
            file_content = file.read()
            for new_value, old_value in open_json():
                if old_value == "": continue
                file_content = file_content.replace(old_value.encode(), new_value.encode())

            print("writing to file")
            with open(filepath, 'wb') as output_file:
                output_file.write(file_content)
        except Exception as e:
            print(f"Error processing file '{filename}': {str(e)}")

if __name__ == "__main__":
    print("You must select the /www/data/ directory of your Fear and Hunger install")
    directory = get_directory_from_user()
    if directory:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                print(f"find and replacing {filepath}")
                find_and_replace_text(filepath)