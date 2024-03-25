#Renamer
#Python File and Folder Renamer
#Version: 1.0
#https://recordsmanagement.ubc.ca
#https://www.gnu.org/licenses/gpl-3.0.en.html

import os
import time
from datetime import datetime
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
import subprocess

def replace_chars_in_files(filename):
    return filename.replace(chars_old.get(), chars_new.get())

def rename_files_in_directory(directory, include_subfolders=True):
    renamed_files_count = 0
    renamed_files_info = []
    for root, dirs, files in os.walk(directory):
        if not include_subfolders and root != directory:
            continue  # Skip subdirectories if include_subfolders is False

        for filename in files:
            if chars_old.get() in filename:
                new_filename = replace_chars_in_files(filename)
                base, ext = os.path.splitext(new_filename)
                new_path = os.path.join(root, new_filename)
                old_path = os.path.join(root, filename)
                was_numbered = False  # Initialize the variable

                # Check if the new path already exists
                counter = 2
                while os.path.exists(new_path) and new_path.lower() != old_path.lower():
                    new_filename = f"{base} {counter}{ext}"
                    new_path = os.path.join(root, new_filename)
                    counter += 1
                    was_numbered = True  # File was numbered

                # Rename the file
                os.rename(old_path, new_path)
                renamed_files_count += 1
                if renamed_files_count % 10 == 0:
                    progress_var.set(str(renamed_files_count))

                # Store information about the renamed file
                renamed_files_info.append((old_path, new_path, was_numbered))
    return renamed_files_count, renamed_files_info

def rename_folders_in_directory(directory, chars_old, chars_new):
    renamed_folders_count = 0
    renamed_folders_info = []
    for root, dirs, _ in os.walk(directory):
        for folder_name in dirs:
            if chars_old in folder_name:
                new_folder_name = folder_name.replace(chars_old, chars_new)
                old_path = os.path.join(root, folder_name)
                new_path = os.path.join(root, new_folder_name)

                # Check if the new path already exists
                counter = 2
                while os.path.exists(new_path) and new_path.lower() != old_path.lower():
                    new_folder_name = f"{new_folder_name} {counter}"
                    new_path = os.path.join(root, new_folder_name)
                    counter += 1

                os.rename(old_path, new_path)
                renamed_folders_count += 1

                # Store information about the renamed folder
                if counter > 2:
                    was_numbered = True
                else:
                    was_numbered = False
                renamed_folders_info.append((old_path, new_path, was_numbered))
    return renamed_folders_count, renamed_folders_info

def recursive_folder_rename(directory, chars_old, chars_new):
    renamed_folders_info = []
    total_renamed_folders_count = 0

    while True:
        renamed_folders_count, renamed_folders_in_loop = rename_folders_in_directory(directory, chars_old, chars_new)
        total_renamed_folders_count += renamed_folders_count
        renamed_folders_info.extend(renamed_folders_in_loop)

        if not renamed_folders_count:
            break

    return total_renamed_folders_count, renamed_folders_info

