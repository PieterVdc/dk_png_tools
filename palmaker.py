import png



barr = bytearray(b'')



outpal=png.Reader("pal_out.png")
_,_,outrows,_ = outpal.asRGBA()

outl = list(outrows)

for y in range(11, 354, +22):
    for x in range(5*4, (481*4), +(30*4)):
        barr.append(outl[y][x])
        barr.append(outl[y][x+1])
        barr.append(outl[y][x+2])


b_arr = bytes(barr)

with open("testpal.pal", "wb") as f:
    f.write(b_arr)