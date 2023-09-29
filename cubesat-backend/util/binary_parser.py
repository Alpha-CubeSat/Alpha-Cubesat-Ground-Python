from enum import Enum

from binary_reader import BinaryReader

from util.opcode_map import opcode_map


class BinaryTypes(Enum):
    """Types of binary numbers which can be read by the ``BinaryParser`` class"""

    uint16_list = 8
    uint8 = 9
    uint8_split = 10
    uint8_bools = 11
    uint5_list = 12

class BinaryParser:
    """Class that supports various operations for reading binary data"""

    reader = None

    def __init__(self, binary_data: bytearray):
        """Creates a BinaryParser from the given bytearray"""
        self.reader = BinaryReader(binary_data, endianness=True)

    def pos(self) -> int:
        """Returns the current pos in the buffer"""
        return self.reader.pos()
    
    def remaining(self) -> int:
        """Returns the remaining # of bytes in the buffer"""
        return len(self.reader.buffer())

    def read_uint8(self) -> int:
        """Reads and returns the next unsigned 8-bit integer from the buffer"""
        return self.reader.read_uint8()

    def read_uint16(self) -> int:
        """Reads and returns the next unsigned 16-bit integer from the buffer"""
        return self.reader.read_uint16()
    
    def read_uint8_split(self, name_list, decoded):
        """Reads and returns two 4-bit integers from the next unsigned 
        8-bit integer w/ the format (4-bit int + 4-bit int) from the buffer. 
        Written specifically for reading faults."""
        for entry in name_list:
            byte_value = self.reader.read_uint8()
            fir_4bit = (byte_value >> 4) & 0x0F
            sec_4bit = byte_value & 0x0F
            # Handles cases where only faults are present/eeprom_bools are present
            if entry[0] != "solar_current_average_fault":
                decoded[entry[0]], decoded[entry[1]] = fir_4bit, sec_4bit
            else:
                decoded[entry[0]] = fir_4bit
                for i, bool in enumerate(entry[1]):
                    decoded[bool] = (sec_4bit >> i) & 1 == 1

    def read_uint8_bools(self, name_list, decoded):
        """Reads and returns 8 bools from the next unsigned 8-bit integer.
        Written specifically for reading packaged bools."""

        name_list.reverse()
        byte_value = self.read_uint8()
        for i, entry in enumerate(name_list):
            decoded[entry] = (byte_value >> i) & 1 == 1

    def read_uint5_list(self, name, decoded):
        """Reads and returns 5-bit integers from 10 bytes worth of binary data. 
        Written specifically for decoding the mission-mode history.
        """

        # convert bytes to string of bits and convert every 5 bits to an integer
        history_bytes = self.reader.read_bytes(10)
        bits = format(int.from_bytes(history_bytes, byteorder="big"), '080b')
        for i in range(0, len(bits), 5):
            decoded[name].append(int(bits[i:i+5], 2))

    def read_uint16_list(self, name, decoded):
        """Reads and returns unsigned 16-bit integers until the end flag. 
        Written specifically for decoding processed opcode history.
        """
        while self.remaining()-self.pos() > 2:
            opcode = str(self.read_uint16())
            if opcode in opcode_map:
                decoded[name].append(opcode_map[opcode])
    
    def read_structure(self, structure: list[tuple[str, BinaryTypes]]) -> dict:
        """
        Uses a reader to read the input structure. Supports basic number types.
        Uses a data-driven interface with a list for 'structure' where names and types
        are passed in, and returns a map with names and the values read from the list.

        Example of the 'structure' parameter:\n
        ``structure = [('item_1', BinaryTypes.uint8), ('item_2', BinaryTypes.uint8)]``\n
        Reads an integer from the buffer and stores it in the map under the key 'item_1',
        reads and stores next integer under the key 'item_2', and returns the map.

        :param structure: list of tuples where the first element of the tuple is the name of
            the map key and the second is the BinaryType of the binary number to be read
        :return: a map containing the decoded numbers under their specified map keys
        """
        decoded = {}
        for (name, ptype) in structure:
            if ptype == BinaryTypes.uint8:
                decoded[name] = self.read_uint8()
            elif ptype == BinaryTypes.uint8_split:
                self.read_uint8_split(name, decoded)
            elif ptype == BinaryTypes.uint8_bools:
                self.read_uint8_bools(name, decoded)
            elif ptype == BinaryTypes.uint5_list:
                decoded[name] = []
                self.read_uint5_list(name, decoded)
            elif ptype == BinaryTypes.uint16_list:
                decoded[name] = []
                self.read_uint16_list(name, decoded)
            else:
                raise NotImplementedError()
        return decoded