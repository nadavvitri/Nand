############################################################
# Imports
############################################################
import re
from string import punctuation


def write_keyword(keyword):
    return "<keyword> " + keyword + " </keyword>\n"


def write_identifier(identifier):
    return "<identifier> " + identifier + " </identifier>\n"


def write_symbol(symbol):
    if symbol == '<':
        symbol = "&lt;"
    elif symbol == '>':
        symbol = "&gt;"
    elif symbol == '&':
        symbol = "&amp;"
    elif symbol == '"':
        symbol = "&quot;"
    return "<symbol> " + symbol + " </symbol>\n"


def write_integer(integer):
    return "<integerConstant> " + integer + " </integerConstant>\n"


def write_string(str):
    return "<stringConstant> " + str + " </stringConstant>\n"


def file_to_tokens(file):
    """
    gets file and ignore the lines we don't need, remove comments and add to list
    :param file: jack file to be translated
    :return: file content in list
    """
    file_list = []
    for ln in file.splitlines():
        pattern = re.compile(r'\w+|[{}]'.format(re.escape(punctuation)))
        if '"' in ln:
            first = ln.find('\"')   # find first index of "
            last = ln.index('\"', first + 1)   # find last index of "
            tokens = pattern.findall(ln[:first])  # regex until the first " appear
            tokens.append(ln[first:last + 1])     # append the "string"
            tail = pattern.findall(ln[last + 1:])     # regex the tail of the line
            tokens.extend(tail)
        else:
            tokens = pattern.findall(ln)
        for token in tokens:
            file_list.append(token)
    return file_list
