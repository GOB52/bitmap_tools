#! /usr/bin/env python3
#
#  Reorder and combine palettes for 16colors(4bit) bitmap
#  Palette index:0 transparent color, 1~15 sort by RGB asend.
#
import sys
import argparse
import pprint as p

#from relpath import add_import_path
#add_import_path("../modules")
from gob_bitmap import *

TRANS_CLR = RGBQUAD(255,0,255) # Must be index  0
PADDING = RGBQUAD(52,52,52)

#
# Combine same clr and reorder BGR asend
# (padding if length less than 16)
# opals list[RGBQUAD,...]
def reorder_palette(opals, verbose = False):

    palsz = len(opals)
    pals = opals[:] # copy

    pals.insert(0, TRANS_CLR) # Must need transparent palette
    uniq = list(dict.fromkeys(pals)) # to uniqued
    npals = [uniq[0]] + sorted(uniq[1:]) # Sort that keep TRANS_CLR index

    for i in range(16 - len(npals)):
        npals.append(PADDING)

    if verbose:
        print('reorderd palette')
        p.pprint(npals)

    return npals if len(npals) <= 16 else RuntimeError("Illegal palette size")

#
# Make convert table from old to new palettes
# opal [RGBQUAD,...]
# npal [RGBAUAD...]
# out[n,...] 
def make_convert_table(opal, npal, verbose = False):
    tbl = []
    d = dict(zip(npal, range(len(npal))))

    for rgb in opal:
        tbl.append(d[rgb])
    if verbose:    
        print('convert table:' + str(len(tbl)) )
        p.pprint(tbl)

    return tbl

#
# Convert pixel to reordered palettes
#
def convert_pixels(bmp, tbl, verbose = False):

    pd = array.array('B', [0] * len(bmp.data))

    for i in range(len(bmp.data)):
        pd[i] = tbl[bmp.data[i] >> 4] << 4 |   tbl[bmp.data[i] & 0x0f]
        if verbose and i < 64:
            p.pprint(hex(pd[i]) + ':' +  hex(bmp.data[i]))

    return pd;


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_path', help='src bitmap path')
    parser.add_argument('out_path', help='dest bitmap path')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    bmp = Bitmap()
    if not bmp.read(args.in_path):
        print('Failed to read in_path')
        return -1

    if args.verbose:
        print("input bitmap info");
        p.pprint(bmp)

    if not bmp.file_header.valid() or not bmp.info_header.biSize == 40 or bmp.info_header.biBitCount != 4 or bmp.info_header.biClrUsed != 16:
        print('bitmap must be 4bit color bitmap3 format(biSize==40)')
        return -2

    npals = reorder_palette(bmp.palettes, args.verbose)
    table = make_convert_table(bmp.palettes, npals, args.verbose)
    npixels = convert_pixels(bmp, table, args.verbose)

    bmp.palettes = npals
    bmp.data = npixels
    bmp.write(args.out_path)

    return 0

if __name__ == "__main__":
    sys.exit(main())



