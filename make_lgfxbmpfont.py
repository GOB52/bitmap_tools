#! /usr/bin/env python3
#
# Image to C source style for LovyanGFX GFXfont format.
#
#
import os
import sys
import argparse
import numpy as np
from PIL import Image
import pprint as p

def print_byte(data):
    v = 0
    for idx, d in enumerate(data):
        if idx > 0 and idx % 8 == 0:
            print('0x{:02x},'.format(v),end='')
            v = 0
        v |= (d & 1) << (7-(idx % 8))
    print('0x{:02x},'.format(v),end='')

    
def print_image(name, glist, height, code = 0x20):
    ch = code
    print('const uint8_t {}_bitmaps[] PROGMEM = {{'.format(name))

    for g in glist:
        print('    ',end='')
        for y in range(height):
            h = g[y]
            print_byte(h)
        print('\t// \'%c\'' % ch)
        ch = ch + 1

    print('};')
        

def print_glyph(name, glist, width, height, code = 0x20):
    ch = code
    print('const GFXglyph {}_glyphs[] PROGMEM = {{'.format(name))
    off = 0
    for g in glist:
        print('    {{ {}, {}, {}, {}, {}, {} }},\t//\'{:c}\'\n'.format(off, width, height, width, 0, -height, ch), end='')
        ch = ch + 1
        off += width // 8 * height;

    print('};')

        
def main():
    parser = argparse.ArgumentParser(description='Image to C source style for LovyanGFX GFXfont format.')
    parser.add_argument('src_path', help='image path')
    parser.add_argument('--width', '-w', type=int, required=True, help='font width')
    parser.add_argument('--height', '-h', type=int, required=True, help='font height')
    parser.add_argument('--name', type=str, help='font name')
    parser.add_argument('--code', type=int, default=32, help='Start of character code') # 0x20(white space) as default
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()

    img = Image.open(args.src_path).convert(mode='1')
    width, height = img.size
    if args.verbose:
        print('bitmap size {}:{} / font {}:{}'.format(width, height, args.width, args.height))

    glist = []
        
    for y in range(height//args.height):
        for x in range(width//args.width):
            rect = (x * args.width, y * args.height, (x + 1) * args.width, (y + 1) * args.height)
            g = img.crop(rect)
            ng = np.array(g.getdata())
            ng.shape = args.height, args.width
            glist.append(ng)
            if args.verbose:
                p.pprint(ng)

    name = args.name
    if not name:
        name = os.path.splitext(os.path.basename(args.src_path))[0]
        
    print_image(name, glist, args.height, args.code)
    print_glyph(name, glist, args.width, args.height, args.code)

    print('const GFXfont {}_font PROGMEM = {{\n (uint8_t*){}_bitmaps, (GFXglyph*){}_glyphs, 0x{:x}, 0x{:x}, {} }};'
           .format(name, name, name, args.code, args.code + len(glist) - 1, args.height))
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
