############################################################
# Imports
############################################################
import JackTokenizer as jt

############################################################
# Globals
############################################################
keyword = ["class", "constructor", "function", "method", "field", "static",
           "var", "int", "char", "boolean", "void", "true", "false", "null",
           "this", "let", "do", "if", "else", "while", "return"]

symbol = ['{', '}', '(', ')', ']', '[', '.', ',', ';', '+', '-', '*', '/', '&',
          '|', '<', '>', '=', '~']

keyword_constant = ['true', 'false', 'null', 'this']

op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

index = 0


def check_type(var_type):
    if var_type in keyword:
        return jt.write_keyword(var_type)
    return jt.write_identifier(var_type)


def translate_token(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])  # class
    index += 1
    translated += jt.write_identifier(tokenized[index])  # name
    index += 1
    translated += jt.write_symbol(tokenized[index])   # "{"
    index += 1
    return "<class>\n" + translated + inside_class(tokenized) + jt.write_symbol(tokenized[index]) + "</class>"


def inside_class(tokenized):
    global index
    if tokenized[index] == "}":
        return ""
    if tokenized[index] == "static" or tokenized[index] == "field":
        return compile_class_var_dec(tokenized) + inside_class(tokenized)
    elif tokenized[index] == "function" or tokenized[index] == "method" or tokenized[index] == "constructor":
        return "<subroutineDec>\n" + compile_subroutine_dec(tokenized) + "</subroutineDec>\n" + inside_class(tokenized)


def compile_class_var_dec(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])  # field / static
    index += 1
    translated += check_type(tokenized[index])   # type
    index += 1
    translated += jt.write_identifier(tokenized[index])  # varName
    index += 1
    while tokenized[index] != ";":
        translated += jt.write_symbol(tokenized[index])     # ,
        index += 1
        translated += jt.write_identifier(tokenized[index])
        index += 1
    translated += jt.write_symbol(tokenized[index])   # ;
    index += 1
    return "<classVarDec>\n" + translated + "</classVarDec>\n"


def compile_subroutine_dec(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])
    index += 1
    translated += check_type(tokenized[index])
    index += 1
    translated += jt.write_identifier(tokenized[index])
    index += 1
    translated += jt.write_symbol(tokenized[index])
    index += 1
    if tokenized[index] == ")":
        translated += "<parameterList>\n</parameterList>\n" + jt.write_symbol(tokenized[index]) + \
                      "<subroutineBody>\n" + compile_subroutine_body(tokenized) + "</subroutineBody>\n"
    else:
        translated += "<parameterList>\n" + compile_params_list(tokenized) + "</parameterList>\n" + \
           jt.write_symbol(tokenized[index]) + "<subroutineBody>\n" + compile_subroutine_body(tokenized) +\
           "</subroutineBody>\n"
    index += 1
    return translated


def compile_params_list(tokenized):
    global index
    translated = check_type(tokenized[index])
    index += 1
    translated += jt.write_identifier(tokenized[index])
    index += 1
    if tokenized[index] == ",":
        translated += jt.write_symbol(tokenized[index])
        index += 1
        return translated + compile_params_list(tokenized)
    return translated


def compile_subroutine_body(tokenized):
    global index
    index += 1
    translated = jt.write_symbol(tokenized[index])  # "{"
    index += 1
    vars_dec = ""
    statements = ""
    while tokenized[index] == "var":
        vars_dec += compile_var_dec(tokenized)
    while tokenized[index] != "return":
        if tokenized[index] != '}':
            statements += compile_statement(tokenized)
        else:
            return translated + vars_dec + "<statements>\n" + statements \
                   + "</statements>\n" + jt.write_symbol(tokenized[index])

    return translated + vars_dec + "<statements>\n" + statements + compile_statement(tokenized) \
           + "</statements>\n" + jt.write_symbol(tokenized[index])


