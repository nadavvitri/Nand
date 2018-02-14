############################################################
# Constants
############################################################
OTHER_SEGMENTS = ["local", "argument", "this", "that"]
LINE_BREAK = '\n'
SP = "@SP" + LINE_BREAK
SP_D = SP + "A=M" + LINE_BREAK + "M=D" + LINE_BREAK
SP_PLUS_ONE = SP + "M=M+1" + LINE_BREAK
SP_MINUS_ONE = SP + "M=M-1" + LINE_BREAK
STACK_POP = SP_MINUS_ONE + "A=M" + LINE_BREAK + "D=M" + LINE_BREAK
LCL = "@LCL" + LINE_BREAK
ARG = "@ARG" + LINE_BREAK
THIS = "@THIS" + LINE_BREAK
THAT = "@THAT" + LINE_BREAK
BASE_TEMP_SEGMENT = 5
EQUAL = "eq"
GREATER = "gt"

############################################################
# Globals
############################################################
label_number = 1
current_function = ""


def constant(number):
    """
    D = const
    *SP = D
    SP++
    :param number: constant[number]
    :return: line in asm code
    """
    translated = "@" + number + LINE_BREAK + \
                 "D=A" + LINE_BREAK + \
                 SP_D + \
                 SP_PLUS_ONE
    return translated


def pop_static(number, file_name):
    """
    D = STACK_POP
    @filename.number
    M = D
    :param number: static[number]
    :param file_name: the name of the vm file
    :return: line in asm code
    """
    translated = STACK_POP + \
                 "@" + file_name + "." + number + LINE_BREAK +\
                 "M=D" + LINE_BREAK
    return translated


def push_static(number, file_name):
    """
    D = STACK_POP
    @filename.number
    M = D
    :param number: static[number]
    :param file_name: the name of the vm file
    :return: line in asm code
    """
    translated = "@" + file_name + "." + number + LINE_BREAK + \
                 "D=M" + LINE_BREAK + \
                 SP_D +\
                 SP_PLUS_ONE
    return translated


def push_temp(number):
    """
    address = 5 + i
    *SP = *address
    SP++
    :param number: temp[number]
    :return: line in asm code
    """
    cell = BASE_TEMP_SEGMENT + int(number)
    translated = "@R" + str(cell) + LINE_BREAK + \
                 "D=M" + LINE_BREAK + \
                 SP_D + \
                 SP_PLUS_ONE
    return translated


def pop_temp(number):
    """
    D = i + *R5
    address = D
    D = STACK_POP
    *address = D
    :param number: pop stack[number]
    :return: line in asm code
    """
    translated = "@R5" + LINE_BREAK + \
                 "D=A" + LINE_BREAK + \
                 "@" + str(number) + LINE_BREAK +\
                 "D=D+A" + LINE_BREAK + \
                 "@address" + LINE_BREAK + \
                 "M=D" + LINE_BREAK +\
                 STACK_POP + \
                 "@address" + LINE_BREAK +\
                 "A=M" + LINE_BREAK + \
                 "M=D" + LINE_BREAK
    return translated


def segment_pointers(segment):
    """
    local, argument, this and that are implemented the same way, just we need
    to choose the "@" + segment
    :param segment: local/argument/this/that
    :return: "@segment\n"
    """
    if segment == OTHER_SEGMENTS[0]:
        return LCL
    elif segment == OTHER_SEGMENTS[1]:
        return ARG
    elif segment == OTHER_SEGMENTS[2]:
        return THIS
    else:
        return THAT


def push_other_segments(segment, number):
    """
    address = segment + i
    *SP = *address
    SP++
    :param segment: segment type
    :param number: segment[number]
    :return: line in asm code
    """
    translated = segment_pointers(segment) + \
                 "D=M" + LINE_BREAK + \
                 "@" + number + LINE_BREAK + \
                 "A=D+A" + LINE_BREAK + \
                 "D=M" + LINE_BREAK + \
                 SP_D + \
                 SP_PLUS_ONE
    return translated


