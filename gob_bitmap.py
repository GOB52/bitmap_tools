
#
# 4bit 16colors bitmap
#
from struct import pack
from struct import unpack
import array
from ctypes import *


class BITMAPFILEHEADER(LittleEndianStructure):
    _pack_ = 2
    _fields_ = [
        ('bfType', c_uint16),
        ('bfSize', c_uint32),
        ('bfReserved1', c_uint16),
        ('bfReserved2', c_uint16),
        ('bfOffBits', c_uint32),
    ]

    def __init__(self, width = 0, height = 0, depth = 4, clrs = 16):
        hsize = 14 + 40 + (4 * clrs)  # BITMAPFILEHADER + BITMAPINFOHEADER + palettes
        dwidth = width + ((width % 4) + 3) // 4
        self.biType = 0x4d42
        self.bfSize = hsize + (dwidth * height) // 2 # 4
        self.bfReserved1 = self.bfReserved2 = 0
        self.bfOffBits = hsize

    def __repr__(self):
        return 'BitmapFileHeader\n' + 'bfType:' + hex(self.bfType) + '\n' + 'bfSize:' + str(self.bfSize) + '\n' + 'bfOffBits:' + hex(self.bfOffBits)

    def valid(self):
        return True if self.bfType == 0x4d42 else False


class BITMAPINFOHEADER(LittleEndianStructure):
    _pack_ = 2
    _fields_ = [
        ("biSize", c_uint32),
        ("biWidth", c_int32),
        ("biHeight", c_int32),
        ("biPlanes", c_uint16),
        ("biBitCount", c_uint16),
        ("biCompression", c_uint32),
        ("biSizeImage", c_uint32),
        ("biXPelsPerMeter", c_int32),
        ("biYPelsPerMeter", c_int32),
        ("biClrUsed", c_uint32),
        ("biClrImportant", c_uint32),
     ]

    def __init__(self, width = 0, height = 0, depth = 4, clrs = 16):
        self.biSize = 40  # 4
        self.biWidth = width  # 4
        self.biHeight = height  # 4
        self.biPlanes = 1  # 2
        self.biBitCount = depth  # 2
        self.biCompression = 0  # 4
        self.biSizeImage = 0 # 4
        self.biXPixPerMeter = 0  # 4
        self.biYpixPerMeter = 0  # 4
        self.biClrUsed = clrs  # 4
        self.biClrImportant = 0  # 4

    def __repr__(self):
       return 'BitmapInfoHeader\n' +'biSize:' + str(self.biSize) + '\n' + 'biWidth:' + str(self.biWidth) + '\n' + 'biHeight:' + str(self.biHeight) + '\n' + 'biBitCount:' + str(self.biBitCount) + '\n' + 'biClrUsed:' + str(self.biClrUsed) + '\n' + 'biCompression:' + str(self.biCompression) + '\n' + 'biSizeImage:' + str(self.biSizeImage)


class RGBQUAD(LittleEndianStructure):
    _pack_ = 2
    _fields_ = [
        ("rgbBlue", c_uint8),
        ("rgbGreen", c_uint8),
        ("rgbRed", c_uint8),
        ("rgbReserved", c_uint8),
    ]

    def __init__(self, r = 0, g = 0, b = 0):
        self.rgbBlue = b;
        self.rgbGreen = g;
        self.rgbRed = r;
        self.rgbReserved = 0;

    def __hash__(self):
#        return hash((self.rgbBlue, self.rgbGreen, self.rgbRed, self.rgbReserved)) # tuple is hashable
        return self.b * 65536 + self.g * 256 + self.r # for compare

    def __eq__(self, other):
        if not isinstance(other, RGBQUAD):
            return NotImplemented
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, RGBQUAD):
            return NotImplemented
        return hash(self) < hash(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __repr__(self):
        return '(' + str(self.rgbRed) + ',' + str(self.rgbGreen) + ',' + str(self.rgbBlue) + ')'

    @property
    def r(self):
        return self.rgbRed

    @r.setter
    def r(self, v):
        self.rgbRed = v

    @property
    def g(self):
        return self.rgbGreen

    @g.setter
    def g(self, v):
        self.rgbGreen = v

    @property
    def b(self):
        return self.rgbBlue

    @b.setter
    def b(self, v):
        self.rgbBlue = v


# BMP3 format
class Bitmap():
    def __init__(self, width = 1, height = 1, depth = 4, clrs = 16):
        self.file_header = BITMAPFILEHEADER(width, height, depth, clrs)
        self.info_header = BITMAPINFOHEADER(width, height, depth, clrs)
        self.palettes = [None] * clrs;
        self.data = array.array('B', [0] * self.info_header.biSizeImage)
        

    def __repr__(self):
        return str(self.file_header) + '\n' + str(self.info_header) + '\n' + str([ x for x in self.palettes ])

    @staticmethod
    def __read_header(bf):
        bfh = BITMAPFILEHEADER()
        bf.readinto(bfh)
        bih = BITMAPINFOHEADER()
        bf.readinto(bih)

        palettes = list()
        for i in range(bih.biClrUsed):
            rgb = RGBQUAD()
            bf.readinto(rgb)
            palettes.append(rgb)

        return bfh, bih, palettes
        
    @staticmethod
    def read_header(bpath):
        with open(bpath, 'rb') as f:
            return Bitmap.__read_header(f)

    def read(self, bpath):
        with open(bpath, 'rb') as f:
            self.file_header, self.info_header, self.palettes = Bitmap.__read_header(f)
            if not self.file_header.valid():
                return False

            self.data = array.array('B')
            f.seek(self.file_header.bfOffBits)
            self.data.fromfile(f, self.info_header.biSizeImage)
        return True

    def write(self, bpath):
        with open(bpath, 'wb') as f:
            f.write(self.file_header)
            f.write(self.info_header)
            for i in range(self.info_header.biClrUsed):
                f.write(self.palettes[i])
            self.data.tofile(f)
        return True


