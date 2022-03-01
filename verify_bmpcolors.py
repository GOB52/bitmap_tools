#! /usr/bin/env python3
#
# Verify that the number of colors in the Bitmap is as specified.
#
#
import sys
import argparse
import pprint as p

#from relpath import add_import_path
#add_import_path("../modules")
from gob_bitmap import Bitmap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bitmap_path', help='bitmap path')
    parser.add_argument('colors', help='check bitmap colors', type=int)
    parser.add_argument('-d', '--depth', type=int, help='check color depth')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    bfh, bih, palettes = Bitmap.read_header(args.bitmap_path)

    if args.verbose:
        p.pprint(bfh)
        p.pprint(bih)
        p.pprint(palettes)
        p.pprint('args.colors:' + str(args.colors))

    if not bfh.valid():
        p.pprint('Not bitmap file:' + args.bitmap_path)

    verify = bfh.valid() and bih.biClrUsed == args.colors
    if args.depth:
        verify &= (bih.biBitCount == args.depth)

    print( 'OK' if verify else 'NG')

    return 0 if verify else -1
        
if __name__ == "__main__":
    sys.exit(main())
