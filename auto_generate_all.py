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

root = tk.Tk()
root.withdraw()
# scuffed but this works
print('The autogenerate script will generate the 4 fonts required for the base game. Default metrics and sizing will be used.')
print('Please select the regular fonts.')
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
print("Please select the bold fonts.")
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
if farc_exists and spr_exists:
    import farc
    import spr
    def replace_sprite_texture(farc_to_read, sprite_binary_to_edit, texname_to_edit, image_to_use, farc_to_write):
        entries = farc.read(farc_to_read)
        sprset = spr.read_from_raw(entries[sprite_binary_to_edit])
        sprset.replace_texture(texname_to_edit, image_to_use)
        farc.save(entries, farc_to_write, True)
    var_replace_sprite = None
    import json
    mod_json_array = {
          "preview": "https://images.gamebanana.com/img/ss/mods/62db8b8e73794.jpg","submitter": "feat_jinsoul","avi": "https://images.gamebanana.com/img/av/62bbea45f31d1.png","upic": "","caticon": "https://images.gamebanana.com/img/ico/ModCategory/6297a8ca8644e.png","cat": "User Interface","description": "","homepage": "https://gamebanana.com/mods/391229","lastupdate": "2022-07-23T05:50:18"
    }
    json_data = json.dumps(mod_json_array)
    folder_name = input("Please enter a folder name for the output. ")
else:
    print("farc and spr are not present...")
    print("not automating sprite creation!")

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
print("Setting up mod folder..")
toml_array = """enabled = true
name = "IBM Plex® Fonts"
description = "This is a mod that replaces both the LATIN9 and default (JP) fontsets. Does not include support for bold fonts at this time."
version = "1.0"
date = "22.07.2022"
author = "feat_jinsoul"
include = ["."]"""
try:
    if not os.path.isdir(folder_name):
        rom_folder_name = folder_name + "/rom"
        auth2d_folder_name = rom_folder_name + "/2d"
        os.makedirs(folder_name)
        os.makedirs(rom_folder_name)
        os.makedirs(auth2d_folder_name)
except OSError as e:
    print(e)
    print("Unable to create the directories for the folder name you want. Exiting...")
    exit(1)
# ok now I know the directories exist because I made them!
try:
    os.rename("spr_fnt_36latin9.farc", auth2d_folder_name + "/spr_fnt36_latin9.farc")
    os.rename("spr_fnt_36.farc", auth2d_folder_name + "/spr_fnt_36.farc")
    os.rename("spr_fnt_bold36.farc", auth2d_folder_name + "/spr_fnt_bold36.farc")
    os.rename("spr_fnt_bold36latin9.farc", auth2d_folder_name + "/spr_fnt_bold36latin9.farc")
except OSError as e:
    print(e)
    print("Unable to move the sprites to their location. Exiting...")
    exit(1)
# ok time to move the fontmap
try:
    os.rename("fontmap.farc", rom_folder_name + "/fontmap.farc")
except OSError as e:
    print(e)
    print("Unable to move the fontmap to its location. Exiting...")
    exit(1)
# ok time to. um. make the json and the toml
try:
    with open("{}\\config.toml".format(folder_name), "a+", encoding="utf-8") as f:
        f.write(toml_array)
    with open("{}\\mod.json".format(folder_name), "a+", encoding="utf-8") as f2:
        f2.write(json_data)
except OSError as e:
    print(e)
    print("Unable to create the config.toml. Exiting...")
    exit(1)