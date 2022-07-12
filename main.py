"""
Main Module
Run assembler
"""
import sys
import os
from src.symbol_table import SymbolTable
from src.parser import Parser
from src.code import translate_a_command, translate_c_command
from src.utility import write_file


def translate_program(input_file):
    result = ""
    symbol_table = SymbolTable()
    parser = Parser(input_file)

    # first pass to add labels to symbol table
    while parser.has_more_commands():
        parser.advance()
        try:
            if parser.current_command_type == Parser.L_COMMAND:
                parser.process_label(symbol_table)
        except Exception as e:
            print(f"Error parsing command {parser.current_command}")
            raise e

    # second pass to translate code
    parser.reset_command_index()
    while parser.has_more_commands():
        parser.advance()
        try:
            binary = ""
            if parser.current_command_type == Parser.C_COMMAND:
                dest, comp, jump = parser.get_dest_comp_jump()
                binary = translate_c_command(dest, comp, jump)
            elif parser.current_command_type == Parser.A_COMMAND:
                binary = translate_a_command(parser.get_symbol(), symbol_table)
            result += binary +"\n"
        except Exception as e:
            print(f"Error parsing command {parser.current_command}")
            raise e
    return result


if __name__ == "__main__":
    user_file_input = sys.argv[1]
    try:
        path, input_filename = os.path.split(os.path.realpath(user_file_input))
        _, extension = os.path.splitext(input_filename)
        if extension == ".asm":
            print(f"*** Translating {input_filename}")
            binary_codes = translate_program(user_file_input )
            out_filename = input_filename.split(".asm")[0] + ".hack"
            out_file_path = os.path.join(path, out_filename)
            write_file(out_file_path, binary_codes[0:-1])  # since last char is newline
            print(f"*** Writing output file {out_filename} to {path}")

    except FileNotFoundError as e:
        print("Input file not found")
        print(e)