def compile_many_vars_dec(tokenized):
    global index
    translated = jt.write_symbol(tokenized[index])  # ","
    index += 1
    translated += jt.write_identifier(tokenized[index])  # var
    index += 1
    while tokenized[index] != ";":
        translated += jt.write_symbol(tokenized[index])  # ","
        index += 1
        translated += jt.write_identifier(tokenized[index])  # var
        index += 1
    return translated


def compile_var_dec(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])
    index += 1
    translated += check_type(tokenized[index])
    index += 1
    translated += jt.write_identifier(tokenized[index])
    index += 1
    if tokenized[index] == ",":
        translated += compile_many_vars_dec(tokenized)
    translated = "<varDec>\n" + translated + jt.write_symbol(tokenized[index]) + "</varDec>\n"
    index += 1
    return translated


def compile_statement(tokenized):
    global index
    if tokenized[index] == "}":
        return
    if tokenized[index] == "if":
        return "<ifStatement>\n" + compile_if_statement(tokenized) + "</ifStatement>\n"
    elif tokenized[index] == "let":
        return "<letStatement>\n" + compile_let_statement(tokenized) + "</letStatement>\n"
    elif tokenized[index] == "while":
        return "<whileStatement>\n" + compile_while_statement(tokenized) + "</whileStatement>\n"
    elif tokenized[index] == "do":
        return "<doStatement>\n" + compile_do_statement(tokenized) + "</doStatement>\n"
    elif tokenized[index] == "return":
        return "<returnStatement>\n" + compile_return_statement(tokenized) + "</returnStatement>\n"
    else:
        return jt.write_symbol(tokenized[index]) + compile_statement(tokenized) + jt.write_symbol(tokenized[index])


def compile_else(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])   # else
    index += 1
    translated += jt.write_symbol(tokenized[index])   # {
    index += 1
    statements = ""
    while tokenized[index] != "}":
        statements += compile_statement(tokenized)
    return translated + "<statements>\n" + statements + "</statements>\n"


def compile_expression(tokenized):
    global index
    if tokenized[index] == ")":
        return
    elif tokenized[index].isdigit():
        translated = "<term>\n" + "<integerConstant> " + tokenized[index] + " </integerConstant>\n" +\
                     "</term>\n"
        index += 1
    elif '"' in tokenized[index]:  # "
        temp_str = tokenized[index][1:-1]
        if temp_str == "":
            translated = "<term>\n" + "<stringConstant>" + "\n</stringConstant>\n" + \
                         "</term>\n"
        else:
            translated = "<term>\n" + "<stringConstant>" + temp_str.strip() + "</stringConstant>\n" +\
                     "</term>\n"
        index += 1
    elif tokenized[index] in keyword_constant:
        translated = "<term>\n" + jt.write_keyword(tokenized[index]) + "</term>\n"
        index += 1
    elif tokenized[index] == "(":
        translated = "<term>\n" + jt.write_symbol(tokenized[index]) + "<expression>\n"
        index += 1
        translated += compile_expression(tokenized) + "</expression>\n"
        translated += jt.write_symbol(tokenized[index]) + "</term>\n"
        index += 1
    elif tokenized[index] == '-' or tokenized[index] == '~':
        translated = "<term>\n" + jt.write_symbol(tokenized[index])
        index += 1
        translated += compile_expression(tokenized) + "</term>\n"
        return translated
    else:
        translated = "<term>\n" + jt.write_identifier(tokenized[index])   # var
        index += 1
        if tokenized[index] == "[":  # arry
            translated += jt.write_symbol(tokenized[index]) + "<expression>\n"  # [
            index += 1
            translated += compile_expression(tokenized) + "</expression>\n" + jt.write_symbol(tokenized[index])
            index += 1
        elif tokenized[index] == "(" or tokenized[index] == ".":  # subroutine call
            translated += compile_subroutine_call_sec(tokenized)  # . or (
        translated += "</term>\n"
    while tokenized[index] in op:   # eg x | y
        translated += jt.write_symbol(tokenized[index])  # op
        index += 1
        translated += compile_expression(tokenized)
    return translated


