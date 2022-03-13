# bitmap_tools
Tools for Windows bitmap (Windows V3 format) by Python3.

## Overview
I will publish the tools I needed to create my game on M5Stack.

## Tools
### reorder_palette.py
Reorder and combine palette colors for 16 colors (4bit depth) bitmap.  

- If not exists transpalent color ***(RGB(255,0,255)*** then add to bitmap.
- Combine the same colors into one. If the result is less than 16 colors, it is padded.
- Sort palettes ascending by RGB, ***However the index of transparent color is fixed at 0***
- Output bitmap that has reordered palette colors.

#### Usage
python3 reorder\_palette.py src\_bitmap.bmp dest\_bitmap.bmp 

## Utilities
### gob_bitmap.py
Windows bitmap accessor.  
reorder\_palette.py use the gob_bitmap.py.

### Remarks
[Windows V3 BITMAPINFOHEADER](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapinfoheader)  

If you want to convert format of images. see also 
[ImageMagic](https://github.com/ImageMagick/ImageMagick)