def pop_other_segments(segment, number):
    """
    D = i + *segment
    address = D
    D = STACK_POP
    *address = D
    :param segment: segment type
    :param number: pop stack[number]
    :return: line in asm code
    """
    translated = segment_pointers(segment) + \
                 "D=M" + LINE_BREAK + \
                 "@" + number + LINE_BREAK + \
                 "D=D+A" + LINE_BREAK +\
                 "@address" + LINE_BREAK + \
                 "M=D" + LINE_BREAK + \
                 STACK_POP +\
                 "@address" + LINE_BREAK + \
                 "A=M" + LINE_BREAK + \
                 "M=D" + LINE_BREAK
    return translated


def this_or_that(number):
    """
    Supplies THIS or THAT for pointer segment
    :param number: 0 or 1
    :return: "@THIS\n" if 0, else "@THAT\n"
    """
    if int(number) == 0:
        return THIS
    return THAT


def push_pointer(number):
    """
    *SP = THIS/THAT
    SP++
    :param number: 0 or 1
    :return: line in asm code
    """
    cell = this_or_that(number)
    translated = cell + \
                 "D=M" + LINE_BREAK + \
                 SP_D + \
                 SP_PLUS_ONE
    return translated


def pop_pointer(number):
    """
    D = STACK_POP
    *THIS/THAT = D
    :param number: 0 or 1
    :return: line in asm code
    """
    cell = this_or_that(number)
    translated = cell + \
                 "D=A" + LINE_BREAK + \
                 "@address" + LINE_BREAK + \
                 "M=D" + LINE_BREAK + \
                 STACK_POP + \
                 "@address" + LINE_BREAK + \
                 "A=M" + LINE_BREAK + \
                 "M=D" + LINE_BREAK
    return translated


def add():
    """
    SP--
    D = *SP
    A = *SP--
    D = M + D
    *SP = D
    :return: line in asm code
    """
    translated = SP_MINUS_ONE + \
                 "A=M" + LINE_BREAK + \
                 "D=M" + LINE_BREAK + \
                 "A=A-1" + LINE_BREAK + \
                 "M=D+M" + LINE_BREAK
    return translated


def sub():
    """
    SP--
    D = *SP
    A = *SP--
    D = M - D
    *SP = D
    :return: line in asm code
    """
    translated = SP_MINUS_ONE + \
                 "A=M" + LINE_BREAK + \
                 "D=M" + LINE_BREAK + \
                 "A=A-1" + LINE_BREAK + \
                 "M=M-D" + LINE_BREAK
    return translated


def neg():
    """
    A = SP--
    M = -M
    :return: line in asm code
    """
    translated = SP + \
                 "A=M-1" + LINE_BREAK + \
                 "M=-M" + LINE_BREAK
    return translated


def logic_and():
    """
    D = STACK_POP
    A = SP--
    D = D & M
    M = D
    :return: line in asm code
    """
    translated = STACK_POP + \
                 "A=A-1" + LINE_BREAK + \
                 "M=M&D" + LINE_BREAK
    return translated


def logic_or():
    """
    D = STACK_POP
    A = SP--
    D = D | M
    M = D
    :return: line in asm code
    """
    translated = STACK_POP + \
                 "A=A-1" + LINE_BREAK + \
                 "M=M|D" + LINE_BREAK
    return translated


def logic_not():
    """
    A = SP--
    M = !M
    :return: line in asm code
    """
    translated = SP + \
                 "A=M-1" + LINE_BREAK + \
                 "M=!M" + LINE_BREAK
    return translated


