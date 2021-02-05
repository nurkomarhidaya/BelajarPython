# RSA Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

import sys
# PENTING: Ukuran blok HARUS kurang dari atau sama dengan ukuran kunci!
# (Catatan: Ukuran blok dalam byte, ukuran kunci dalam bit. Di sana
# adalah 8 bit dalam 1 byte.)

# IMPORTANT: The block size MUST be less than or equal to the key size!
# (Note: The block size is in bytes, the key size is in bits. There
# are 8 bits in 1 byte.)

DEFAULT_BLOCK_SIZE = 128 # 128 bytes
BYTE_SIZE = 256 # One byte has 256 different values.

def main():
    # Menjalankan tes yang mengenkripsi pesan ke file atau mendekripsi pesan
    # dari file
    
    # Runs a test that encrypts a message to a file or decrypts a message
    # from a file.
    
    filename = 'encrypted_file1.txt' # the file to write to/read from
    mode = 'encrypt' # set to 'encrypt' or 'decrypt'
    #mode = 'decrypt' # set to 'encrypt' or 'decrypt'
    

    if mode == 'encrypt':
        message = '''"Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets." -Gerald Priestland "The Founding Fathers gave the free press the protection it must have to bare the secrets of government and inform the people." -Hugo Black'''
        pubKeyFilename = 'al_sweigart_pubkey.txt'
        print('Encrypting and writing to %s...' % (filename))
        encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)

        print('Encrypted text:')
        print(encryptedText)

    elif mode == 'decrypt':
        privKeyFilename = 'al_sweigart_privkey.txt'
        print('Reading from %s and decrypting...' % (filename))
        decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)

        print('Decrypted text:')
        print(decryptedText)


def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    # Mengubah pesan string menjadi daftar bilangan bulat blok. Setiap bilangan bulat
    # mewakili 128 (atau apapun blockSize diatur ke) karakter string.
     
    # Converts a string message to a list of block integers. Each integer
    # represents 128 (or whatever blockSize is set to) string characters.

    messageBytes = message.encode('ascii') # convert the string to bytes ( mengubah string menjadi byte )

    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):

        # Hitung bilangan bulat blok untuk blok teks ini
        # Calculate the block integer for this block of text

        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    # Mengubah daftar bilangan bulat blok ke string pesan asli.
    # Panjang pesan asli diperlukan untuk mengonversi yang terakhir dengan benar
    # blok bilangan bulat.
    
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                # Dekode string pesan untuk 128 (atau apa pun
                # blockSize disetel ke) karakter dari bilangan bulat blok ini.
                 
                # Decode the message string for the 128 (or whatever
                # blockSize is set to) characters from this block integer.
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
    # Mengubah string pesan menjadi daftar bilangan bulat blok, lalu
    # mengenkripsi setiap bilangan bulat blok. Teruskan kunci PUBLIK untuk mengenkripsi.
     
    # Converts the message string into a list of block integers, and then
    # encrypts each block integer. Pass the PUBLIC key to encrypt.
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        # ciphertext = plaintext ^ e mod n
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
    # Mendekripsi daftar int blok terenkripsi ke dalam pesan asli
    # string. Panjang pesan asli diperlukan untuk mendekripsi dengan benar
    # blok terakhir. Pastikan untuk memberikan kunci PRIVATE untuk mendekripsi.
     
    # Decrypts a list of encrypted block ints into the original message
    # string. The original message length is required to properly decrypt
    # the last block. Be sure to pass the PRIVATE key to decrypt.
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        # plaintext = ciphertext ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    # Diberikan nama file dari file yang berisi kunci publik atau pribadi,
    # mengembalikan kunci sebagai nilai tuple (n, e) atau (n, d).
  
    # Given the filename of a file that contains a public or private key,
    # return the key as a (n,e) or (n,d) tuple value.
    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=DEFAULT_BLOCK_SIZE):
    # Menggunakan kunci dari file kunci, mengenkripsi pesan dan menyimpannya ke file
    # file. Mengembalikan string pesan terenkripsi.
     
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.
    keySize, n, e = readKeyFile(keyFilename)
    
    # Periksa apakah ukuran kunci lebih besar dari ukuran blok.
    # Check that key size is greater than block size.
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (blockSize * 8, keySize))

    # Enkripsi pesannya
    # Encrypt the message
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)

    # Ubah nilai int yang besar menjadi satu nilai string.
    # Convert the large int values to one string value.
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    # Tuliskan string terenkripsi ke file keluaran.
    # Write out the encrypted string to the output file.
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    fo = open(messageFilename, 'w')
    fo.write(encryptedContent)
    fo.close()
    
    # Juga kembalikan string yang dienkripsi.
    # Also return the encrypted string.
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    # Menggunakan kunci dari file kunci, baca pesan terenkripsi dari file
    # dan kemudian mendekripsinya. Mengembalikan string pesan yang didekripsi.
     
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    keySize, n, d = readKeyFile(keyFilename)

    # Baca panjang pesan dan pesan terenkripsi dari file.
    # Read in the message length and the encrypted message from the file.
    fo = open(messageFilename)
    content = fo.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    # Periksa apakah ukuran kunci lebih besar dari ukuran blok
    # Check that key size is greater than block size.
    if keySize < blockSize * 8: # * 8 to convert bytes to bits ( * 8 untuk mengubah byte menjadi bit )
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Did you specify the correct key file and encrypted file?' % (blockSize * 8, keySize))

    # Ubah pesan terenkripsi menjadi nilai int yang besar.
    # Convert the encrypted message into large int values.
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    # Dekripsi nilai int yang besar.
    # Decrypt the large int values.
    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)

# Jika rsaCipher.py dijalankan (bukannya diimpor sebagai modul) panggil
# fungsi main ().

# If rsaCipher.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()
