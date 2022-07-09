"""
SymbolTable Module
"""
import copy
from core.utility import invert_dictionary


PREDEFINED = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4,
    "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9,
    "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SCREEN": 16384, "KBD": 24576
}


class SymbolTable:
    """
    Keeps a correspondence between symbolic labels and numeric addresses
    """
    def __init__(self):
        """
        self.__table: dictionary mapping symbol (String) to address (int)
        self.__next_address: int, next avail address
        """
        self.__table = copy.deepcopy(PREDEFINED)
        self.__inverted_table = invert_dictionary(PREDEFINED)
        self.__next_address = 16

    def get_table(self):
        """
        :return: dictionary containing mapping
        """
        return self.__table

    def contains(self, symbol):
        """
        Does symbol table contain given symbol?
        :param symbol: (string) symbol
        :return: Boolean, true if self.__table contains symbol
        """
        return symbol in self.__table

    def get_address(self, symbol):
        """
        Returns address associated with symbol
        :param symbol: (string) symbol
        :return: (int) address
        """
        return self.__table[symbol]

    def add_label(self, symbol, address):
        """
        Add label to self.__table with corresponding address
        :param symbol: (string) label
        :param address: (int) address
        :return: (int) NA
        """
        return self.__add_entry(symbol, address)

    def add_variable(self, symbol):
        """
        Add variable to table at next avail address
        :param symbol: (string) variable
        :return: address used
        """
        if symbol in self.__table:
            raise KeyError(f"Entry {symbol} already exists at address {self.__table[symbol]}")

        while self.__next_address in self.__inverted_table:
            self.__next_address  += 1
        return self.__add_entry(symbol, self.__next_address )

    def __add_entry(self, symbol, address):
        """
        Add entry to self.__table
        :param symbol: (string) symbol
        :param address: (int) address
        :return: (int) address that was used
        """
        if symbol in self.__table:
            raise KeyError(f"Entry {symbol} already exists at address {self.__table[symbol]}")

        if address in self.__inverted_table:
            print(f"Adding {symbol} at address {address}")
            print(f"-- The following symbols also map to address {address}: {self.__inverted_table[address]}")

        self.__table[symbol] = address
        self.__inverted_table[address] = self.__inverted_table.get(address, []) + [symbol]
        return address
