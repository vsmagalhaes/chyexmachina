import numpy as np


def _commentstripper(filein, cchar):
    linesout = []
    for line in filein:
        pos = line.find(cchar)
        if pos != 0:
            if pos != -1:
                linesout.append(line[:pos])
            else:
                linesout.append(line)
    return linesout


def strip_off_comm(filein, *cmtchars):
    """
    Strips a file of comments and returns it as a list of strings, each string a line.
    *** DOES NOT CLOSE FILE
    :param filein: Variable carrying the file
    :param cmtchars: List of comment markers, if none given, # is assumed
    :return: list of strings without commented lines
    """
    if isinstance(filein, file):
        list = _file_to_list(filein)
    else:
        list = filein
    if cmtchars:
        for cchar in cmtchars:
            list = _commentstripper(list, cchar)
    else:
        list = _commentstripper(list, "#")
    return list


def _file_to_list(entrada, *rewind):
    """
    Turns file into a list of strings for further processing
    rewinds file to initial state
    :param entrada: file to converted
    :return: list of strings representative of file
    """
    saida = []
    for line in entrada:
        if (line.strip()):
            saida.append(line)
    entrada.seek(0)
    return saida


def float_line(line, *columns, **kwargs):
    """
    Transforms a string into a numpy array of floats
    :param line: Input line
    :param columns: Desired columns, Defaults to all
    :param kwargs: skip -> columns to skip if any (List)!
    :return:
    """
    if 'skip' in kwargs:
        skipcolumns = kwargs['skip']
    else:
        skipcolumns = []
    words = line.split()
    numvalues = []
    posout = 0
    if not columns:
        columns = range(len(words))
    for i in range(len(words)):
        if (i in columns) and not (i in skipcolumns):
            numvalues.append(float(words[i]))
            posout += 1
    numvalues = np.asarray(numvalues)
    return numvalues


def float_file(filein, *columns, **kwargs):
    """
    Transforms a file from a file container or already as a list of strings into a 2 numpy array of floats.
    If file is in file container file should be closed afterwards
    ***strip_off_comm should be run first to avoid crashes!
    *** DOES NOT CLOSE FILE
    :param file: Input file or list of strings
    :param columns: Desired columns, defaults to all
    :param kwargs: skip -> columns to skip if any (List)!
    :return: a 2D numpy array of the values in File
    """
    if isinstance(filein, file):
        list = _file_to_list(filein)
    else:
        list = filein
    output = []
    for line in list:
        numline = float_line(line, *columns, **kwargs)
        output.append(numline)
    output = np.asarray(output)
    return output


def str_file(filein, *columns, **kwargs):
    """
    Returns a list of strings from line
    :param filein: Input file or list of strings
    :param columns: Desired columns, defaults to all
    :param kwargs: skip -> columns to skip if any (List)!
    :return:
    """
    if isinstance(filein, file):
        list = _file_to_list(filein)
    else:
        list = filein
    output = []
    for line in list:
        strline = str_line(line, *columns, **kwargs)
        output.append(strline)
    output = np.asarray(output, dtype=str)
    return output


def str_line(line, *columns, **kwargs):
    """
    Transforms a string into a numpy array of strings
    :param line: Input line
    :param columns: Desired columns, Defaults to all
    :param kwargs: skip -> columns to skip if any (List)!
    :return:
    """
    if 'skip' in kwargs:
        skipcolumns = kwargs['skip']
    else:
        skipcolumns = []
    words = line.split()
    numvalues = []
    posout = 0
    if not columns:
        columns = range(len(words))
    for i in range(len(words)):
        if (i in columns) and not (i in skipcolumns):
            numvalues.append((words[i]))
            posout += 1
    numvalues = np.asarray(numvalues, dtype=str)
    return numvalues


def print_list_inlines(list):
    """
    Prints a list in lines per line element
    :param list: input list
    :return: VOID
    """
    for obj in list:
        print obj
