##########################################################
# file : Assembler.py
# writer : Nadav vitri , nadav.vitri , 203819909
#          Arie shtine, arie.shtine, 204616122
# EXERCISE : nand2tetris ex6 2017-2018
# DESCRIPTION: This program translate asm file to Hack binary code
##########################################################

############################################################
# Imports
############################################################
import sys
import os
import Parse
import Code_tables

############################################################
# Constants
############################################################
FILE_ARG_INDEX = 1
FILE_NAME_LAST_INDEX = -4


def first_pass(input_file):
    """
    Scan the entire file for labels, e.g (xxx), add the pair (xxx, address) to
    the symbols table, where address is the number of the instruction
    following (xxx)
    :param input_file: file to translate to Hack binary code
    :return: None
    """
    i = 0  # set counter for line instructions
    for ln in input_file:
        ln = ln.strip()
        if not Parse.ignore_line(ln) and not ln.startswith("("):
            i += 1  # counter for label symbols value
        key = ln[1:-1]  # remove bracket from label
        if ln.startswith("("):
            Code_tables.symbols_table[key] = i


def main(file):
    """
    The main function that drive the program.
    First we do first pass to add labels to the pre-defined symbols table, then
    we do second pass and translate A and C instructions
    :param file: file to translate to Hack binary code
    :return: None
    """
    if os.path.isdir(file):
        for filename in os.listdir(file):
            if filename.endswith(".asm"):
                translate_file(file + "/" + filename)
    else:
        translate_file(file)


def translate_file(file):
    """
    Translate file to hack binary code
    :param file: file to translate to Hack binary code
    :return: None
    """
    input_file = open(file, "r")
    # change extension to .hack
    output_file = open(file[:FILE_NAME_LAST_INDEX] + ".hack", "w")
    first_pass(input_file)  # first pass
    input_file.seek(0)
    for ln in input_file:  # second pass
        line = ln.strip()
        if not Parse.ignore_line(line) and not line.startswith("("):
            in_binary = Parse.parse_line(line)
            output_file.write(in_binary + '\n')
    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main(sys.argv[FILE_ARG_INDEX])
