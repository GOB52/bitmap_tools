# bitmap_tools
Window bitmap(Windows V3 フォーマット)やイメージの為のツール群 (***要Python3***)

## 概要
M5Stackでゲームを作る為に私が必要なツールを公開します。

## Tools
### reorder\_palette.py
16色ビットマップ(4bitカラー)のパレットを並び替えます。

- 透過色がなければ ***RGB(255,0,255)*** を透過色として追加します。
- 同色パレットをまとめて一つのパレットにまとめます。その結果16色に満たなくなった場合は穴埋めされます。
- RGB昇順に並び替えます。***ただし透過色はパレットインデックス0番固定とします。***
- 並び替えたパレットが適用されたビットマップを出力します。

#### 使い方
python3 reorder\_palette.py src\_bitmap.bmp dest\_bitmap.bmp 

### make\_lgfxbmpfont.py
イメージを、C言語スタイルの [LovyanGFX](https://github.com/lovyan03/LovyanGFX) GFXfont フォーマットに変換し標準出力へ出力します。  
***等幅フォントとしてのみ***

参照
[LovyanGFX v0](https://github.com/lovyan03/LovyanGFX/blob/c8b09ac1cbf2f9183de432172134470dbd29eb71/src/lgfx/v1/lgfx_fonts.hpp)
[LovyanGFX v1](https://github.com/lovyan03/LovyanGFX/blob/de8dd6352ebd68abc5884cb4a004711229400224/src/lgfx/v0/lgfx_fonts.hpp)

- Pillowがサポートする画像を指定することができます。
- イメージを読み込み2値化します。
- 引数で指定した大きさで切り取ります。
- 引数で指定した文字コードから始まるものとして出力します。

#### 必要なもの
[Pillow](https://pillow.readthedocs.io/en/stable/)  
[numpy](https://numpy.org/)

#### 使い方
python3 make\_lgfxbmpfont.py src\_image_path -w8 -h8 --name example --code 32 > example\_font.h

出力例
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

## ユーティリティ
### gob_bitmap.py
Windowsビットマップのアクセッサ  
reorder\_palette.py にて使用しています。

### 備考
[Windows V3 BITMAPINFOHEADER](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapinfoheader)  

イメージフォーマットの変換をしたい場合はこちら
[ImageMagic](https://github.com/ImageMagick/ImageMagick)


