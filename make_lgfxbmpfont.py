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
    parser = argparse.ArgumentParser(description='Output C style source to stdout in GFXfont, FixedBMPfont, and GLCDfont format from image')
    parser.add_argument('src_path', help='image path')
    parser.add_argument('--width',  type=int, required=True, help='font width')
    parser.add_argument('--height', type=int, required=True, help='font height')
    parser.add_argument('--name', type=str, help='font name')
    parser.add_argument('--code', type=int, default=32, help='Start of character code (32 as default)') # 0x20(white space) as default
    parser.add_argument('--format', type=str, default='GFX', choices=['GFX','BMP', 'GLCD'], help='output format (GFX as default)')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()

    img = Image.open(args.src_path).convert(mode='1')
    width, height = img.size
    if args.verbose:
        print('image size {}:{} / font {}:{}'.format(width, height, args.width, args.height))

    glist = []

    if height//args.height == 0 or width//args.width == 0:
        print('A width or height greater than the size of the image was specified. image:({}:{})'
              .format(width, height))
        return -1
    
    for y in range(height//args.height):
        for x in range(width//args.width):
            rect = (x * args.width, y * args.height, (x + 1) * args.width, (y + 1) * args.height)
            g = img.crop(rect)
            if args.format == 'GLCD':
                g = g.rotate(270)
            ng = np.array(g.getdata())
            ng.shape = args.height, args.width
            glist.append(ng)
            if args.verbose:
                p.pprint(ng)

    name = args.name
    if not name:
        name = os.path.splitext(os.path.basename(args.src_path))[0]
        
    print_image(name, glist, args.height, args.code)

    if args.format == 'GFX':
        print_glyph(name, glist, args.width, args.height, args.code)
        print('const GFXfont {}_font PROGMEM = {{ (uint8_t*){}_bitmaps, (GFXglyph*){}_glyphs, 0x{:x}, 0x{:x}, {} }};'
              .format(name, name, name, args.code, args.code + len(glist) - 1, args.height))

    elif args.format in {'BMP', 'GLCD'}:
        print('const std::uint8_t {}_font_info[] PROGMEM = {{ 0x{:x}, 0x{:x}, {} }};\n'
              .format(name, args.code, args.code + len(glist) - 1, args.width))

        if args.format == 'BMP':
            print('const FixedBMPfont {}_font PROGMEM = {{ {}_bitmaps, {}_font_info, {}, {}, {} }};\n'
                  .format(name, name, name, args.width, args.height, args.height - 1))

        elif args.format == 'GLCD':
            print('const GLCDfont {}_font PROGMEM = {{ {}_bitmaps, {}_font_info, {}, {}, {} }};\n'
                  .format(name, name, name, args.width, args.height, args.height - 1))

    return 0

if __name__ == '__main__':
    sys.exit(main())
