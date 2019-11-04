import os
#calling encrypt and decrypt function and have em under one file

class Crypto(object):
    def encryption(filename, keyfile):
        with open(filename, "rb") as infile:
            file_bytes = infile.read()
        print("Path and Name of Opened File: %s " % (filename))
        print("Keyfile: ", keyfile)

        # converting file to binary
        print("File Bytes: ", file_bytes[:50])
        file_bits = bin(int.from_bytes(file_bytes, 'big'))[2:]
        print("File Bits: {} Length of Bits: {}".format(file_bits[:50], len(file_bits)))

        # converting key to binary
        init = bin(int.from_bytes(keyfile, 'big'))[2:]
        len_file = len(file_bits)
        if len(init) > len_file:
            init = init[:len_file]
        print("Keyfile in Binary: ", init)

        # split the file bits into two chunks
        a = len(file_bits)
        print("Length of bit stream: ", a)
        b = int(a/2) #same as a//2
        c = a-b
        print("Length of First Chunk: ", b)
        print("Length of Second Chunk: ", c)
        d = (file_bits[:b])
        e = (file_bits[b:])
        print("First Chunk: ", d[:50])
        print("Second Chunk: ", e[:50])

        # for the first chunk, reverse the bits
        f = d[::-1]
        print("Reversed first chunk: " + f[:50])

        # for the second chunk, do some shifting to the right
        g = (e[5:]+e[:5])
        print("Second chunk after shift by 5 : " + g[:50])

        # concatenate the two chunks
        h = f + g
        print("Concatenated File Bits: ", h[:50] + " ... ")

        # xor the concatenated chunk with the key
        cipher_bin = '{1:0{0}b}'.format(len(h), int(h, 2) ^ int(init, 2))
        print('File Cipher in Binary: ', cipher_bin[:50])
        len_cipher_bin = len(cipher_bin)
        print("Length of Cipher Bit Stream: ", len_cipher_bin)

        # write the bits to file
        outPut_file = filename+".enc"
        with open(outPut_file, "w") as out_file:
            out_file.write(cipher_bin)
            out_file.close()
            os.remove(filename)
        print(" +++ Encryption Completed. +++ ")

    def decryption(filename, keyfile):
        with open(filename, "r") as infile:
            file_bits = infile.read()
        print("Path and Name of Opened File: %s " % (filename))
        print("File Content (bits): ", file_bits[:50])

        # convert key to binary
        init = bin(int.from_bytes(keyfile, 'big'))[2:]
        len_file_bits = len(file_bits)
        if len(init) > len_file_bits:
            init = init[:len_file_bits]
        print("Key in Binary: ", init)

        # xor the file and the key bits
        x = '{1:0{0}b}'.format(len(file_bits), int(file_bits, 2) ^ int(init, 2))
        print('XOR Result Between File and Key Bits: ', x[:50])

        # split the result of xor into two chunks
        a = len(x)
        print("Length of the File Bits: ", a)
        b = int(a / 2)
        d = x[:b]
        e = x[b:]
        print("First Chunk: {} - Chunk length: {}".format(d[:50] + " ...", len(d)))
        print("Second Chunk: {} - Chunk length: {}".format(e[:50] + " ...", len(e)))

        # for the first chunk, we reverse the bits
        f = d[::-1]
        print("Reversed Bits of the First Chunk ", f[:50])

        # for the second chunk, we shift the bits to the left
        g = e[-5:] + e[:-5]
        print("Second Chunk After Reverse Shift by 5 : ", g[:50])

        # concatenate the two chunks
        h = f + g
        print("Concatenated File Bits of Decrypted File: ", h[:50] + " ... ")

        # convert the bits to bytes
        file_bytes = int(h, 2).to_bytes((len(h) + 7) // 8, byteorder='big')
        print(" Decrypted File Bytes: ", file_bytes[:50])

        # write the file bytes to a file
        outfile = os.path.splitext(filename)[0]
        with open(outfile, "wb") as out_file:
            # Write bytes to the file"file.txt"
            out_file.write(file_bytes)
            out_file.close()
            os.remove(filename)
        print(" ++ Decryption Completed. ++ ")


