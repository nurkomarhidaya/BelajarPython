import pyperclip


def main():
    pesanSaya = 'Indonesia Raya Tanah Airku:IRTA'
    kunciSaya = 8

    sanditeks = enkripsiPesan(kunciSaya, pesanSaya)
    print(sanditeks + '|')

    pyperclip.copy(sanditeks)

def enkripsiPesan(kunci, pesan):
    sanditeks = ['']*kunci

    for col in range(kunci):
        pointer = col

        while pointer < len(pesan):
            sanditeks[col] += pesan[pointer]

            pointer += kunci

        return ''.join(sanditeks)

    if __name__ == '__main__':
        main()

    