def equal_greater_smaller(command):
    """
    In generally, there is 2 unique labels, each for true or false (the sub of
    the two recent element from the stack equals/greater/smaller)
    :param command: eq/lg/gt
    :return: line in asm code
    """
    global label_number
    if command == EQUAL:
        jump_effect = "JNE"
    elif command == GREATER:
        jump_effect = "JLE"
    else:
        jump_effect = "JGE"
    global label_number
    part1 = SP_MINUS_ONE + \
            "A=M" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@Ynegative" + str(label_number) + LINE_BREAK + \
            "D;JLT" + LINE_BREAK + \
            SP + \
            "A=M-1" + LINE_BREAK + \
            "D=M" + LINE_BREAK
    y_negative = "(Ynegative" + str(label_number) + ")"
    label_number += 1
    part2 = "@XnegativeYpositive" + str(label_number) + LINE_BREAK + \
            "D;JLT" + LINE_BREAK + \
            SP + \
            "A=M" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "A=A-1" + LINE_BREAK + \
            "D=M-D" + LINE_BREAK
    x_negative_y_positive = "(XnegativeYpositive" + str(label_number) + ")"
    label_number += 1
    part3 = "@False" + str(label_number) + LINE_BREAK + \
            "D;" + jump_effect + LINE_BREAK + \
            SP + \
            "A=M" + LINE_BREAK + \
            "A=A-1" + LINE_BREAK + \
            "M=-1" + LINE_BREAK
    false_label_1 = "(False" + str(label_number) + ")"
    label_number += 1
    part4 = "@End" + str(label_number) + LINE_BREAK + \
            "0;JMP" + LINE_BREAK +\
            false_label_1 + LINE_BREAK + \
            SP + \
            "A=M" + LINE_BREAK + \
            "A=A-1" + LINE_BREAK + \
            "M=0" + LINE_BREAK + \
            "@End" + str(label_number) + LINE_BREAK + \
            "0;JMP" + LINE_BREAK
    end_exit_label = "End" + str(label_number)
    label_number += 1
    part5 = y_negative + LINE_BREAK + \
            SP + \
            "A=M-1" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@YnegativeAndXpositive" + str(label_number) + LINE_BREAK + \
            "D;JGT" + LINE_BREAK + \
            SP + \
            "A=M" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "A=A-1" + LINE_BREAK + \
            "D=M-D" + LINE_BREAK
    y_negative_x_positive = "(YnegativeAndXpositive" + str(label_number) + ")"
    label_number += 1
    part6 = "@False" + str(label_number) + LINE_BREAK + \
            "D;" + jump_effect + LINE_BREAK + \
            SP + \
            "A=M" + LINE_BREAK + \
            "A=A-1" + LINE_BREAK + \
            "M=-1" + LINE_BREAK + \
            "@" + end_exit_label + LINE_BREAK + \
            "0;JMP" + LINE_BREAK
    false_label_2 = "(False" + str(label_number) + ")"
    label_number += 1
    part7 = false_label_2 + LINE_BREAK + \
                SP + \
                "A=M" + LINE_BREAK + \
                "A=A-1" + LINE_BREAK + \
                "M=0" + LINE_BREAK + \
                "@" + end_exit_label + LINE_BREAK + \
                "0;JMP" + LINE_BREAK
    part8 = x_negative_y_positive + LINE_BREAK
    if (command == "gt" or command == "eq"):
        part8 += SP + \
                "A=M" + LINE_BREAK + \
                "A=A-1" + LINE_BREAK + \
                "M=0" + LINE_BREAK + \
                "@" + end_exit_label + LINE_BREAK + \
                "0;JMP" + LINE_BREAK
    else:
        part8 += SP + \
            "A=M" + LINE_BREAK + \
            "A=A-1" + LINE_BREAK + \
            "M=-1" + LINE_BREAK + \
            "@" + end_exit_label + LINE_BREAK + \
            "0;JMP" + LINE_BREAK
    part9 = y_negative_x_positive + LINE_BREAK
    if (command == "lt" or command == "eq"):
        part9 += SP + \
                 "A=M" + LINE_BREAK + \
                 "A=A-1" + LINE_BREAK + \
                 "M=0" + LINE_BREAK + \
                 "@" + end_exit_label + LINE_BREAK + \
                 "0;JMP" + LINE_BREAK
    else:
        part9 += SP + \
                 "A=M" + LINE_BREAK + \
                 "A=A-1" + LINE_BREAK + \
                 "M=-1" + LINE_BREAK + \
                 "@" + end_exit_label + LINE_BREAK + \
                 "0;JMP" + LINE_BREAK
    return part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + \
           part9 + "(" + end_exit_label + ")" + LINE_BREAK


