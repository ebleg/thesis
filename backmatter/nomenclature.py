#! /usr/bin/env python3

import os
import re
from dataclasses import dataclass
import jinja2
from jinja2 import Template

@dataclass
class Symbol:
    latex_string: str
    explanation: str
    tags: list
    sortkey: str = ""

GREEK_LETTER = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu",
                "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega")

class Nomenclature(object):
    def __init__(self, template_folder: str, scan_folder: str, exclude: tuple = ()):
        self.symbols = []

        self.jinja_env = jinja2.Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(template_folder)
        )

        # Loop over file
        for subdir, dirs, files in os.walk(scan_folder):
            for file in files:
                if os.path.join(subdir, file) not in exclude:
                    self.parse_file(os.path.join(subdir, file))

    def parse_file(self, file):
        with open(file) as f:
            for line in f.readlines():
                match = re.match(r"^%<symbol.*$", line)
                if match:
                    self.parse_string(line)

    def parse_string(self, line):
        # Only proceed if match
        if symbol_match := re.search(r"(?<=%<symbol:\s).+?(?=>)", line):
            symbol = symbol_match.group(0)

            # Only proceed if match
            if expl_match := re.search(r"(?<=<expl:\s).+?(?=>)", line):
                explanation = expl_match.group(0)
                if (tag_match := re.search(r"(?<=<tags:\s).+?(?=>)", line)):
                    tags = tag_match.group(0)
                    tags = tags.split(",")
                    tags = [tag.strip().lower() for tag in tags]

                else:
                    tags = []

                if sortkey_match := re.search(r"(?<=<sortkey:\s).+?(?=>)", line):
                    sortkey = sortkey_match.group(0)
                elif "letter" in tags:
                    sortkey = symbol.lower()
                elif "greek"in tags:
                    for char in GREEK_LETTER:
                        if re.search(char, symbol.lower()):
                            sortkey = str(GREEK_LETTER.index(char))
                            break
                else:
                    sortkey = ""

                self.symbols.append(Symbol(symbol, explanation, tags, sortkey))

    def create_nomenclature_section(self, template_name, filename, title, filter_fcn, level=1):
        template = self.jinja_env.get_template(template_name)
        nomencl_str = template.render(title=title,
                                      level=level,
                                      symbols=sorted([symbol for symbol in self.symbols if filter_fcn(symbol)],
                                      key=lambda symbol: symbol.sortkey))
        with open(filename, "w") as f:
            f.write(nomencl_str)


if __name__ == "__main__":
    print("test")
    home = r"C:\Users\emiel\Documents\MSc Systems and Control\Thesis\Git\thesis"
    folder = os.path.join(home, "main")
    nomencl = Nomenclature(folder)

    nomencl.create_nomenclature_section("nomenclature_template.tex", os.path.join(home, "main", "contact",
                                        "nomenclature.tex"), "Notation",
                                        filter_fcn=lambda symbol: "contact" in symbol.tags, level=1)
