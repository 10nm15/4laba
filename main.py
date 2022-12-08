import math

from rc5 import RC5

key = input("Input key: ").encode()

text = input("Input text: ")


def extractBitsFromBytes(byt3s):
    bits = []
    for byt3 in byt3s:
        cutb = bin(byt3)[2:]
        for bit in cutb:
            bits.append(int(bit))
    return bits


def extractBytesFromText(text):
    return text.encode()


def extractSubBits(bits, length, begin):
    subBits = []
    end = begin + length
    if end >= len(bits):
        end = len(bits)
    for i in range(begin, end):
        subBits.append(bits[i])
    return subBits


def extractBitsFromText(text):
    return extractBitsFromBytes(extractBytesFromText(text))


def extractBytesFromBits(bits):
    byt3s = []
    bytesCount = math.ceil(len(bits) / 8)
    for i in range(bytesCount):
        subBits = extractSubBits(bits, 8, i * 8)
        byteStr = "".join(str(bit) for bit in subBits)
        byt3s.append(int(byteStr, 2))
    return byt3s


def hash(text, key):
    blocklen = 64
    result = key
    textInBits = extractBitsFromText(text)
    c = math.ceil(len(textInBits) / blocklen)
    for blockNumber in range(c):
        rc5 = RC5(blocklen, 20, result)
        Mi = extractBytesFromBits(extractSubBits(textInBits, blocklen, blockNumber * blocklen))
        data = rc5.encryptBlock(Mi)
        prevHash = int.from_bytes(data, byteorder='little') ^ int.from_bytes(Mi, byteorder='little')
        result = prevHash.to_bytes(prevHash.bit_length(), byteorder='little')

    return result


final = int.from_bytes(bytes=hash(text, key), byteorder='little')
print(hex(final))