def compile_expression_list(tokenized):
    global index
    if tokenized[index] == ")":  # no expression at all
        return "<expressionList>\n </expressionList>\n"
    translated = "\n<expression>\n" + compile_expression(tokenized) + "</expression>\n"
    while tokenized[index] == ",":
        translated += jt.write_symbol(tokenized[index])
        index += 1
        translated += "<expression>\n" + compile_expression(tokenized) + "</expression>\n"
    return "<expressionList>" + translated + "</expressionList>\n"


def compile_subroutine_call(tokenized):
    global index
    translated = jt.write_identifier(tokenized[index])  # subroutineName | className | varName
    index += 1
    if tokenized[index] == ".":
        translated += jt.write_symbol(tokenized[index])  # .
        index += 1
        translated += jt.write_identifier(tokenized[index])  # name
        index += 1
    translated += jt.write_symbol(tokenized[index])   # (
    index += 1
    translated += compile_expression_list(tokenized) + jt.write_symbol(tokenized[index])
    index += 1
    return translated


def compile_subroutine_call_sec(tokenized):
    global index
    translated = ""
    if tokenized[index] == ".":
        translated += jt.write_symbol(tokenized[index])  # .
        index += 1
        translated += jt.write_identifier(tokenized[index])  # name
        index += 1
    translated += jt.write_symbol(tokenized[index])   # (
    index += 1
    translated += compile_expression_list(tokenized) + jt.write_symbol(tokenized[index])
    index += 1
    return translated


def compile_if_statement(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])
    index += 1
    translated += jt.write_symbol(tokenized[index])  # '('
    index += 1
    translated += "<expression>\n" + compile_expression(tokenized) + "</expression>\n" \
                  + jt.write_symbol(tokenized[index])  # eg if (xxx)
    index += 1
    translated += jt.write_symbol(tokenized[index])  # "{"
    index += 1
    statements = ""
    while tokenized[index] != "}":
        statements += compile_statement(tokenized)
    translated += "<statements>\n" + statements + "</statements>\n" + jt.write_symbol(tokenized[index])
    index += 1
    if tokenized[index] == "else":
        translated += compile_else(tokenized) + jt.write_symbol(tokenized[index])
        index += 1
    return translated


def compile_let_statement(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])    # let
    index += 1
    translated += jt.write_identifier(tokenized[index])  # varName
    index += 1
    if tokenized[index] == "[":
        translated += jt.write_symbol(tokenized[index])
        index += 1
        translated += "<expression>\n" + compile_expression(tokenized) + "</expression>\n" \
                      + jt.write_symbol(tokenized[index])
        index += 1
    translated += jt.write_symbol(tokenized[index])    # =
    index += 1
    translated += "<expression>\n" + compile_expression(tokenized) + "</expression>\n" + \
                  jt.write_symbol(tokenized[index])
    index += 1
    return translated


def compile_while_statement(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])    # while
    index += 1
    translated += jt.write_symbol(tokenized[index])    # (
    index += 1
    translated += "<expression>\n" + compile_expression(tokenized) + \
                  "</expression>\n" + jt.write_symbol(tokenized[index])
    index += 1
    translated += jt.write_symbol(tokenized[index]) + "<statements>\n"   # {
    index += 1
    while tokenized[index] != "}":
        translated += compile_statement(tokenized)
    translated += "</statements>\n" + jt.write_symbol(tokenized[index])    # }
    index += 1
    return translated


def compile_do_statement(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])     # do
    index += 1
    translated += compile_subroutine_call(tokenized) + jt.write_symbol(tokenized[index])
    index += 1
    return translated


def compile_return_statement(tokenized):
    global index
    translated = jt.write_keyword(tokenized[index])   # return
    index += 1
    if tokenized[index] != ";":   # eg return expression
        translated += "<expression>\n" + compile_expression(tokenized) + "</expression>\n"
    translated += jt.write_symbol(tokenized[index])  # ;
    index += 1
    return translated

