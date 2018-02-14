############################################################
# Imports
############################################################
import JackTokenizer as jt
import SymbolTable as st
import VMWriter as vm
############################################################
# Globals
############################################################
keyword = ["class", "constructor", "function", "method", "field", "static",
           "var", "int", "char", "boolean", "void", "true", "false", "null",
           "this", "let", "do", "if", "else", "while", "return"]

symbol = ['{', '}', '(', ')', ']', '[', '.', ',', ';', '+', '-', '*', '/', '&',
          '|', '<', '>', '=', '~']

keyword_constant = ['true', 'false', 'null', 'this']
in_method_flag = False
op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
WHILE_COUNTER, IF_COUNTER = 0, 0
index = 0
vars_table = st.SymbolTable()
output_file = vm.VMWriter(None, None)


def check_type(var_type):
    if var_type in keyword:
        return jt.write_keyword(var_type)
    return jt.write_identifier(var_type)


def translate_token(tokenized, root):
    global index, output_file
    vars_table.restart_table()
    output_file = vm.VMWriter(root, tokenized[1])
    index += 1
    # class_name = tokenized[index]  # name
    index += 1
    index += 1
    inside_class(tokenized)


def inside_class(tokenized):
    global index, vars_table, in_method_flag
    if tokenized[index] == "}":
        return
    if tokenized[index] == "static" or tokenized[index] == "field":
        compile_class_var_dec(tokenized)
        inside_class(tokenized)
    elif tokenized[index] == "function" or tokenized[index] == "method" or tokenized[index] == "constructor" or \
                    tokenized[index] == "Constructor":
        vars_table.start_subroutine()
        compile_subroutine_dec(tokenized)
        in_method_flag = False
        inside_class(tokenized)


def compile_class_var_dec(tokenized):
    global index, vars_table
    kind = tokenized[index]  # field / static
    index += 1
    var_type = tokenized[index]   # type
    index += 1
    var_name = tokenized[index]  # varName
    index += 1
    vars_table.define(var_name, var_type, kind)
    while tokenized[index] != ";":
        index += 1
        var_name = tokenized[index]
        vars_table.define(var_name, var_type, kind)
        index += 1
    index += 1


def compile_subroutine_dec(tokenized):
    global index, in_method_flag
    function_or_method = tokenized[index]  # eg function
    index += 1
    func_type = tokenized[index]
    index += 1
    name = tokenized[index]
    index += 1
    index += 1
    if tokenized[index] == ")":
            compile_subroutine_body(tokenized, function_or_method, func_type, name)
    else:
        if function_or_method == "method":
            in_method_flag = True
            vars_table.define("this", tokenized[1], "argument")
        compile_params_list(tokenized)
        compile_subroutine_body(tokenized, function_or_method, func_type, name)
    index += 1


def compile_params_list(tokenized):
    global index, vars_table
    arg_type = tokenized[index]
    index += 1
    arg_name = tokenized[index]
    index += 1
    vars_table.define(arg_name, arg_type, "argument")
    if tokenized[index] == ",":
        # translated += jt.write_symbol(tokenized[index])
        index += 1
        compile_params_list(tokenized)


def compile_subroutine_body(tokenized, function, func_type, name):
    global index, vars_table, in_method_flag
    index += 1
    index += 1
    while tokenized[index] == "var":
        compile_var_dec(tokenized)
    if function == "function":  # TODO nested classes to do linked list
        output_file.write_function(name, vars_table.var_count("local"))
    elif function == "method":   # TODO nested classes to do linked list
        in_method_flag = True
        output_file.write_function(name, vars_table.var_count("local"))
        output_file.write_push("argument", "0")
        output_file.write_pop("pointer", 0)
    elif function == "constructor" or function == "Constructor":
        output_file.write_function(name, vars_table.var_count("local"))
        output_file.write_push("constant", vars_table.var_count("this"))
        output_file.write_call("Memory.alloc", 1)
        output_file.write_pop("pointer", 0)
    while tokenized[index] != "return":
        if tokenized[index] != '}':
            # statements += compile_statement(tokenized)
            compile_statement(tokenized)
        else:
            return
    compile_statement(tokenized)


def compile_many_vars_dec(tokenized, var_type, kind):
    global index, vars_table
    index += 1
    var_name = tokenized[index]  # var_name
    index += 1
    vars_table.define(var_name, var_type, kind)
    while tokenized[index] != ";":
        index += 1
        var_name = tokenized[index]  # var_name
        vars_table.define(var_name, var_type, kind)
        index += 1


def compile_var_dec(tokenized):
    global index, vars_table
    kind = "local"  # TODO check
    index += 1
    var_type = tokenized[index]
    index += 1
    var_name = tokenized[index]
    index += 1
    vars_table.define(var_name, var_type, kind)
    if tokenized[index] == ",":
        compile_many_vars_dec(tokenized, var_type, kind)
    index += 1


