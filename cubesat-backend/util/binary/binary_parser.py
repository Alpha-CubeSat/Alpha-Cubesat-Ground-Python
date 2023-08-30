from enum import Enum
import opcode_map
from binary_reader import BinaryReader


class BinaryTypes(Enum):
    """Types of binary numbers which can be read by the ``BinaryParser`` class"""

    # int64 = 0
    # int32 = 1
    # uint32 = 2
    # int16 = 3
    uint16 = 4
    # int8 = 5
    uint8 = 6
    # float64 = 7
    # float32 = 8

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
        decoded = {"command_log": []}
        for (name, ptype) in structure:
            if ptype == BinaryTypes.uint8:
                decoded[name] = self.read_uint8()
            elif ptype == BinaryTypes.uint16:
                decoded[name] = []
                while self.remaining()-self.pos() > 2:
                    opcode = str(self.read_uint16())
                    if opcode == "65279":
                        break
                    if opcode in opcode_map.opcode_map:
                        decoded[name].append(opcode_map.opcode_map[opcode])
            else:
                raise NotImplementedError()
        return decoded

