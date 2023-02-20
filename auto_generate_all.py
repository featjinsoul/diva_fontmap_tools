import os
from tkinter import *
import tkinter as tk
import tkinter.filedialog as fd
from sys import platform
import argparse
import importlib.util

def get_args(add_ignore_gooey=True):
    parser = argparse.ArgumentParser(description='DIVA Font Generator')
    font_args = parser.add_argument_group('Per-Font Settings', 'set the fonts to use -- all arguments accept comma-separated lists for fallback font support')
    font_args.add_argument('--shrink', default=None, help='shrink the amount of space each character takes in its box by X pixels (optional)')
    return parser.parse_args()

args = get_args()

farc_spec = importlib.util.find_spec("farc")
farc_exists = farc_spec is not None
spr_spec = importlib.util.find_spec("spr")
spr_exists = spr_spec is not None

if farc_exists and spr_exists:
    import farc
    import spr
    def replace_sprite_texture(farc_to_read, sprite_binary_to_edit, texname_to_edit, image_to_use, farc_to_write):
        entries = farc.read(farc_to_read)
        sprset = spr.read_from_raw(entries[sprite_binary_to_edit])
        sprset.replace_texture(texname_to_edit, image_to_use)
        farc.save(entries, farc_to_write, True)
    var_replace_sprite = None
else:
    print("farc and spr are not present...")
    print("not automating sprite creation!")

root = tk.Tk()
root.withdraw()
# scuffed but this works
tk.messagebox.showwarning(message='The autogenerate script will generate the 4 fonts required for the base game. Default metrics and sizing will be used.')
tk.messagebox.showwarning(message='Please select the regular fonts.')
regular_fontlist = fd.askopenfilenames(filetypes=[("Fonts", ".ttf .otf")], parent=root, title='Choose the regular fonts.')
regular_fontlist = list(regular_fontlist)
for file in regular_fontlist:
    regular_fontlist = str(regular_fontlist)
# fear me
if platform == "darwin":
    regular_fontlist = regular_fontlist.replace('(','').replace(')','').replace('[','').replace(']','').replace(', ',',')
elif platform == "win32":
    regular_fontlist = regular_fontlist.replace('(','').replace(')','').replace('[','').replace(']','').replace(', ',',').replace("'",'')

# time to do it again for the bold fonts.
tk.messagebox.showwarning(message='Please select the bold fonts.')
bold_fontlist = fd.askopenfilenames(filetypes=[("Fonts", ".ttf .otf")], parent=root, title='Choose the bold fonts.')
bold_fontlist = list(bold_fontlist)
for file in bold_fontlist:
    bold_fontlist = str(bold_fontlist)
# fear me again
if platform == "darwin":
    bold_fontlist = bold_fontlist.replace('(','').replace(')','').replace('[','').replace(']','').replace(', ',',')
elif platform == "win32":
    bold_fontlist = bold_fontlist.replace('(','').replace(')','').replace('[','').replace(']','').replace(', ',',').replace("'",'')
print(regular_fontlist)
print(bold_fontlist)

print("Running scripts..")
print("Your platform is {}...".format(platform))
if platform == "darwin":
    os.system("python3 generate_font.py -f {} -s 36 -m 36,36,38,38 --latin9".format(regular_fontlist))
    os.system("python3 generate_font.py -f {} -s 36 -m 36,36,38,38 --japanese36".format(regular_fontlist))
    os.system("python3 generate_font.py -f {} -s 36 -m 36,36,38,38 --latin9_bold36".format(bold_fontlist))
    os.system("python3 generate_font.py -f {} -s 36 -m 36,36,38,38 --japanese_bold36".format(bold_fontlist))
elif platform == "win32":
    if args.shrink:
        os.system("python generate_font.py -f {} -s 36 -m 36,36,38,38 --latin9 --shrink {}".format(regular_fontlist, args.shrink))
        os.system("python generate_font.py -f {} -s 36 -m 36,36,38,38 --japanese36 --shrink {}".format(regular_fontlist, args.shrink))
        os.system("python generate_font.py -f {} -s 36 -m 36,36,38,38 --latin9_bold36 --shrink {}".format(bold_fontlist, args.shrink))
        os.system("python generate_font.py -f {} -s 36 -m 36,36,38,38 --japanese_bold36 --shrink {}".format(bold_fontlist, args.shrink))
    else:
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
    print(error)
    print("Unable to copy the fontmaps into the fontmap directory!")
    exit(1)
print("Successfully moved fontmaps into the fontmap directory!")

if platform == "darwin":
    os.system("python3 fontmap_extract.py fontmap/")
elif platform == "win32":
    os.system("python fontmap_extract.py fontmap/")
print("Successfully built fontmap farc!")
print("Creating sprite farcs!")
if replace_sprite_texture:
    replace_sprite_texture("base_spr_fnt_36latin9.farc", "spr_fnt_36latin9.bin", "NOMERGE_D5COMP_000_0", "font11_36x36.png", "spr_fnt_36latin9.farc")
    replace_sprite_texture("base_spr_fnt_36.farc", "spr_fnt_36.bin", "NOMERGE_D5COMP_000_0", "font20_36x36.png", "spr_fnt_36.farc")
    replace_sprite_texture("base_spr_fnt_bold36.farc", "spr_fnt_bold36.bin", "NOMERGE_D5COMP_000_0", "font22_36x36.png", "spr_fnt_bold36.farc")
    replace_sprite_texture("base_spr_fnt_bold36latin9.farc", "spr_fnt_bold36latin9.bin", "NOMERGE_D5COMP_000_0", "font14_36x36.png", "spr_fnt_bold36latin9.farc")
    var_replace_sprite = True
else: 
    print("Skipping sprite creation!")
if var_replace_sprite == True:
    print("Cleaning up images..")
    os.remove("font11_36x36.png")
    os.remove("font14_36x36.png")
    os.remove("font20_36x36.png")
    os.remove("font22_36x36.png")
