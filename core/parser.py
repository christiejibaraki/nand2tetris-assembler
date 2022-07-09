"""
Parser:
Encapsulates access to the input code.
 - Reads an assembly language command
 - Parses it
 - Provides convenient access to components (fields and symbols)
 - (Additionally removes all white space and comments).
"""

import os
from core.utility import read_file, clean_code


class Parser:

    A_COMMAND = "address_command"
    C_COMMAND = "computation_command"
    L_COMMAND = "label_command"

    def __init__(self, input_file):
        self.clean_prog = clean_assembly_lang_prog_file(input_file)
        self.commands = self.clean_prog.split("\n")
        self.current_index = None
        self.current_command = None
        self.current_command_type = None
        self.symbol = None
        self.dest = None
        self.comp = None
        self.jump = None

    def has_more_commands(self):
        """
        Returns true if more commands in input
        :return: Boolean
        """
        return self.current_index is None or self.current_index < len(self.commands)-1

    def advance(self):
        """
        Advance command
        :return: NA, increment index and update current_command
        """
        if self.current_index is None:
            self.current_index = 0
        else:
            if self.current_index == len(self.commands)-1:
                raise Exception("No more commands in the input")
            self.current_index += 1
        self.current_command = self.commands[self.current_index]
        self.__update_command_properties()

    def __update_command_properties(self):
        """
        Set current command type
        :return:
        """
        self.__reset_properties()

        if self.current_command is None:
            self.current_command_type = None
        elif self.current_command[0] == "@":
            self.current_command_type = Parser.A_COMMAND
            self.symbol = self.current_command[1:]
        elif self.current_command[0] == "(":
            self.current_command_type = Parser.L_COMMAND
            self.symbol = self.current_command[1:-1]
        else:
            self.current_command_type = Parser.C_COMMAND
            self.dest, self.comp, self.jump = parse_command(self.current_command)

    def __reset_properties(self):
        """
        Reset properties of current command to None
        :return: NA
        """
        self.symbol = None
        self.dest = None
        self.comp = None
        self.jump = None

    def command_type(self):
        """
        Return type of current command
        :return: (str) A_COMMAND, C_COMMAND, or L_COMMAND
        """
        return self.current_command_type

    def get_symbol(self):
        return self.symbol

    def get_dest_comp_jump(self):
        return self.dest, self.comp, self.jump


def parse_command(command_str):
    """
    Parse command string
    :param command_str: (str) command
    :return: tuple (str, str, str)
    """
    dest = "null"  # optional
    comp = None  # required
    jump = "null"  # optional

    if "=" in command_str:
        tmp = command_str.split("=")
        dest = tmp[0]
        comp = tmp[1].split(";")[0]
    else:
        comp = command_str.split(";")[0]

    if ";" in command_str:
        jump = command_str.split(";")[1]

    return dest, comp, jump


def clean_assembly_lang_prog_file(input_file_arg):
    """
    Cleans text in file by stripping whitespace and removing comments
    Reads input file, cleans text, writes results to output file
    :param input_file_arg: file ending in .in
    :return: (str) cleaned assembly language program
    """
    try:
        _, input_filename = os.path.split(os.path.realpath(input_file_arg))
        _, extension = os.path.splitext(input_filename)
        if extension == ".asm":
            clean_string = clean_code(read_file(input_file_arg))
            return clean_string
        else:
            print(f"For file {input_filename}, expected extension .asm; actual extension: {extension}")
    except FileNotFoundError as e:
        print("Input file not found")
        print(e)
    return None
