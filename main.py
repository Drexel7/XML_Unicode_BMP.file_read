import os
from PIL import Image #pentru parsarea fisierelor BMP
import xml.etree.ElementTree as xml_tr #pentru parsarea fisierelor xml


class GenericFile: #clasa de baza
    def get_path(self):
        pass

    def get_freq(self):
        pass


class TextASCII(GenericFile): #clasa derivata
    path_absolut: str #atribut

    def __init__(self, path_absolut): #constructor
        try:
            self.freq = {} ##dictionarul in care vom retine frecventa caracterelor
            self.path_absolut = path_absolut #atribut
            with open(path_absolut, 'r') as f: #deschidem fisierul
                content = f.read() #citim continutul
            for char in content:
                if char in self.freq.keys():    #daca caracterul exista deja in dictionar
                    self.freq[char] += 1    #incrementam frecventa
                else:
                    self.freq[char] = 1

        except: #daca nu se poate deschide fisierul
            pass

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.freq


class TextUNICODE(GenericFile):
    path_absolut: str

    def __init__(self, path_absolut):
        try:
            self.freq = {}
            self.path_absolut = path_absolut
            with open(path_absolut, 'rb') as f: #deschidem fisierul in mod binar
                content = f.read()
            for char in content:
                if chr(char) in self.freq.keys():
                    self.freq[chr(char)] += 1
                else:
                    self.freq[chr(char)] = 1
            f.close()
        except:
            pass

    def get_path(self):
        return self.path_absolut #returnam calea absoluta

    def get_freq(self):
        return self.freq #returnam dictionarul cu frecventele


class Binary(GenericFile):
    path_absolut = "" #calea absoluta

    def __init__(self, path_absolut):
        try:
            self.freq = {} #dictionarul in care vom retine frecventa caracterelor
            self.path_absolut = path_absolut
            with open(path_absolut, 'rb') as f:
                content = f.read()
            content = bytes(content)

            for char in content:
                if char in self.freq.keys(): # daca caracterul exista deja in dictionar
                    self.freq[char] += 1
                else:
                    self.freq[char] = 1
            # print(self.freq)
            f.close()
        except:
            pass

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.freq


class BMP(Binary):
    def __init__(self, path_absolut, width, height, bpp):
        super().__init__(path_absolut) #apelam constructorul din clasa parinte
        self.width = width
        self.height = height #
        self.bpp = bpp #bits per pixel

    def show_info(self): #afisam informatiile despre imagine
        print("Path: " + str(self.path_absolut) + " Height: " + str(self.height) + " Width: " + str(
            self.width) + " Bpp: " + str(self.bpp)) #afisam informatiile despre imagine


class XML_File(TextASCII):
    def __init__(self, path_absolut, first_tag):
        super().__init__(path_absolut)
        self.first_tag = first_tag

    def get_first_tag(self): #returnam primul tag din fisier
        return self.first_tag


def isASCII(file_path): #verificam daca fisierul este ASCII
    try:
        f = open(file_path, 'r')
        content = f.read()
        lg = len(content) #lungimea fisierului

        x = TextASCII(file_path) #cream un obiect de tip TextASCII
        freq = x.get_freq() #obtinem dictionarul cu frecventele

        nrSimboluri = len(freq.keys()) #numarul de simboluri diferite

        median_freq = lg / nrSimboluri #mediana frecventei

        high_freq = [9, 10, 13] + [i for i in range(32, 128)]  # lista cu simboluri care ar trebui sa aiba frecventa mare
        low_freq = [i for i in range(0, 9)] + [11, 12] + [i for i in range(14, 32)] + [i for i in
                                                                                       range(128, 257)
                                                                                       ] # lista cu simboluri care ar trebui sa aiba frecventa mica
        okay = 1 #variabila care ne spune daca fisierul este ASCII sau nu
        for elem in high_freq: #parcurgem lista cu simboluri care ar trebui sa aiba frecventa mare
            if elem in freq.keys():
                if freq[elem] < median_freq:
                    okay = 0

        for elem in low_freq: #parcurgem lista cu simboluri .. mica
            if elem in freq.keys():
                if freq[elem] > median_freq:
                    okay = 0

        if okay == 1:
            return 1
        else:
            return 0
    except: #daca nu se poate deschide fisierul
        return 0


