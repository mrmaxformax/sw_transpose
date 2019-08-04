# !/usr/bin/env python3
"""
This is a script designed to find the longest word in the text file, transpose the letters and show
the result.
"""
import argparse
import concurrent.futures
import logging
import logging.handlers
import os
import re
import sys
from glob import glob

logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])


def file_reading(file_path: str) -> list:
    """
    The method just reads the text file line by line and saves the result to the list of strings. One line is in
    one list element
    :param file_path: Path to the file the script needs to read.
    :return: the list of strings, extracted from the file.
    """

    logger.debug("Current file path: {}".format(file_path))
    err_msgs = {'file_format_err': "Error: not supported file format!"}

    try:
        if not file_path.endswith('.txt'):
            print(err_msgs['file_format_err'])
            logger.debug(err_msgs['file_format_err'])
            sys.exit(1)

        with open(file_path, "r") as f:
            lines = list(filter(None, (line.rstrip() for line in f)))
        return lines
    except IOError as e:
        logger.exception("%s", e)
        sys.exit(1)


def transpose(string_list: list) -> None:
    """
    The method finds the longest word, transposes it and prints Original and Transpose words on the screen.
    Script exits with code '1' if gets empty list.
    If some string has more than one word it would be split into substrings and analyzed separately.
    If for some reason the script can not find any word, it prints the appropriate message.
    If the list has multiple words with the same length and that length is maximum, first word in the list will be
    returned as the longest. There can be multiple ways how to handle that situation (like print all, print some
    message, ask the user what should be done) but because there is no info in the description (the bug in the docs :-))
    I choose the simplest way.

    Output example:
        Original: abcde
        Transposed: edcba

    :param string_list: the list of strings for analisys
    :return: None
    """

    logger.debug("Got the list for analysis: {}".format(string_list))
    max_len_word: str = ''
    err_msgs = {"empty_list": "Error: the list of strings is empty!\n",
                "empty_string": 'There is only empty strings. Try to use another file.\n'}

    if len(string_list) == 0:
        print(err_msgs['empty_list'])
        logger.debug(err_msgs['empty_list'])
        sys.exit(1)

    for i in range(len(string_list)):
        list_item = string_list[i]
        list_item = list_item.strip()

        if list_item:
            # if we don't use regex we have a problem
            # if we use it we have more problems
            list_item = re.sub(r'([-])\1+', ' ', list_item)
            list_item = list_item.replace(' - ', ' ').replace('- ', ' ').replace(' -', ' ')
            list_item = re.sub(r'[^A-Za-z\- _]+',  '', list_item)

            sub_list_item = list_item.split(' ')

            for single_word in sub_list_item:
                if single_word:
                    single_word = single_word.replace(' ', '')
                    if len(single_word) > len(max_len_word):
                        max_len_word = single_word

    max_len_word_transposed: str = max_len_word[::-1]

    if max_len_word_transposed:
        conclusion = f"Original: {max_len_word}\nTransposed: {max_len_word_transposed}\n"
    else:
        conclusion = err_msgs['empty_string']

    logger.debug(conclusion)
    print(conclusion)


def parse_args(arguments: list):
    """
    Parse arguments. Just parse.
    :param arguments: the list of arguments, added by the user from CLI
    :return: the namespace with arguments and values
    """

    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-f", type=str, help="Path to the file")
    parser.add_argument("-p", type=str, help="Path to the folder with multiple files")

    g = parser.add_mutually_exclusive_group()
    g.add_argument("--debug", "-d", action="store_true", default=False, help="enable debugging mode")
    g.add_argument("--silent", "-s", action="store_true", default=False, help="enable silent (only critical) mode")

    args_parsed = parser.parse_args(arguments)
    if not (args_parsed.f or args_parsed.p):
        parser.error('No files requested, add -f file_name or -p path_to_files or --help for more info.')

    return args_parsed


def setup_logging(opt) -> None:
    """
    Logging configuration.
    :param opt: arguments from cli to choose what type of logging, silent/debug/none is active
    """
    root = logging.getLogger("")
    root.setLevel(logging.WARNING)
    logger.setLevel(opt.debug and logging.DEBUG or logging.INFO)

    if not opt.silent:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(levelname)s [%(name)s]: %(message)s"))
        root.addHandler(ch)


def main(path: str) -> None:
    """
    The main method runs 'file reading' and 'transpose' methods. The entry point.
    :param path: path to the file
    """

    logger.debug("Working with the words from '{}' file".format(path))
    list_of_strings = file_reading(file_path=path)
    transpose(string_list=list_of_strings)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    setup_logging(opt=args)

    err_msgs = {"path_file": "Error: The path to file was sent! Change to folder path not file path.",
                "dir_not_exist": "Error: The directory does not exist"}

    if args.f:
        main(path=args.f)
    else:
        if os.path.isfile(args.p):
            print(err_msgs['path_file'])
            logger.debug(err_msgs['path_file'])
            sys.exit(1)

        # Get a list of files to process
        if not os.path.exists(args.p):
            raise OSError(err_msgs['dir_not_exist'])

        files = glob(args.p + "/**/*.txt", recursive=True)

        # Create a pool of processes. One for each CPU.
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Process the list of files, split the work across the process pool to use all CPUs
            zip(files, executor.map(main, files))
