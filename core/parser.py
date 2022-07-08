"""
Parser:
Encapsulates access to the input code.
 - Reads an assembly language command
 - Parses it
 - Provides convenient access to components (fields and symbols)
 - (Additionally removes all white space and comments).
"""

import sys
import os
from utility import read_file, clean_code


def clean_assembly_lang_prog_file(input_file_arg):
    """
    Cleans text in file by stripping whitespace and removing comments
    Reads input file, cleans text, writes results to output file
    :param input_file_arg: file ending in .in
    :return: String, cleaned assembly language program
    """
    try:
        path, input_filename = os.path.split(os.path.realpath(sys.argv[1]))
        _, extension = os.path.splitext(input_filename)
        if extension == ".asm":
            print("Cleaning file: ", input_file_arg)
            clean_string = clean_code(read_file(input_file_arg))
            # out_filename = input_filename.split(".in")[0] + ".out"
            # out_file_path = os.path.join(path, out_filename)
            # write_file(out_file_path, clean_string)
            # print(f"Writing output file {out_filename} to {path}")
            return clean_string
        else:
            print("File must have extension .in")
    except FileNotFoundError as e:
        print("Input file not found")
        print(e)
    return None
