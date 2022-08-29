#! /usr/bin python3

import subprocess
#import sys
import os
import glob
import texoutparse
from termcolor import colored
import shutil

from backmatter.nomenclature import Nomenclature

FILENAME = "mscThesis.tex"
BUILD_DIR = "build"
BUILD_NAME = "mscThesis"

HOME = os.getcwd()

BUILD_DIR_FULL = os.path.join(HOME, BUILD_DIR)

# Steps to take 2. Clean directory 3. Copy build directory 4. build 5. Clean build directory
# 6. Copy build files to build (spare pdf)

# --------------------------------------------------------------------------------------------------------------------
# Functions for pretty printing
# --------------------------------------------------------------------------------------------------------------------
def print_colored_header(text, color):
    text = text.split('\n')
    print(colored(text[0], color))
    print("".join(text[1:]))
    print()

# Function for text in colored box
def boxed(msg, indent=0, padding=2):
    l = len(msg)
    top_line = indent*" " + "┌" + (l+2*padding)*"─" + "┐\n" 
    middle_line = indent*" " + "│" + padding*" " + msg + padding*" " + "│\n" 
    bottom_line = indent*" " + "└" + (l+2*padding)*"─" + "┘\n" 
    return top_line + middle_line + bottom_line

# --------------------------------------------------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------------------------------------------------
print()
print(colored(boxed("THESIS COMPILATION", indent=1, padding=28), "blue"))
print()

# --------------------------------------------------------------------------------------------------------------------
# Generate nomenclature
# --------------------------------------------------------------------------------------------------------------------
print("Generate nomenclature")
nomencl = Nomenclature(os.path.join(HOME, "backmatter"), [os.path.join(HOME, "main/contact"), 
                                                          os.path.join(HOME, "main/quaternions"),
                                                          os.path.join(HOME, "main/other"),
                                                          os.path.join(HOME, "backmatter", "appendix"), 
                                                          os.path.join(HOME, "preamble")])

nomencl.create_nomenclature_section("nomenclature_template.tex", os.path.join(HOME, "backmatter", "symbols_pt1.tex"),
                                    "Chapters 2 and 3", 
                                    filter_fcn=lambda symbol: set(("econ", "geometry", "numberset")).intersection(set(symbol.tags)), 
                                    level=1)

nomencl.create_nomenclature_section("nomenclature_template.tex", os.path.join(HOME, "backmatter", 
                                    "symbols_pt2.tex"), "Chapter 4", 
                                    filter_fcn=lambda symbol: set(("quaternions",)).intersection(set(symbol.tags)), 
                                    level=1)

# --------------------------------------------------------------------------------------------------------------------
# Clean directory
# --------------------------------------------------------------------------------------------------------------------
print("Clean directory")
files_to_remove = glob.glob(os.path.join(HOME, f"{BUILD_NAME}*.*"))
for file in files_to_remove:
    if not (file[-4:] in [".pdf", ".cls", ".tex"]):
        os.remove(file)
        print(f"Removed {file}")

print("Copy from build dir")
files_to_move = glob.glob(os.path.join(BUILD_DIR_FULL, f"{BUILD_NAME}.*"))
for file in files_to_move:
    try:
        shutil.move(file, HOME)
    except shutil.Error:
        print(f"Could not move file {file}")

# --------------------------------------------------------------------------------------------------------------------
# Compilation
# --------------------------------------------------------------------------------------------------------------------
print("Start compilation")
print(80*"⎯")
result = subprocess.run(["latexmk", "-pdf", "-quiet"], capture_output=False)
print(80*"⎯")
print("Compilation finished")
print()

# --------------------------------------------------------------------------------------------------------------------
# Clean build dir
# --------------------------------------------------------------------------------------------------------------------
for file in os.listdir(BUILD_DIR_FULL):
    os.remove(os.path.join(BUILD_DIR_FULL, file))

# Check if build dir is empty
if os.listdir(BUILD_DIR_FULL): # List is False if empty
    print("List dir not empty --- abort file management")
else:
    # Move everything back
    files_to_move = glob.glob(os.path.join(HOME, BUILD_NAME) + "*.*")

    for file in files_to_move:
        if not (file[-4:] in [".pdf", ".cls", ".tex"]):
            shutil.move(file, BUILD_DIR_FULL)

# --------------------------------------------------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------------------------------------------------
#parse_result = subprocess.run([PPDFLATEX, os.path.join(HOME, BUILD_DIR, f"{BUILD_NAME}.log")])
parser = texoutparse.LatexLogParser()
with open(os.path.join(HOME, BUILD_DIR, f"{BUILD_NAME}.log")) as logfile:
    parser.process(logfile)

if len(parser.badboxes) != 0:
    print(colored(boxed("BAD BOXES", indent=30), "cyan"))
    for badbox in parser.badboxes:
        print_colored_header(str(badbox), "cyan")
        print()
    print()

if len(parser.warnings) != 0:
    print(colored(boxed("WARNINGS", indent=32), "yellow"))
    for warningmsg in parser.warnings:
        print_colored_header(str(warningmsg), "yellow")
        print()
    print()

if len(parser.errors) != 0:
    print(colored(boxed("ERRORS", indent=33), "red"))
    for errormsg in parser.errors:
        print_colored_header(str(errormsg), "red")
        print()
    print()

print(colored(parser, 'green'))