def arithmetic_logical_command(command):
    """
    This function manage the command to the matching arithmetic operation
    :param command: add/sub/neg/and/or/not/eq/lg/gt
    :return: line in asm code
    """
    if command == "add":
        return add()
    elif command == "sub":
        return sub()
    elif command == "neg":
        return neg()
    elif command == "and":
        return logic_and()
    elif command == "or":
        return logic_or()
    elif command == "not":
        return logic_not()
    else:
        return equal_greater_smaller(command)


def write_init():
    init_code = "@256" + LINE_BREAK + \
                "D=A" + LINE_BREAK + \
                SP + \
                "M=D" + LINE_BREAK
    return init_code + write_call("Sys.init", "0")


def write_label(label_name):
    global current_function
    label = "(" + label_name + "." + current_function + ")" + LINE_BREAK
    return label


def write_goto(label_name):
    global current_function
    jump = "@" + label_name + "." + current_function + LINE_BREAK + \
           "0;JMP" + LINE_BREAK
    return jump


def write_if(label_name):
    global current_function
    if_goto = SP_MINUS_ONE + \
              "A=M" + LINE_BREAK + \
              "D=M" + LINE_BREAK + \
              "@" + label_name + "." + current_function + LINE_BREAK + \
              "D;JNE" + LINE_BREAK
    return if_goto


def write_function(function_name, num_vars):
    push_zero = "(" + function_name + "." + ")" + LINE_BREAK
    global current_function
    current_function = function_name
    for i in range(int(num_vars)):
        push_zero += SP + \
                    "A=M" + LINE_BREAK + \
                    "M=0" + LINE_BREAK + \
                    SP_PLUS_ONE
    return push_zero


def write_call(function_name, num_vars):
    global label_number
    call = "@returnAddr" + str(label_number) + LINE_BREAK + \
            "D=A" + LINE_BREAK + \
            SP + \
            "A=M" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            SP_PLUS_ONE + \
           "@LCL" + LINE_BREAK + \
           "D=M" + LINE_BREAK + \
           SP + \
           "A=M" + LINE_BREAK + \
           "M=D" + LINE_BREAK + \
           SP_PLUS_ONE + \
            "@ARG" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            SP + \
            "A=M" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            SP_PLUS_ONE + \
            "@THIS" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            SP + \
           "A=M" + LINE_BREAK + \
           "M=D" + LINE_BREAK + \
            SP_PLUS_ONE + \
            "@THAT" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            SP + \
           "A=M" + LINE_BREAK + \
           "M=D" + LINE_BREAK + \
            SP_PLUS_ONE + \
            SP + \
            "D=M" + LINE_BREAK + \
            "@" + str(int(num_vars) + int(5)) + LINE_BREAK + \
            "D=D-A" + LINE_BREAK + \
            "@ARG" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            SP + \
            "D=M" + LINE_BREAK + \
            "@LCL" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            "@" + function_name + "." + LINE_BREAK + \
            "0;JMP" + LINE_BREAK + \
            "(returnAddr" + str(label_number) + ")" + LINE_BREAK
    label_number += 1
    return call


def write_return():
    ret = "@LCL" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@endFrame" + LINE_BREAK + \
            "MD=D" + LINE_BREAK + \
            "@5" + LINE_BREAK + \
            "A=D-A" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@retAddr" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            SP + \
            "M=M-1" + LINE_BREAK + \
            SP + \
            "A=M" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@ARG" + LINE_BREAK + \
            "A=M" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            "@ARG" + LINE_BREAK + \
            "D=M+1" + LINE_BREAK + \
            SP + \
            "M=D" + LINE_BREAK + \
            "@endFrame" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@1" + LINE_BREAK + \
            "A=D-A" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@THAT" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            "@endFrame" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@2" + LINE_BREAK + \
            "A=D-A" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@THIS" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            "@endFrame" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@3" + LINE_BREAK + \
            "A=D-A" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@ARG" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            "@endFrame" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@4" + LINE_BREAK + \
            "A=D-A" + LINE_BREAK + \
            "D=M" + LINE_BREAK + \
            "@LCL" + LINE_BREAK + \
            "M=D" + LINE_BREAK + \
            "@retAddr" + LINE_BREAK + \
            "A=M" + LINE_BREAK + \
            "0;JMP" + LINE_BREAK
    return ret

