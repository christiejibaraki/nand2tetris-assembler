"""
Translates assembly language into binary codes
"""

JUMP_CODES = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

DEST_CODES = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011", "DM": "011",
    "A": "100",
    "AM": "101", "MA": "101",
    "AD": "110", "DA": "110",
    "AMD": "111", "ADM": "111",
    "MAD": "111", "MDA": "111",
    "DAM": "111", "DMA": "111"
}

COMP_CODES = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000", "M": "1110000",
    "!D": "0001101",
    "!A": "0110001", "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011", "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101"
}


def translate_a_command(address_value, symbol_table):
    """
    Translate address command to binary
    :param address_value: (str) xxx in @xxx
    :param symbol_table: a symbol table
    :return: (str) binary address instruction
    """
    try:
        dec_value = int(address_value)
        return "0" + format(dec_value, "015b")
    except ValueError:
        if symbol_table.contains(address_value):
            return "0" + format(symbol_table.get_address(address_value), "015b")
        return "0" + format(symbol_table.add_variable(address_value), "015b")


def translate_c_command(dest, comp, jump):
    """
    translate dest=comp;jump command
    dest and jump can be "null"

    :param dest: (str)
    :param comp: (str)
    :param jump: (str)
    :return: (str) binary code
    """
    ac_code = translate_comp(comp)
    d_code = translate_dest(dest)
    j_code = translate_jump(jump)
    return "111" + ac_code + d_code + j_code


def translate_dest(mnemonic):
    """
    Convert dest mnemonic to binary
    :param mnemonic: (str) assembly dest command
    :return: (str) binary
    """
    if mnemonic not in DEST_CODES:
        raise Exception(f"Invalid dest mnemonic: {mnemonic}")
    return DEST_CODES[mnemonic]


def translate_comp(mnemonic):
    """
    Convert comp mnemonic to binary
    :param mnemonic: (str) assembly comp command
    :return: (str) binary
    """
    if mnemonic not in COMP_CODES:
        raise Exception(f"Invalid comp mnemonic: {mnemonic}")
    return COMP_CODES[mnemonic]


def translate_jump(mnemonic):
    """
    Convert jump mnemonic to binary
    :param mnemonic: (str) assembly jump command
    :return: (str) binary
    """
    if mnemonic not in JUMP_CODES:
        raise Exception(f"Invalid jump mnemonic: {mnemonic}")
    return JUMP_CODES[mnemonic]
