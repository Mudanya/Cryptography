import base64


class Decrypt():
    ciphertext = "MDAxMTAxMTAwMDAwMDEwMDAwMTEwMTEwMTAxMDAxMTAxMDAwMDExMDAwMDEwMTEwMTEwMDAxMTAxMDAwMDExMDAxMDAxMTEwMTExMDExMTAxMTAwMTEwMDEwMTAxMTEwMDExMDAxMTExMDAxMTAxMDAxMTEwMDAxMTAwMTAxMTAxMDExMTExMDAxMDAwMDAx"
    key = "rachel"

    def __init__(self):
        self.toBinary(self.ciphertext, self.key)

    def toBinary(self, ciphertext, key):
        # ctext = base64.base64decode(ciphertext)
        ctext = base64.b64decode(ciphertext)
        print("Decoded ciphertext: ", ctext)
        self.key = ''.join(format(i, 'b') for i in bytearray(self.key, encoding='utf-8'))
        print("Key in Binary :", self.key)
        self.xoring(ctext, self.key)

    def xoring(self, ctext, keyfile):
        self.y = '{1:0{0}b}'.format(len(ctext), int(ctext, 2) ^ int(keyfile, 2))
        print("Result {} - Length {}".format(self.y, len(self.y)))
        self.split(self.y)

    def split(self,y):
        a = len(y)
        print("Length of Ciphertext = ", a)
        b = int(a / 2)  # int makes the division a whole number
        self.d = (y[:b])  # print everything from position 0 to b-1
        self.e = (y[b:])  # print everything from last to first
        print("Length of chunk_1: ", len(self.d))
        print("Length of chunk_2: ", len(self.e))
        print("Chunk_1: ", self.d)  # d is binary form of chunk 1
        print("Chunk_2: ", self.e)
        self.reverse(self.d)
        self.shift(self.e)

    def reverse(self, d):
        self.reversed = d[::-1]
        print("Reserved bits: ", self.reversed)

    def shift(self, e):
        self.rshift = e[-5:]+e[:-5]
        print("Shifted Chunk_2 Bits: ", self.rshift)
        self.concatenate(self.reversed, self.rshift)

    def concatenate(self, p, q):
        self.dectext = p+q
        print("Final Text: ", self.dectext)
        print(self.bits2a(self.dectext))

    def bits2a(self, b):
        return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)] * 8))

if __name__ == '__main__':
        Decrypt()


