import os
from tkinter import *
import tkinter as tk
import tkinter.filedialog as fd
from sys import platform

root = tk.Tk()
# scuffed but this works
tk.messagebox.showwarning(message='The autogenerate script will generate the 4 fonts required for the base game. Default metrics and sizing will be used.')
tk.messagebox.showwarning(message='Please select the regular fonts.')
regular_fontlist = fd.askopenfilenames(filetypes=[("Fonts", ".ttf .otf")], parent=root, title='Choose the regular fonts.')
regular_fontlist = list(regular_fontlist)
for file in regular_fontlist:
    regular_fontlist = str(regular_fontlist)
# fear me
regular_fontlist = regular_fontlist.replace('(','').replace(')','').replace('[','').replace(']','').replace(', ',',')
# time to do it again for the bold fonts.
tk.messagebox.showwarning(message='Please select the bold fonts.')
bold_fontlist = fd.askopenfilenames(filetypes=[("Fonts", ".ttf .otf")], parent=root, title='Choose the bold fonts.')
bold_fontlist = list(bold_fontlist)
for file in bold_fontlist:
    bold_fontlist = str(bold_fontlist)
# fear me again
bold_fontlist = bold_fontlist.replace('(','').replace(')','').replace('[','').replace(']','').replace(', ',',')

print("Running scripts..")
print("Your platform is {}...".format(platform))
if platform == "darwin":
    os.system("python3 generate_font.py -f {} -s 36 -m 36,36,38,38 --latin9".format(regular_fontlist))
    os.system("python3 generate_font.py -f {} -s 36 -m 36,36,38,38 --japanese36".format(regular_fontlist))
    os.system("python3 generate_font.py -f {} -s 36 -m 36,36,38,38 --latin9_bold36".format(bold_fontlist))
    os.system("python3 generate_font.py -f {} -s 36 -m 36,36,38,38 --japanese_bold36".format(bold_fontlist))
elif platform == "win32":
    os.system("python generate_font.py -f {} -s 36 -m 36,36,38,38 --latin9".format(regular_fontlist))
    os.system("python generate_font.py -f {} -s 36 -m 36,36,38,38 --japanese36".format(regular_fontlist))
    os.system("python generate_font.py -f {} -s 36 -m 36,36,38,38 --latin9_bold36".format(bold_fontlist))
    os.system("python generate_font.py -f {} -s 36 -m 36,36,38,38 --japanese_bold36".format(bold_fontlist))

print()
print()
tk.messagebox.showwarning(message='About to move fontmap and generate farc.')
print("Moving fontmaps into the fontmap directory..")
try:
    os.replace("font11_36x36.json", "fontmap/font11_36x36.json")
    os.replace("font14_36x36.json", "fontmap/font14_36x36.json")
    os.replace("font20_36x36.json", "fontmap/font20_36x36.json")
    os.replace("font22_36x36.json", "fontmap/font22_36x36.json")
except OSError as error:
    print(OSError)
    print("Unable to copy the fontmaps into the fontmap directory!")
    exit(1)
print("Successfully moved fontmaps into the fontmap directory!")

if platform == "darwin":
    os.system("python3 fontmap_extract.py fontmap/")
elif platform == "win32":
    os.system("python fontmap_extract.py fontmap/")
print("Successfully built fontmap farc!")