def log_error(error_message):
    global timestamp
    with open(f'Error-Log_{timestamp}.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"{error_message}\n")

def show_completion_message(execution_time_str, output_file, error_log_path, renamed_files_count):
    completion_window = tk.Toplevel(root)
    completion_window.title("Operation Completed")
    completion_window.resizable(False, False)

    if output_file:
        message = f"Execution completed in {execution_time_str}.\n\nTotal number of renamed items: {renamed_files_count}\n\nLog file saved as {output_file}"
    else:
        message = f"Execution completed in {execution_time_str}.\n\nNo items were renamed."

    completion_label = tk.Label(completion_window, text=message)
    completion_label.pack(padx=20, pady=5)

    if output_file:
        open_button = tk.Button(completion_window, text="Open Log File", command=lambda: open_output_file(output_file))
        open_button.pack(pady=5)

    if os.path.exists(error_log_path):
        error_log_label = tk.Label(completion_window, text=f"Error log saved as {error_log_path}")
        error_log_label.pack(pady=5)

        open_log_button = tk.Button(completion_window, text="Open Error Log", command=lambda: open_output_file(error_log_path))
        open_log_button.pack(pady=5)

    chars_old.set('')
    chars_new.set('')
    progress_var.set("0")
    include_subfolders_var.set(False)


def open_output_file(output_file):
    try:
        subprocess.run(['start', '', output_file], shell=True)
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error opening file: {str(e)}")

def rename_items_in_thread(include_subfolders=True):
    global timestamp
    top_directory = input_path_entry.get()

    if not chars_old.get():
        output_label.config(fg="red")
        output_text.set("Old Character field cannot be empty!")
        return
    
    if not os.path.exists(top_directory):
        output_label.config(fg="red")
        output_text.set("Invalid path!")
        return

    output_text.set("")

    # Confirmation dialog
    subfolders_message = " and its subfolders" if include_subfolders else ""
    operation_type = operation_var.get()
    
    if operation_type == "Rename Files":
        confirmation_message = f"This will replace all '{chars_old.get()}' characters with '{chars_new.get()}' characters in file names in the following folder{subfolders_message}:\n\n'{top_directory}'\n\nThis cannot be undone. Are you sure you want to continue?"
    elif operation_type == "Rename Folders":
        confirmation_message = f"This will replace all '{chars_old.get()}' characters with '{chars_new.get()}' characters in folder names in the following folder{subfolders_message}:\n\n'{top_directory}'\n\nThis cannot be undone. Are you sure you want to continue?"

    # Confirmation dialog
    if not messagebox.askyesno("Confirm", confirmation_message):
        return

    start_spinner()

    start_time = time.time()
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Choose between renaming files or renaming folders
    if operation_type == "Rename Files":
        renamed_files_count, renamed_files_info = rename_files_in_directory(top_directory, include_subfolders)
    elif operation_type == "Rename Folders":
        if include_subfolders:
            renamed_files_count, renamed_files_info = recursive_folder_rename(top_directory, chars_old.get(), chars_new.get())
        else:
            renamed_files_count, renamed_files_info = rename_folders_in_directory(top_directory, chars_old.get(), chars_new.get())
    
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_str = time.strftime("%H:%M:%S", time.gmtime(execution_time))

    output_file = ''
    error_log_path = os.path.join(os.getcwd(), f'Error-Log_{timestamp}.txt')

    if renamed_files_count != 0:
        output_csv_file = f'Renamed-Items_{timestamp}.csv'
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Original Name', 'Renamed Name', 'Numbered'])
            for old_path, new_path, was_numbered in renamed_files_info:
                writer.writerow([old_path, new_path, 'Yes' if was_numbered else 'No'])
        output_file = output_csv_file

    stop_spinner()
    show_completion_message(execution_time_str, output_file, error_log_path, renamed_files_count)

thread = threading.Thread(target=rename_items_in_thread, daemon=True)

def execute_button_callback():
    global thread

    if thread.is_alive():
        output_text.set("A process is already running.")
    else:
        input_path_entry.config(state=tk.DISABLED)
        execute_button.config(state=tk.DISABLED)
        browse_button.config(state=tk.DISABLED)
        chars_old_entry.config(state=tk.DISABLED)
        chars_new_entry.config(state=tk.DISABLED)
        include_subfolders_check.config(state=tk.DISABLED)

        include_subfolders = include_subfolders_var.get()  # Get the user's choice
        thread = threading.Thread(target=rename_items_in_thread, args=(include_subfolders,), daemon=True)
        thread.start()

        root.after(100, check_thread_status)

def check_thread_status():
    if thread.is_alive():
        root.after(100, check_thread_status)
    else:
        input_path_entry.config(state=tk.NORMAL)
        execute_button.config(state=tk.NORMAL)
        browse_button.config(state=tk.NORMAL)
        chars_old_entry.config(state=tk.NORMAL)
        chars_new_entry.config(state=tk.NORMAL)
        include_subfolders_check.config(state=tk.NORMAL)

def browse_button_callback():
    selected_path = filedialog.askdirectory()
    if selected_path:
        input_path_entry.delete(0, tk.END)
        input_path_entry.insert(0, selected_path)
        output_label.config(fg="black")
        output_text.set("")
    output_text.set("")
    progress_var.set("0")
    include_subfolders_var.set(False)

# File menu functions
def exit_app():
    if threading.active_count() > 1:
        confirm = tk.messagebox.askyesno("Exit?", "A process is running. Are you sure you want to exit?")
        if not confirm:
            return
    root.destroy()

def clear_fields():
    # Enable the Path entry
    input_path_entry.config(state=tk.NORMAL)

    # Clear the fields
    input_path_entry.delete(0, tk.END)
    output_text.set("")
    progress_var.set("0")
    chars_old.set('')
    chars_new.set('')
    include_subfolders_var.set(False)

def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.resizable(False, False)

    help_message = "This application allows you to rename files and folders by replacing specific characters within their names.\n\n" \
               "To use this tool:\n\n" \
               "1. Click 'Browse' to select the top-level directory for renaming. \n\n" \
               "2. In the 'Old Character' field, enter the character(s) you wish to replace. This field must not be empty.\n\n" \
               "3. In the 'New Character' field, enter the replacement character(s). Leave this field empty if you want to remove the old characters without replacing them.\n\n" \
               "4. Choose the operation type using the radio buttons: 'Rename Files' or 'Rename Folders'.\n\n" \
               "5. Check the 'Include Subfolders' checkbox if you want the renaming process to include files or folders within subdirectories.\n\n" \
               "6. Click 'Rename' to start the process.\n\n" \
               "Please note:\n" \
               "- The 'Old Charachter' and 'New Character' fields are both case-sensitive.\n" \
               "- The renaming process cannot be undone. Ensure you have backups of important files.\n" \
               "- The application provides a csv report upon completion, including the total number of files or folders renamed.\n\n" \
               "Use this tool with caution and verify your inputs before proceeding."

    help_label = tk.Label(help_window, text=help_message, justify=tk.LEFT)
    help_label.pack(padx=20, pady=10)


def show_about():
    about_message = "Renamer\nVersion 1.0"
   
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.resizable(False, False)

    about_label = tk.Label(about_window, text=about_message)
    about_label.pack(padx=20, pady=10)

    # Frame for UBC RMO
    ubc_frame = tk.Frame(about_window)
    ubc_frame.pack(padx=20, pady=20)

    ubc_label = tk.Label(ubc_frame, text="Developed by\nRecords Management Office\nThe University of British Columbia")
    ubc_label.pack()

    ubc_link_label = tk.Label(ubc_frame, text="https://recordsmanagement.ubc.ca", fg="blue", cursor="hand2")
    ubc_link_label.pack()

    def open_ubc_link(event):
        import webbrowser
        webbrowser.open("https://recordsmanagement.ubc.ca")

    ubc_link_label.bind("<Button-1>", open_ubc_link)

    # Frame for license
    license_frame = tk.Frame(about_window)
    license_frame.pack(padx=20, pady=10)

    license_label = tk.Label(license_frame, text="License: ")
    license_label.pack(side='left')

    license_link_label = tk.Label(license_frame, text="GPL-3.0", fg="blue", cursor="hand2")
    license_link_label.pack(side='left')

    def open_license_link(event):
        import webbrowser
        webbrowser.open("https://www.gnu.org/licenses/gpl-3.0.en.html")

    license_link_label.bind("<Button-1>", open_license_link)

def start_spinner():
    # Create and start the spinner
    spinner_frame.pack_forget()  # Remove any existing spinner frame
    spinner_frame.pack(pady=10)
    spinner.start(10)  # You may adjust the interval as needed

def stop_spinner():
    # Stop and hide the spinner
    spinner.stop()
    spinner_frame.pack_forget()

# Main window
root = tk.Tk()
root.title("Renamer")
root.geometry("600x180")
root.resizable(False, False)

# Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# File menu options
file_menu.add_command(label="Clear Fields", command=clear_fields)
file_menu.add_command(label="Exit", command=exit_app)

# Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Help menu options
help_menu.add_command(label="Help", command=show_help)
help_menu.add_command(label="About", command=show_about)

# Main window padding
root.option_add('*TButton*Padding', 5)
root.option_add('*TButton*highlightThickness', 0)
root.option_add('*TButton*highlightColor', 'SystemButtonFace')

# File renaming
chars_old = tk.StringVar()
chars_new = tk.StringVar()
operation_var = tk.StringVar(value="Rename")

frameR = tk.Frame(root)
frameR.pack(padx=10, pady=10)

# Old character input
chars_old_label = tk.Label(frameR, text="Old Character:")
chars_old_label.pack(side='left')
chars_old_entry = tk.Entry(frameR, textvariable=chars_old)
chars_old_entry.pack(side='left', padx=10)

# New character input
chars_new_label = tk.Label(frameR, text="New Character:")
chars_new_label.pack(side='left')
chars_new_entry = tk.Entry(frameR, textvariable=chars_new)
chars_new_entry.pack(side='left', padx=10)

# Frame to hold the path input field and the "Browse" button
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Input field for the path
input_label = tk.Label(frame, text="Directory Path:")
input_label.pack(side='left')

input_path_entry = tk.Entry(frame, width=60)
input_path_entry.pack(side='left', padx=10)

# "Browse" button
browse_button = tk.Button(frame, text="Browse", command=browse_button_callback)
browse_button.pack(side='left', padx=10)

# Frame for the "Include Subfolders" checkbox and radio buttons
frameS = tk.Frame(root)
frameS.pack(padx=10, pady=10)

# "Include Subfolders" checkbox
include_subfolders_var = tk.BooleanVar(value=False)
include_subfolders_check = tk.Checkbutton(frameS, text="Include Subfolders", variable=include_subfolders_var)
include_subfolders_check.pack(side='left', padx=10)

# Radio buttons for "Rename Files" and "Rename Folders"
operation_var = tk.StringVar(value="Rename Files")  # Initial value
rename_files_radio = tk.Radiobutton(frameS, text="Rename Files", variable=operation_var, value="Rename Files")
rename_files_radio.pack(side='left', padx=10)

rename_folders_radio = tk.Radiobutton(frameS, text="Rename Folders", variable=operation_var, value="Rename Folders")
rename_folders_radio.pack(side='left', padx=10)

# Frame to hold the "Execute" button
frameE = tk.Frame(root)
frameE.pack(padx=10, pady=10)

# "Execute" button
execute_button = tk.Button(frameE, text="Rename", command=execute_button_callback)
execute_button.pack(side='left', padx=10)

# Output label to display invalid path messages
output_text = tk.StringVar()
output_label = tk.Label(frameE, textvariable=output_text)
output_label.pack(side='left', padx=10)

# Progress label
progress_label = tk.Label(frameE, text="Renamed files/folders:")
progress_label.pack(side='left', padx=10)

# Shared variable to store the count of renamed files/folders
progress_var = tk.StringVar()
progress_var.set("0")  # Initialize to 0

# Label to display the count of renamed files/folders
rows_written_label = tk.Label(frameE, textvariable=progress_var)
rows_written_label.pack(side='left')

# Spinner setup
spinner_frame = tk.Frame(root)
spinner_frame.pack_forget()  # Initially hide the spinner frame
spinner = ttk.Progressbar(spinner_frame, mode='indeterminate', length=500)
spinner.pack()

root.protocol("WM_DELETE_WINDOW", exit_app)

if __name__ == "__main__":
    root.mainloop()
