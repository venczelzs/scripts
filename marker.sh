#! /bin/sh

DIR="../PSNEPTANCGALA"
OUT="../PSNEPTANCGALAKESZ"
WIDTH=650
FONT="/usr/share/fonts/truetype/noto/NotoSans-BoldItalic.ttf"
TEXT="Fotó: Köves Szilvia"
SIZE=50
OPACITY=50
COLOR="(220, 220, 220, 80)"

python marker.py -d "$DIR" -w "$WIDTH" -f "$FONT" -s "$SIZE" -c "$COLOR" -o "$OPACITY" -O "$OUT" -t "$TEXT"
