##########################################################
# file : JackAnalyzer.py
# writer : Nadav vitri , nadav.vitri , 203819909
#          Arie shtine, arie.shtine, 204616122
# EXERCISE : nand2tetris ex10 2017-2018
# DESCRIPTION: This program translate jack file to XML
##########################################################

############################################################
# Imports
############################################################
import sys
import os
import CompilationEngine as ce
import JackTokenizer as jt

############################################################
# Constants
############################################################
FILE_ARG_INDEX = 1
FILE_NAME_LAST_INDEX = -5
NO_COMMENT_FOUND = -1

IN_COMMENT = False
IN_COMMENT_2_BACK_SLASHES = False
IN_STRING = False


def first_pass(file):
    global IN_COMMENT
    global IN_COMMENT_2_BACK_SLASHES
    global IN_STRING
    new_file = ""
    for ln in file:
        i = 0
        while i < len(ln):
            if ln[i] == '\"':
                IN_STRING = not IN_STRING
            elif not IN_STRING and not IN_COMMENT and (i + 2 < len(ln) and ln[i:i + 2] == '//'):
                IN_COMMENT_2_BACK_SLASHES = True
            elif not IN_STRING and (i + 2 < len(ln) and ln[i:i + 2] == '/*'):
                IN_COMMENT = True
                i += 2
            elif not IN_STRING and (i + 2 < len(ln) and ln[i:i + 2] == '*/'):
                IN_COMMENT = False
                i += 2
            if not IN_COMMENT and not IN_COMMENT_2_BACK_SLASHES:
                new_file += ln[i]
                if ln[i] == ';':
                    new_file += '\n'
            i += 1
        IN_COMMENT_2_BACK_SLASHES = False
    return new_file


def main(file):
    """
    The main function that drive the program.
    Reads the vm file line by line and if line is needed to be translate
    (and not to ignore the line), then send the line to parse and gets the line
    translate to assembly code
    :param file: jack file to be translated
    :return: None
    """
    if os.path.isdir(file):
        for filename in os.listdir(file):
            if filename.endswith(".jack"):
                translate_jack_file(file + os.sep + filename)
                ce.index = 0   # restart index counter to zero
    else:
        translate_jack_file(file)


def translate_jack_file(file):
    """
    translate only one vm file to asm file
    :param file: name of file
    :return: None
    """
    input_file = open(file, "r")
    output_file = open(file[:FILE_NAME_LAST_INDEX] + ".xml", "w")
    # remove comments from file
    clean_file = first_pass(input_file)
    # file to list of tokens
    tokenized = jt.file_to_tokens(clean_file)
    translated = ce.translate_token(tokenized)
    output_file.write(translated)
    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main(sys.argv[FILE_ARG_INDEX])
