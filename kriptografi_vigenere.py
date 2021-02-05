################################################################
# Vigenère Cipher ( Sandi Subtitusi Polyalphabetic )#
# Editor : Muhammad Azis Suprayogi#
# Source : # http://inventwithpython.com/hacking (BSD Licensed)#
################################################################

import pyperclip

HURUF = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#pada fungsi main terdapat variabel pesan, kunci dan mode sebelum program dijalankan
#pada mode anda dapat menetapkan apakah program akan melakukan enkripsi atau dekripsi
def main():
    pesanSaya = """Muhammad Azis Suprayogi, NIM 92319021, Tugas Keamanan Sistem dan Kriptografi, 
    Kelas 56 MMSI 1, Dosen Dr.Ihsan Jatnika"""
    kunciSaya = 'GUNADARMA'
    #silahkan ubah untuk melakukan enkripsi atau dekripsi disini
    modeSaya = 'enkripsi' 

    if modeSaya == 'enkripsi':
        ubah = enkripsiPesan(kunciSaya, pesanSaya)
    elif modeSaya == 'dekripsi':
        ubah = dekripsiPesan(kunciSaya, pesanSaya)

    print('%sed pesan : ' % (modeSaya.title()))
    print(ubah)
    pyperclip.copy(ubah)
    print()
    print('Pesan akan disalin kedalam papan klip.')

#pada bagian ini menjelaskan bagaimana enkripsi berjalan
def enkripsiPesan(kunci, pesan):
    return ubahPesan(kunci, pesan, 'enkripsi')

#pada bagian ini menjelaskan bagaimana dekripsi berjalan
def dekripsiPesan(kunci, pesan):
    return ubahPesan(kunci, pesan, 'dekripsi')

def ubahPesan(kunci, pesan, mode):
    ubah = [] 

    #menyimpan pesan enkripsi dan dekripsi

    kunciIndex = 0
    kunci = kunci.upper()

    for symbol in pesan: 
    #akan dilakukan pada seluruh karakter dalam pesan
        nomor = HURUF.find(symbol.upper())
        if nomor != -1: #-1 berarti symbol.upper() tidak ditemukan didalam HURUF
            if mode == 'enkripsi':
                nomor += HURUF.find(kunci[kunciIndex]) #tambahkan jika dienkripsi
            elif mode == 'dekripsi':
                nomor -= HURUF.find(kunci[kunciIndex]) #kurangi jika melakukan dekripsi

            nomor %= len(HURUF) 
           
            #tambahkan pada hasil symbol enkrip/dekrip yang sudah diubahkan
            if symbol.isupper():
                ubah.append(HURUF[nomor])
            elif symbol.islower():
                ubah.append(HURUF[nomor].lower())

            kunciIndex += 1 
            #ubah kunci yang akan dipakai selanjutnya
            if kunciIndex == len(kunci):
                kunciIndex = 0

        else:
            #symbol tidak berada pada HURUF, maka tambahkan hal tersebut dan ubahkan
            ubah.append(symbol)

    return ''.join(ubah)

#jika sandiVigenere.py sudah berjalan termasuk seluruh modulnya
#panggil fungsi main
if __name__ == '__main__':
    main()
    
    
#Enkripsied pesan : 
#Souapmrp Afcf Sxpimyuav, NLM 92319021, Kgggm Xedmrzat Mvswed pat Eeistfsrgzv, 
#   Khlre 56 MSMV 1, Drsvz Dx.Cusdn Amttcxa