def compile_statement(tokenized):
    global index
    if tokenized[index] == "}":
        return
    if tokenized[index] == "if":
        compile_if_statement(tokenized)
    elif tokenized[index] == "let":
        compile_let_statement(tokenized)
    elif tokenized[index] == "while":
        compile_while_statement(tokenized)
    elif tokenized[index] == "do":
        compile_do_statement(tokenized)
    elif tokenized[index] == "return":
        compile_return_statement(tokenized)
    else:
        compile_statement(tokenized)


def compile_else(tokenized):
    global index
    # translated = jt.write_keyword(tokenized[index])   # else
    index += 1
    # translated += jt.write_symbol(tokenized[index])   # {
    index += 1
    while tokenized[index] != "}":
        compile_statement(tokenized)


def compile_expression(tokenized):
    global index
    if tokenized[index] == ")":
        return
    elif tokenized[index].isdigit():
        output_file.write_push("constant", tokenized[index])
        index += 1
    elif '"' in tokenized[index]:  # "
        temp_str = tokenized[index][1:-1]
        output_file.write_push("constant", len(temp_str))
        output_file.write_call("String.new", 1)
        for c in temp_str:
            output_file.write_push("constant", ord(c))
            output_file.write_call("String.appendChar", 2)
        index += 1
    elif tokenized[index] in keyword_constant:
        keyword = tokenized[index]
        if keyword == "true":
            output_file.write_push("constant", 0)
            output_file.write_arithmetic("not")
        elif keyword == "false" or keyword == "null":
            output_file.write_push("constant", 0)
        elif keyword == "this":
            output_file.write_push("pointer", 0)
        index += 1
    elif tokenized[index] == "(":
        index += 1
        compile_expression(tokenized)
        index += 1
    elif tokenized[index] == '-' or tokenized[index] == '~':
        log_command = tokenized[index]
        index += 1
        # TODO make chang from here
        if tokenized[index] == "(":
            index += 1
            compile_expression(tokenized)
            index += 1
        else:
            compile_expression(tokenized)
        # TODO to here
        # compile_expression(tokenized)
        if log_command == '~':
            output_file.write_arithmetic("not")
        else:
            output_file.write_arithmetic("neg")
    else:
        name = tokenized[index]   # var
        index += 1
        if tokenized[index] == "[":  # arry
            # translated += jt.write_symbol(tokenized[index]) + "<expression>\n"  # [
            index += 1
            # translated += compile_expression(tokenized) + "</expression>\n" + jt.write_symbol(tokenized[index])
            compile_expression(tokenized)
            output_file.write_push(vars_table.kind_of(name), vars_table.index_of(name))
            output_file.write_arithmetic("add")
            output_file.write_pop("pointer", "1")
            output_file.write_push("that", "0")
            index += 1
        elif tokenized[index] == "(" or tokenized[index] == ".":  # subroutine call
            compile_subroutine_call_sec(tokenized, name)  # . or (
        else:
            output_file.write_push(vars_table.kind_of(name), vars_table.index_of(name))
    while tokenized[index] in op:   # eg x | y
        if tokenized[index] == '+':
            index += 1
            compile_expression(tokenized)
            output_file.write_arithmetic("add")
        elif tokenized[index] == '-':
            index += 1
            compile_expression(tokenized)
            output_file.write_arithmetic("sub")
        elif tokenized[index] == '*':
            index += 1
            compile_expression(tokenized)
            output_file.write_call("*", 2)  # op
        elif tokenized[index] == '/':
            index += 1
            compile_expression(tokenized)
            output_file.write_call("/", 2)  # op
        elif tokenized[index] == '>':
            index += 1
            compile_expression(tokenized)
            output_file.write_arithmetic("gt")
        elif tokenized[index] == '<':
            index += 1
            compile_expression(tokenized)
            output_file.write_arithmetic("lt")
        elif tokenized[index] == '=':
            index += 1
            compile_expression(tokenized)
            output_file.write_arithmetic("eq")
        elif tokenized[index] == '&':
            index += 1
            compile_expression(tokenized)
            output_file.write_arithmetic("and")
        elif tokenized[index] == '|':
            index += 1
            compile_expression(tokenized)
            output_file.write_arithmetic("or")
    # return translated


def compile_expression_list(tokenized, name, flag):
    global index
    counter = 1
    sign = tokenized[index]
    if sign == ")" and not flag:  # no expression at all
        counter = 0
    compile_expression(tokenized)
    while tokenized[index] == ",":
        index += 1
        counter += 1
        compile_expression(tokenized)
    if not flag and "." not in name:
        name = tokenized[1] + "." + name
        counter += 1
    if counter >= 1 and sign != ")" and flag:
        counter += 1
    output_file.write_call(name, counter)


