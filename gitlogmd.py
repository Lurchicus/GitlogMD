"""
GitlogMD by Dan Rhea (12/24/2024)
GitlogMD (gitlogmd) will scan a log from a git repository (git log > logfile)
and reformat the contents into a markdown file (logfile.md) where logfile is
the name of the file containing the log to be formatted.
"""

import os.path
from colorama import Fore

class LogInfo:
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

infile = getfile("Enter the input filename [git log > file]: ", True)
mdfile = getfile("Enter the output filename [will become a markdown file]: ", False)
print(Fore.GREEN + "Input: " + infile + " Output: " + mdfile + Fore.WHITE)

# todo read input file...
GnuLog = []
InCount = 0
Chunk = ""
Meld = ""
File = open(infile, "r", encoding="utf-8")
for Line in File:
    # Skip empty lines
    if len(Line) > 1:
        # Instantiate the LogInfo class
        if Line.startswith("commit"):
            Info = LogInfo("","","","","")
        # Parse...
        # Get the commit and entry number
        if Line.startswith("commit"):
            Line = Line.strip()
            InCount = InCount + 1
            Stuff = Line.split()
            Info.num = str(InCount)
            Info.commit = Stuff[1].strip()
            #Info.message = "<<No message>>"
        # Get the author
        if Line.startswith("Author:"):
            Line = Line.strip()
            Meld = ""
            Chunk = ""
            Stuff = Line.split()
            for Chunk in Stuff[1:]:
                Meld = Meld + Chunk + " "
            Info.author = Meld.strip()
        # Get the date info
        if Line.startswith("Date:"):
            Line = Line.strip()
            Meld = ""
            Chunk = ""
            Stuff = Line.split()
            for Chunk in Stuff[1:]:
                Meld = Meld + Chunk + " "
            Info.date = Meld.strip()
        # Get the commit message
        if Line.startswith(" "):
            Info.message = Line.strip()
        # Push the Class onto a list
        if len(Info.message) > 0:
            GnuLog.append(Info)
File.close()

# Output the class info (this is where I'll create the MD file)
Info = LogInfo("","","","","")
OFile = open(mdfile, "w", encoding="utf-8")
Items = len(GnuLog)
OFile.writelines("# History (git log)\n")
#OFile.writelines(OLine)
for Info in GnuLog[0:]:
    OFile.writelines("\n\n## Commit " + str(Items) + " \n")
    OFile.writelines("| Item | Info | \n| :--- | :--- |\n")
    Items -= 1
    OFile.writelines("| Date | " + Info.date + " |\n")
    OFile.writelines("| Author | " + Info.author + " |\n")
    OFile.writelines("| Message | " + Info.message + " |\n")
    OFile.writelines("| commit | " + Info.commit + " |\n")
OFile.flush()
OFile.close()