def isBinary(file_path):  # verificam daca fisierul este binar
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        content = bytes(content)
        lg = len(content)

        x = Binary(file_path) # cream un obiect de tip Binary
        freq = x.get_freq()  # obtinem dictionarul cu frecventele

        nrSimboluri = len(freq.keys()) # numarul de simboluri diferite
        median_freq = lg / nrSimboluri
        sum = 0
        for i in range(0, 256): # verificam daca suma frecventelor este egala cu lungimea fisierului
            sum += freq[i]

        wrong = [] # lista cu simboluri care nu se incadreaza in intervalul 60% - 140% din medie
        okay = 1
        for i in range(0, 256):
            if freq[i] > median_freq * 1.4 or freq[
                i] < median_freq * 0.6:  # daca nu se incadreaza intre 60% si 140% din medie
                wrong.append(i) # adaugam in lista

        if len(wrong) > nrSimboluri // 5:  # daca e mai mult de 20% din nr total de numere
            okay = 0
        return okay
    except:
        return 0


def isUNICODE(file_path):
    try:
        f = open(file_path, 'rb')
        content = f.read()
        lg = len(content)

        y = TextUNICODE(file_path) #cream un obiect de tip TextUNICODE
        freq = y.get_freq()

        if '0' in freq.keys(): #verificam daca exista caracterul null
            freq_0 = freq['0'] #daca exista, il stergem
        else:
            freq_0 = 0 #daca nu exista, ii dam valoarea 0

        if freq_0 >= lg * 0.3:  # daca exista mai mult de 30% din numarul total de caractere
            return 1
        else:
            return 0

    except:
        print("Eroare isUNICODE")
        return 0


def isBMP(file_path):
    if isBinary(file_path) == 1: #verificam daca fisierul este binar
        return 1
    return 0    #daca nu este binar, nu este BMP


if __name__ == "__main__":

    xml = [] #lista cu fisierele XML
    unicode = [] #lista cu fisierele UNICODE
    bmp = [] #lista cu fisierele BMP

    ROOT_DIR = r'D:\PP\LABORATOR\LAB6\Tema' #directorul curent
    for root, subdirs, files in os.walk(ROOT_DIR): #parcurgem recursiv directorul curent
        for file in os.listdir(root):
            file_path = os.path.join(root, file) #obtinem calea absoluta a fisierului
            if os.path.isfile(file_path): #verificam daca este fisier

                if isUNICODE(file_path): #verificam daca fisierul este UNICODE
                    x = TextUNICODE(file_path) #cream un obiect de tip TextUNICODE
                    unicode.append(x) #adaugam in lista
                else:
                    if isASCII(file_path):
                        try:
                            tree = xml_tr.parse(file_path) #incercam sa parsam fisierul ca XML
                            tree_root = tree.getroot() #obtinem radacina
                            first_tag = tree_root.tag #obtinem primul tag
                            xml_file = XML_File(file_path, first_tag) #cream un obiect de tip XML_File
                            xml.append(xml_file) #adaugam in lista
                        except:
                            pass

                if isBMP(file_path):
                    try:
                        im = Image.open(file_path) #incercam sa deschidem fisierul ca imagine
                        (height, width) = im.size #obtinem latimea si inaltimea
                        depth = im.depth #obtinem adancimea
                        bands = len(im.getbands()) #obtinem numarul de canale
                        bpp = depth * bands #obtinem numarul de biti pe pixel
                        bmp_photo = BMP(file_path, height, width, bpp=24) #cream un obiect de tip BMP
                        bmp.append(bmp_photo) #adaugam in lista
                    except:
                        pass

    print("XML files:")
    for elem in xml: #afisam informatiile despre fisierele XML
        print(elem.get_path())
        print("First tag: " + str(elem.get_first_tag()))
    print("\nUNICODE files: ")
    for elem in unicode:
        print(elem.get_path())
    print("\nBMP files: ")
    for elem in bmp:
        elem.show_info()
