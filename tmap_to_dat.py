import os
import png
import glob
from os.path import exists


colordict = {}

barr = bytearray(b'')

inpal =png.Reader("pal_in.png")
outpal=png.Reader("pal_out.png")
_,_,inrows,_ = inpal.asRGBA()
_,_,outrows,_ = outpal.asRGBA()

inl = list(inrows)
outl = list(outrows)

pal_idx = 0

for y in range(11, 354, +22):
    for x in range(5*4, (481*4), +(30*4)):
        inpix =  (inl[y][x], inl[y][x+1], inl[y][x+2])
        colordict[inpix] = pal_idx
        pal_idx +=1



for infilename in glob.iglob("in/" + '**/*.png', recursive=True):
    outfilename = "out" + infilename[2:][:-4] + ".dat"
    print(outfilename)

    r=png.Reader(infilename)
    w,h,rows,info = r.asRGBA()

    # values per row
    vpr = 4 * w

    # Create a 2D matrix, a sequence of rows. Each row has vpr values.
    m = [[0] * vpr for y_ in range(h)]


    rowno = 0
    for row in rows:
        l = list(row)
        for i in range(0, len(l), +4):
            inpix =  (l[i], l[i+1], l[i+2])
            outpx_idx = colordict.get(inpix)
            if (outpx_idx == None):
                outpx_idx = 255
            barr.append(outpx_idx)
                
        rowno += 1
    b_arr = bytes(barr)
    os.makedirs(os.path.dirname(outfilename), exist_ok=True)
    with open(outfilename, "wb") as f:
        f.write(b_arr)

    os.makedirs(os.path.dirname(outfilename), exist_ok=True)