def compile_subroutine_call(tokenized):
    global index
    flag = False
    name = tokenized[index]  # subroutineName | className | varName
    if vars_table.kind_of(name):
        flag = True
        output_file.write_push(vars_table.kind_of(name), vars_table.index_of(name))
        name = vars_table.type_of(name)
    index += 1
    if tokenized[index] == ".":
        name += tokenized[index]  # .
        index += 1
        name += tokenized[index]  # name in class
        index += 1
    # translated += jt.write_symbol(tokenized[index])   # (
    elif tokenized[index] == "(":
        output_file.write_push("pointer", "0")
        if vars_table.kind_of(name) is None:  # TODO check if not crush other jack files
            name = tokenized[1] + "." + name
        else:
            name = vars_table.type_of(name) + "." + name
        flag = True
    index += 1
    compile_expression_list(tokenized, name, flag)
    index += 1


def compile_subroutine_call_sec(tokenized, name):
    global index, in_method_flag
    flag = False
    if tokenized[index] == ".":
        if vars_table.kind_of(name) is not None:
            output_file.write_push("this", vars_table.index_of(name))
            flag = True
            name = vars_table.type_of(name)
        name += tokenized[index]  # .
        index += 1
        name += tokenized[index]  # method name
        index += 1
    elif tokenized[index] == "(" and in_method_flag:
        output_file.write_push("pointer", 0)
    # translated += jt.write_symbol(tokenized[index])   # (
    index += 1
    compile_expression_list(tokenized, name, flag)
    index += 1


def compile_if_statement(tokenized):
    global index, IF_COUNTER
    IF_COUNTER += 1
    index += 1
    index += 1
    compile_expression(tokenized)
    index += 1
    index += 1
    output_file.write_if("IF_TRUE" + str(IF_COUNTER))
    output_file.write_goto("IF_FALSE" + str(IF_COUNTER))
    output_file.write_label("IF_TRUE" + str(IF_COUNTER))
    last = str(IF_COUNTER)
    while tokenized[index] != "}":
        compile_statement(tokenized)
    index += 1
    # output_file.write_goto("IF_END" + last)
    if tokenized[index] == "else":
        output_file.write_goto("IF_END" + last)
        output_file.write_label("IF_FALSE" + last)
        # IF_COUNTER += 1
        compile_else(tokenized)
        output_file.write_label("IF_END" + last)
        index += 1
    else:
        # IF_COUNTER += 1
        output_file.write_label("IF_FALSE" + last)
    # output_file.write_label("IF_END" + last)


def compile_let_statement(tokenized):
    global index, vars_table
    translated = ""
    index += 1
    var_name = tokenized[index]  # varName
    index += 1
    if tokenized[index] == "[":
        # TODO handle this case
        # translated += jt.write_symbol(tokenized[index])
        index += 1
        compile_expression(tokenized)
        index += 1
        output_file.write_push(vars_table.kind_of(var_name), vars_table.index_of(var_name))
        output_file.write_arithmetic("add")
        index += 1
        compile_expression(tokenized)
        output_file.write_pop("temp", "0")
        output_file.write_pop("pointer", "1")
        output_file.write_push("temp", "0")
        output_file.write_pop("that", "0")
        index += 1
    else:
        index += 1
        compile_expression(tokenized)
        type_of = vars_table.kind_of(var_name)
        counter = vars_table.index_of(var_name)
        output_file.write_pop(type_of, counter)
        index += 1
    # return translated


def compile_while_statement(tokenized):
    global index, WHILE_COUNTER
    # translated = jt.write_keyword(tokenized[index])    # while
    WHILE_COUNTER += 1
    index += 1
    # translated += jt.write_symbol(tokenized[index])    # (
    index += 1
    output_file.write_label("WHILE_EXP" + str(WHILE_COUNTER))
    last = WHILE_COUNTER
    compile_expression(tokenized)
    output_file.write_arithmetic("not")
    index += 1
    # translated += jt.write_symbol(tokenized[index]) + "<statements>\n"   # {
    index += 1
    output_file.write_if("WHILE_END" + str(WHILE_COUNTER))
    while tokenized[index] != "}":
        compile_statement(tokenized)
    # translated += "</statements>\n" + jt.write_symbol(tokenized[index])    # }
    output_file.write_goto("WHILE_EXP" + str(last))
    output_file.write_label(("WHILE_END" + str(last)))
    index += 1
    # return translated


def compile_do_statement(tokenized):
    global index
    index += 1
    compile_subroutine_call(tokenized)
    index += 1
    output_file.write_pop("temp", 0)


def compile_return_statement(tokenized):
    global index
    translated = ""
    index += 1
    if tokenized[index] != ";":   # eg return expression
        compile_expression(tokenized)
        output_file.write_return()
    else:
        output_file.write_push("constant", 0)  # return
        output_file.write_return()
    index += 1


