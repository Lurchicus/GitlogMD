"""
GitlogMD by Dan Rhea (12/24/2024)
GitlogMD (gitlogmd) will scan a log from a git repository (git log > logfile)
and reformat the contents into a markdown file (logfile.md) where logfile is
the name of the file containing the log to be formatted.

I have been looking at this project and finally had to admit that the "history"
output file was of limited  use as it was always one commit behind. I'm going
to add a "-b" brief format that will create single lines (md format) that is
really ment to be run once and added to the README.md file.
"""

import os.path
from colorama import Fore

class loginfo:
    """
    This class saves individual git log information for later formatting.
    All values are strings. These will be stored in a list.
    """
    def __init__(self, num, commit, author, date, message):
        self.num = num
        self.commit = commit
        self.author = author
        self.date = date
        self.message = message


def getfile(prompt=": ", check=True):
    """
    This function shows a predefined prompt and collects input from the user.
    The input is validated for nonzero input length, nonzero prompt length
    and optionally file existance. Errors messages are displayed for these if
    needed.

    prompt: A plain text string that will be shown to the user (default "")
    check:  A boolean flag to indicate if file existance is to be checked
            or not (default: True)
    return  A string containing (we hope) a filename in the current directory
    """
    if len(prompt) <= 0:
        print(Fore.RED + "Error: Prompt string was not supplied!" + Fore.WHITE)
        return ""
    fname = ""
    while len(fname) <= 0:
        fname = input(Fore.YELLOW + prompt + Fore.WHITE)
        if len(fname) <= 0:
            print(Fore.RED + "Error: Input string was not provided." + Fore.WHITE)
        else:
            if check:
                if not os.path.isfile("./" + fname):
                    print(Fore.RED + "Error: File ./" + fname + " was not found." + Fore.WHITE)
                    fname = ""
                else:
                    break
            else:
                break
    return fname


in_file = getfile("Enter the input filename [git log > file]: ", True)
md_file = getfile("Enter the output filename [will become a markdown file]: ", False)
print(Fore.GREEN + "Input: " + in_file + " Output: " + md_file + Fore.WHITE)

gnu_log = []
in_count: int = 0
chunk: str = ""
meld: str = ""
file = open(in_file, "r", encoding="utf-8")
for line in file:
    # Skip empty lines
    if len(line) > 1:
        # Instantiate the LogInfo class
        if line.startswith("commit"):
            info = loginfo("","","","","")
        # Parse...
        # Get the commit and entry number
        if line.startswith("commit"):
            line = line.strip()
            in_count = in_count + 1
            stuff = line.split()
            info.num = str(in_count)
            info.commit = stuff[1].strip()
            #Info.message = "<<No message>>"
        # Get the author
        if line.startswith("Author:"):
            line = line.strip()
            meld = ""
            chunk = ""
            stuff = line.split()
            for chunk in stuff[1:]:
                meld = meld + chunk + " "
            info.author = meld.strip()
        # Get the date info
        if line.startswith("Date:"):
            line = line.strip()
            meld = ""
            chunk = ""
            stuff = line.split()
            for chunk in stuff[1:]:
                meld = meld + chunk + " "
            info.date = meld.strip()
        # Get the commit message
        if line.startswith(" "):
            info.message = line.strip()
        # Push the Class onto a list
        if len(info.message) > 0:
            gnu_log.append(info)
file.close()

# Output the class info (this is where I'll create the MD file)
info = loginfo("","","","","")
o_file = open(md_file, "w", encoding="utf-8")
items = len(gnu_log)
o_file.writelines("# History (git log)\n")
#OFile.writelines(OLine)
for info in gnu_log[0:]:
    o_file.writelines("\n\n## Commit " + str(items) + " \n")
    o_file.writelines("| Item | Info | \n| :--- | :--- |\n")
    items -= 1
    o_file.writelines("| Date | " + info.date + " |\n")
    o_file.writelines("| Author | " + info.author + " |\n")
    o_file.writelines("| Message | " + info.message + " |\n")
    o_file.writelines("| commit | " + info.commit + " |\n")
o_file.flush()
o_file.close()
