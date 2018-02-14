############################################################
# Imports
############################################################
import Translator

############################################################
# Constants
############################################################
NO_COMMENT_FOUND = -1
C_PUSH = "push"
C_POP = "pop"
CONSTANT = "constant"
STATIC = "static"
TEMP = "temp"
POINTER = "pointer"


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
    return False


def check_comment_in_line(ln):
    """
    Gets line and remove comments if there is (e.g "// bla bla")
    :param ln: line we need to translate
    :return: clean line without comments
    """
    index = ln.find('/')  # if there is comment in the end of line
    line = ln[:index]
    if index == NO_COMMENT_FOUND:  # simple line without comment at the end
        line = ln.strip()
    return line


def parse_line(ln, file_name):
    """
    Parse line and check if the line is arithmetic/logical operation or memory
    access operation and send respectively to the appropriate function
    to translate
    :param ln: line from vm file to translate
    :param file_name: the name of the vm file
    :return: line translate to asm commands
    """
    line = check_comment_in_line(ln)
    parsed = line.split()
    command = parsed[0]
    if command == C_POP or command == C_PUSH:   # memory access operation
        return memory_access_command(parsed, file_name)
    elif command == "label":
        return Translator.write_label(parsed[1])
    elif command == "goto":
        return Translator.write_goto(parsed[1])
    elif command == "if-goto":
        return Translator.write_if(parsed[1])
    elif command == "function":
        return Translator.write_function(parsed[1], parsed[2])
    elif command == "call":
        return Translator.write_call(parsed[1], parsed[2])
    elif command == "return":
        return Translator.write_return()
    else:   # arithmetic/logical operation
        return Translator.arithmetic_logical_command(command)


def memory_access_command(parsed_line, file_name):
    """
    Send the line to the matching function to translate, according to the
    memory segment wrote in the line
    :param parsed_line: memory access operation - push/pop + segment + i
    :param file_name: the name of the vm file
    :return:
    """
    command = parsed_line[0]
    segment = parsed_line[1]
    number = parsed_line[2]
    if segment == CONSTANT:
        return Translator.constant(number)
    elif segment == STATIC:
        if command == C_PUSH:
            return Translator.push_static(number, file_name)
        return Translator.pop_static(number, file_name)
    elif segment == TEMP:
        if command == C_PUSH:
            return Translator.push_temp(number)
        return Translator.pop_temp(number)
    elif segment == POINTER:
        if command == C_PUSH:
            return Translator.push_pointer(number)
        return Translator.pop_pointer(number)
    else:
        if command == C_PUSH:
            return Translator.push_other_segments(segment, number)
        return Translator.pop_other_segments(segment, number)
