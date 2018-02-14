############################################################
# Imports
############################################################
import Code_tables

############################################################
# Constants
############################################################
START_CODE_C_INST = "111"
START_SHIFT_CODE = "1"
NO_COMMENT_FOUND = -1
INITIAL_VAR_POS = 16

############################################################
# Globals
############################################################
pos_in_memory = INITIAL_VAR_POS


def ignore_line(ln):
    """
    Check if we ignore this line (// or empty line) or not
    :param ln: line to check
    :return: True if we need to ignore line, else False
    """
    if not ln:
        return True
    if ln.startswith("//"):
        return True
    else:
        return False


def parse_line(ln):
    """
    Gets line and remove comments if there is, then check if this A or C
    instruction and send to other function that translate them
    :param ln: line we need to translate
    :return: line in Hack binary code
    """
    index = ln.find('/')   # if there is comment in the end of line
    line = ln[:index]
    if index == NO_COMMENT_FOUND:  # simple line without comment at the end
        line = ln.strip()
    if ln.startswith("@"):  # the line is A instruction
        return "0" + translate_a_instruction(line)
    else:   # else, the line is C instruction
        return translate_c_instruction(line)


def number_to_binary(num):
    """
    Convert number to binary representation of 15 digit in binary
    :param num: number to convert
    :return: number in binary representation
    """
    return '{0:015b}'.format(int(num))


def translate_a_instruction(ln):
    """
    Parse A instruction to op code (0) and convert the number to binary
    :param ln: line with A instruction
    :return: line in Hack binary code
    """
    global pos_in_memory
    # remove @ from A instruction give the variable name
    variable_name = ln[1:]
    #  simple number for A instruction
    if variable_name.isdigit():
        return number_to_binary(variable_name)
    # if the variable exist in the symbols table
    if variable_name not in Code_tables.symbols_table:
        Code_tables.symbols_table[variable_name] = pos_in_memory
        pos_in_memory += 1  # next free memory position
    return number_to_binary(Code_tables.symbols_table[variable_name])


def translate_c_instruction(ln):
    """
    Parse C instruction to dest, comp and jump parts and translate every part
    to Hack binary code. We adding to start of C instruction "111" according
    to the Hack machine language
    :param ln: line with C instruction
    :return: whole line in Hack binary code
    """
    ln = ln.replace(" ", "")
    dest = None
    jmp = None
    if "=" in ln:
        dest, comp = ln.split("=")
        if ";" in comp:
            comp, jmp = comp.split(";")
    else:
        comp, jmp = ln.split(";")
    rest_of_line = Code_tables.parse_dest(dest) + Code_tables.parse_jmp(jmp)
    if ">" in ln or "<" in ln:
        start_of_line = START_SHIFT_CODE + Code_tables.parse_shift(comp)
    else:
        start_of_line = START_CODE_C_INST + Code_tables.parse_comp(comp)
    return start_of_line + rest_of_line