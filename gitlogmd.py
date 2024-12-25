"""
GitlogMD by Dan Rhea (12/24/2024)
GitlogMD (gitlogmd) will scan a log from a git repository (git log > logfile)
and reformat the contents into a markdown file (logfile.md) where logfile is
the name of the file containing the log to be formatted.
"""


import os.path
from colorama import Fore, Back

def getfile(prompt=": "):
    if (len(prompt) <= 0):
        print(Fore.RED + "Error: Prompt string was not supplied!" + Fore.WHITE)
        return ""
    fname = ""
    while len(fname) <= 0:
        fname = input(Fore.YELLOW + prompt + Fore.WHITE)
        if len(fname) <= 0:
            print(Fore.RED + "Error: Input string was not provided." + Fore.WHITE)
        else:
            if not os.path.isfile("./" + fname):
                print(Fore.RED + "Error: File ./" + fname + " was not found." + Fore.WHITE)
                fname = ""
            else:
                break
    return fname

infile = getfile("Enter the input filename [git log > file]: ")
mdfile = getfile("Enter the output filename [will become a markdown file]: ")
print(Fore.GREEN + "Input: " + infile + " Output: " + mdfile + Fore.WHITE)

#todo read input file...
