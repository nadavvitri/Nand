##########################################################
# file : VMtranslator.py
# writer : Nadav vitri , nadav.vitri , 203819909
#          Arie shtine, arie.shtine, 204616122
# EXERCISE : nand2tetris ex8 2017-2018
# DESCRIPTION: This program translate vm file to asm file
##########################################################

############################################################
# Imports
############################################################
import sys
import os
import Parse
import Translator
from os import path

############################################################
# Constants
############################################################
FILE_ARG_INDEX = 1
FILE_NAME_LAST_INDEX = -3


def main(file):
    """
    The main function that drive the program.
    Reads the vm file line by line and if line is needed to be translate
    (and not to ignore the line), then send the line to parse and gets the line
    translate to assembly code
    :param file: vm file to be translated
    :return: None
    """
    if os.path.isdir(file):
        dict_name = file.split(os.sep)[-1]
        output_file = open(file + os.sep + dict_name + ".asm", "w")
        output_file.write(Translator.write_init())
        for filename in os.listdir(file):
            if filename.endswith(".vm"):
                translate_directory(filename, file, output_file)
        output_file.close()

    else:
        translate_vm_file(file)


def translate_directory(filename, root, output_file):
    """
    translate all vm files in directory to one asm file.
    :param filename: name of file
    :param root: path
    :param output_file: translated vm to asm file
    :return: None
    """
    input_file = open(root + os.sep + filename, "r")
    for ln in input_file:
        line = ln.strip()
        if not Parse.ignore_line(line):  # check if we ignore line or not
            translated = Parse.parse_line(line, filename)
            output_file.write(translated)
    input_file.close()


def translate_vm_file(file):
    """
    translate onlt one vm file to asm file
    :param file: name of file
    :return: None
    """
    input_file = open(file, "r")
    file_name = path.basename(input_file.name)[:FILE_NAME_LAST_INDEX]
    output_file = open(file[:FILE_NAME_LAST_INDEX] + ".asm", "w")
    output_file.write(Translator.write_init())
    for ln in input_file:
        line = ln.strip()
        if not Parse.ignore_line(line):  # check if we ignore line or not
            translated = Parse.parse_line(line, file_name)
            output_file.write(translated)
    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main(sys.argv[FILE_ARG_INDEX])
