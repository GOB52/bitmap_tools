# bitmap_tools
Tools for Windows bitmap (Windows V3 format) or any images by ***Python3***.  
[日本語/Japanese](README.ja.md)

## Overview
I will publish the scripts I needed to create my game on M5Stack.

## Tools
### reorder\_palette.py
Reorder and combine palette colors for 16 colors (4bit depth) bitmap.  

- If not exists transpalent color ***RGB(255,0,255)*** then add to bitmap.
- Combine the same colors into one. If the result is less than 16 colors, it is padded.
- Sort palettes ascending by RGB, ***However the index of transparent color is fixed at 0***
- Output bitmap that reordered palette colors applied.

#### usage
python3 reorder\_palette.py src\_bitmap.bmp dest\_bitmap.bmp 

### make\_lgfxbmpfont.py
Output C style source to stdout in GFXfont, FixedBMPfont, and GLCDfont format.  
**(Only monospaced font.)**  

- You can specify image files supported by the Pillow.
- Load image and ***binarize***.
- Crop to the size specified by the argument
- Output to stdout as if starting from the code specified by the argument.
- It can be displayed in [LovyanGFX](https://github.com/lovyan03/LovyanGFX) or any library that supports font output.

#### See also
[LovyanGFX v0](https://github.com/lovyan03/LovyanGFX/blob/c8b09ac1cbf2f9183de432172134470dbd29eb71/src/lgfx/v1/lgfx_fonts.hpp)  
[LovyanGFX v1](https://github.com/lovyan03/LovyanGFX/blob/de8dd6352ebd68abc5884cb4a004711229400224/src/lgfx/v0/lgfx_fonts.hpp)

#### require
[Pillow](https://pillow.readthedocs.io/en/stable/)  
[numpy](https://numpy.org/)

#### usage
python3 make\_lgfxbmpfont.py src\_image_path -width 8 -height 8 --name example --code 32 > example\_font.h

output example(--format GFX)  
```c
const uint8_t example_bitmaps[] PROGMEM = {
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,	// ' '
    0x1c,0x1c,0x1c,0x18,0x18,0x00,0x18,0x00,	// '!'
    0x36,0x36,0x24,0x00,0x00,0x00,0x00,0x00,	// '"'
.
.
.

};
const GFXglyph example_glyphs[] PROGMEM = {
    { 0, 8, 8, 8, 0, -8 },	//' '
    { 8, 8, 8, 8, 0, -8 },	//'!'
    { 16, 8, 8, 8, 0, -8 },	//'"'
.
.
.

};
const GFXfont example_font PROGMEM = {
 (uint8_t*)example_bitmaps, (GFXglyph*)example_glyphs, 0x20, 0x5f, 8 };
```

## Utilities
### gob_bitmap.py
Windows bitmap accessor.  
reorder\_palette.py use the gob_bitmap.py.

### Remarks
[Windows V3 BITMAPINFOHEADER](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapinfoheader)  

If you want to convert format of images. see also 
[ImageMagic](https://github.com/ImageMagick/ImageMagick)


