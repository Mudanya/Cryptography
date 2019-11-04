import base64

class Encrypt():
    plaintext = input("Enter the text to encypt: ")
   # f = None
    #g = None
    #init = None
    v = None
    key = input("Enter the password: ")

    def __init__(self): #first thing to run when you enstanciate
        super(Encrypt, self).__init__()
        self.decToBinary()

    def decToBinary(self): #convert plaintext--> res and key--> self.init to binary
        print("Plaintext = ", str(self.plaintext))
       # res = ''.join(format(i, 'b') for i in bytearray(self.plaintext, encoding='utf-8'))
        res = ''.join(self.validate(i) for i in bytearray(self.plaintext, encoding='utf-8'))
        self.init = ''.join(format(i, 'b') for i in bytearray(self.key, encoding='utf-8'))
        print("Binary of plaintext = ", res)
        print('Binary form of key: ', self.init)
        self.split(res)

    def validate(self, byte):
        b = str(bin(byte))
        b = b[2:]
        print(b)
        if len(b) != 8:
            b = '0' * (8 - len(b)) + b
        print(b)
        return b

    def split(self, res):
        a = len(res)
        print("Length of PT in binary = ", a)
        b = int(a/2) # int makes the division a whole number
        c = a - b #2nd chunk
        print("Length of chunk_1: ", b)
        print("Length of chunk_2: ", c)
        d = (res[:b]) # print everything from position 0 to b-1
        e = (res[b:]) #print everything from last to first
        print("Chunk_1: ", d) #d is binary form of chunk 1
        print("Chunk_2: ", e)
        #self.reverse(b, d)
        self.reverse(d)
        self.shift(e)

    def reverse(self, d):
        chunklist=[]
        for i in range(len(d)):
            chunklist.append(d[i])
        chunklist.reverse()
        self.v = ''.join(chunklist)
        print("Reversed chunk_1 = ", self.v)
        # self.concatenation(v)
        #self.f = d[::-1] #from last to fist
        #self.f = d[b - 1::-1] #print anything after b-1// then in reverse
        #print("Reversed chunk_1: ", + self.f)

    def shift(self, e):
        g = e[5:]+e[:5] #anything after + before position 5
        print("Shift of chunk_2: ", g)
        self.concatenation(g)

    def concatenation(self, g):
        self.h = self.v + g
        print("Concatenated: ", self.h)
        self.xoring()

    def xoring(self):
        x = '{1:0{0}b}'.format(len(self.h), int(self.h, 2) ^ int(self.init, 2))
        print("Binary x: ", x)
        print("Length Cipher Text: ", len(x))
        bytex = bytes(str(x), encoding='utf-8')
        cbytex = base64.b64encode(bytex)
        # dcbytex = base64.b64decode(cbytex)
        print("Final Cipher: ", cbytex)


if __name__ == "__main__":
    window = Encrypt()

#0111010001101111011011110110110001110011
#0111010001101111011011110110110001110011


#011100100110000101100011011010000110000101100101011011000010000001101100011011110111011001100101011100110010000001100011011011110110010001100101
#011100100110000101100011011010000110000101100101011011000010000001101100011011110111011001100101011100110010000001100011011011110110010001100101