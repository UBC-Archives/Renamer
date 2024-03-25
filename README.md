# Renamer
Python file and folder renamer with GUI and log
> Version: 1.0

> [UBC Records Management Office](https://recordsmanagement.ubc.ca)

> [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html)

**Renamer** is a Python application designed to facilitate the renaming of files and folders within a specified directory. It provides a simple user-friendly interface to replace specific characters in filenames and folder names.

![image](https://github.com/UBC-Archives/renamer/assets/6263442/cdb4c74f-be08-4c94-9432-9a1ce7ec31ef)


**Features:**
- Replace characters in filenames and folder names
- Choose between renaming files or folders
- Option to include subfolders in the renaming process
- Generates a CSV report upon completion, detailing the changes made

**How to Use:**

1. Select Directory: Click on the "Browse" button to choose the top-level directory containing the files and folders you want to rename.

2. Character Replacement: Enter the character(s) you wish to replace in the "Old Character" field and the replacement character(s) in the "New Character" field.

3. Choose Operation Type: Select whether you want to rename files or folders using the radio buttons provided.

4. Include Subfolders: Check the "Include Subfolders" checkbox if you want to include files or folders within subdirectories in the renaming process.

5. Execute: Click on the "Rename" button to start the renaming process.

6. Completion Message: Upon completion, a message will display the total number of renamed items, and a CSV report will be generated with detailed information about the changes made.

**Notes:**

- The "Old Character" and "New Character" fields are case-sensitive.
- If the script attempts to rename a file, and a file with that name already exists in the folder, a number will be added to the end of the new file name. For example, if the script wants to rename 'final_report.pdf' to 'final report.pdf' and a 'final report.pdf' file already exists in the same path, the 'final_report.pdf' file will be renamed to 'final report 2.pdf'. The numbered files will be tagged in the ‘Numbered’ column in the CSV output.
- Renaming is irreversible, so ensure you have backups of important files.
- Use the application with caution, and verify your inputs before proceeding.

**Installation:**

- First, install Python 3.x on your system. You can download Python from [here](https://www.python.org/downloads).
- Next, download the Renamer Python script from [this link](https://github.com/UBC-Archives/renamer/blob/main/UBC-RMO_Renamer.py).
- Once downloaded, double-click on the downloaded UBC-RMO_Renamer.py file to run the program.

**Disclaimer:**

The UBC Records Management Office is not responsible for any loss of data or unintended consequences resulting from the use of this script. Exercise caution and thoroughly review the script to ensure it aligns with your requirements. Please understand and review the changes this script will make to your data before proceeding. If you are uncertain about its functionality or impact, seek professional advice or assistance.
By using this script, you acknowledge and accept the potential risks and responsibilities associated with renaming files and folders, and you agree to use it responsibly and with appropriate precautions.
