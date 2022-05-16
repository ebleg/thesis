#! /usr/bin python3

import subprocess
#import sys
import os
import texoutparse
from termcolor import colored
import shutil

FILENAME = "mscThesis.tex"
BUILD_DIR = "build"
BUILD_DIR = "."
BUILD_NAME = "mscThesis"
PPDFLATEX = "~/GitHub/pplatex-1.0-rc2/bin/ppdflatex"

HOME = os.getcwd()

# Functions for pretty printing
def print_colored_header(text, color):
    text = text.split('\n')
    print(colored(text[0], color))
    print("".join(text[1:]))
    print()

def boxed(msg, indent=0, padding=2):
    l = len(msg)
    top_line = indent*" " + "┌" + (l+2*padding)*"─" + "┐\n" 
    middle_line = indent*" " + "│" + padding*" " + msg + padding*" " + "│\n" 
    bottom_line = indent*" " + "└" + (l+2*padding)*"─" + "┘\n" 
    return top_line + middle_line + bottom_line
 

print()
print(colored(boxed("THESIS COMPILATION", indent=1, padding=28), "blue"))
print()

# Compilation
print("Start compilation")
print(80*"⎯")
result = subprocess.run(["latexmk", "-pdf", "-quiet", f"-jobname={BUILD_DIR}/{BUILD_NAME}"], capture_output=False)
print(80*"⎯")
print("Compilation finished")
print()

# Place pdf in the correct folder
#pdfname = f"{BUILD_NAME}.pdf"
#if os.path.exists(os.path.join(HOME, pdfname)):
#    os.remove(os.path.join(HOME, pdfname))
#
#if os.path.exists(os.path.join(HOME, BUILD_DIR, pdfname)):
#    shutil.copy(os.path.join(HOME, BUILD_DIR, pdfname), os.path.join(HOME, pdfname))

# Parsing
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
