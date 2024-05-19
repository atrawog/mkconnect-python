#!/usr/bin/python

class MouldKingCrypt :
    """
    class with static methods to do MouldKing encryption
    """

    # static class variables
    __Array_C1C2C3C4C5 = [0xC1, 0xC2, 0xC3, 0xC4, 0xC5]

    @staticmethod
    def CreateTelegramForHCITool(manufacturerId, rawDataArray):
        """
        Create input data for hcitool 
        """
        cryptedArray = MouldKingCrypt.Crypt(rawDataArray)
        cryptedArrayLen = len(cryptedArray)

        resultArray = bytearray(8 + cryptedArrayLen)
        resultArray[0] = cryptedArrayLen + 13 # len
        resultArray[1] = 0x02                # flags
        resultArray[2] = 0x01
        resultArray[3] = 0x02
        resultArray[4] = cryptedArrayLen + 3 # len
        resultArray[5] = 0xFF                # type manufacturer specific
        resultArray[6] = manufacturerId[1]   # companyId
        resultArray[7] = manufacturerId[0]   # companyId
        for index in range(cryptedArrayLen):
            resultArray[index + 8] = cryptedArray[index]

        return ' '.join(f'{x:02x}' for x in resultArray)

    @staticmethod
    def Crypt(rawDataArray):
        """
        MouldKing encryption for the given byte-array and return the resulting byte-array 
        """

        targetArrayLength = len(MouldKingCrypt.__Array_C1C2C3C4C5) + len(rawDataArray) + 20

        targetArray = bytearray(targetArrayLength)
        targetArray[15] = 113
        targetArray[16] = 15
        targetArray[17] = 85

        for index in range(len(MouldKingCrypt.__Array_C1C2C3C4C5)):
            targetArray[index + 18] = MouldKingCrypt.__Array_C1C2C3C4C5[(len(MouldKingCrypt.__Array_C1C2C3C4C5) - index) - 1]

        targetArray[18 + len(MouldKingCrypt.__Array_C1C2C3C4C5):] = rawDataArray

        for index in range(15, len(MouldKingCrypt.__Array_C1C2C3C4C5) + 18):
            targetArray[index] = MouldKingCrypt.revert_bits_byte(targetArray[index])

        checksum = MouldKingCrypt.calc_checksum_from_arrays(MouldKingCrypt.__Array_C1C2C3C4C5, rawDataArray)
        targetArray[len(MouldKingCrypt.__Array_C1C2C3C4C5) + 18 + len(rawDataArray):] = [(checksum & 255), ((checksum >> 8) & 255)]

        magicNumberArray_63 = MouldKingCrypt.create_magic_array(63, 7)
        tempArrayLength = targetArrayLength - 18
        tempArray = targetArray[18:].copy()

        MouldKingCrypt.crypt_array(tempArray, magicNumberArray_63)
        targetArray[18:] = tempArray

        magicNumberArray_37 = MouldKingCrypt.create_magic_array(37, 7)
        MouldKingCrypt.crypt_array(targetArray, magicNumberArray_37)

        telegramArray = bytearray(24)

        lengthResultArray = len(MouldKingCrypt.__Array_C1C2C3C4C5) + len(rawDataArray) + 5
        telegramArray[:lengthResultArray] = targetArray[15:15 + lengthResultArray]

        for index in range(lengthResultArray, len(telegramArray)):
            telegramArray[index] = index + 1

        return telegramArray

    @staticmethod
    def create_magic_array(magic_number, size):
        magic_array = [0] * size
        magic_array[0] = 1

        for index in range(1, 7):
            magic_array[index] = (magic_number >> (6 - index)) & 1

        return magic_array

    @staticmethod
    def revert_bits_int(value):
        result = 0
        for index_bit in range(16):
            if ((1 << index_bit) & value) != 0:
                result |= 1 << (15 - index_bit)
        return 65535 & result

    @staticmethod
    def crypt_array(byte_array, magic_number_array):
        # foreach byte of array
        for index_byte in range(len(byte_array)):
            current_byte = byte_array[index_byte]
            current_result = 0
            # foreach bit in byte
            for index_bit in range(8):
                current_result += (((current_byte >> index_bit) & 1) ^ MouldKingCrypt.shift_magic_array(magic_number_array)) << index_bit
            byte_array[index_byte] = current_result & 255
        return byte_array

    @staticmethod
    def calc_checksum_from_arrays(first_array, second_array):
        result = 65535
        for first_array_index in range(len(first_array)):
            result = (result ^ (first_array[(len(first_array) - 1) - first_array_index] << 8)) & 65535
            for index_bit in range(8):
                current_result = result & 32768
                result <<= 1
                if current_result != 0:
                    result ^= 4129

        for current_byte in second_array:
            result = ((MouldKingCrypt.revert_bits_byte(current_byte) << 8) ^ result) & 65535
            for index_bit in range(8):
                current_result = result & 32768
                result <<= 1
                if current_result != 0:
                    result ^= 4129

        return MouldKingCrypt.revert_bits_int(result) ^ 65535

    @staticmethod
    def shift_magic_array(i_arr):
        r1 = i_arr[3] ^ i_arr[6]
        i_arr[3] = i_arr[2]
        i_arr[2] = i_arr[1]
        i_arr[1] = i_arr[0]
        i_arr[0] = i_arr[6]
        i_arr[6] = i_arr[5]
        i_arr[5] = i_arr[4]
        i_arr[4] = r1
        return i_arr[0]

    @staticmethod
    def revert_bits_byte(value):
        result = 0
        for index_bit in range(8):
            if ((1 << index_bit) & value) != 0:
                result = result | (1 << (7 - index_bit))
        return result
