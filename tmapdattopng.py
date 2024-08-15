import math
import os
import png
import glob
from os.path import exists

#struct TbColorTables {
#  unsigned char fade_tables[64*256];
#  unsigned char ghost[256*256];
#  unsigned char flat_colours_tl[2*256];
#  unsigned char flat_colours_tr[2*256];
#  unsigned char flat_colours_br[2*256];
#  unsigned char flat_colours_bl[2*256];
#  unsigned char robs_bollocks[256];
#};

colordict = {}

barr = bytearray(b'')

inpal =png.Reader("pal_in.png")
_,_,inrows,_ = inpal.asRGBA()

inl = list(inrows)

pal_idx = 0

for y in range(11, 354, +22):
    for x in range(5*4, (481*4), +(30*4)):
        inpix =  (inl[y][x], inl[y][x+1], inl[y][x+2])
        colordict[pal_idx] = inpix
        pal_idx +=1

offset = 0
w=32*8

vpr = 4 * w

m = [[0] * vpr for y_ in range(128)]

i = 0
for infilename in glob.iglob("in/" + '**/*.*', recursive=True):
    try:
        with open(infilename, "rb") as f:
            byte = f.read(1)
            while byte:
                if (i >= offset):
                    k = i - offset
                    #outpix = colordict[byte]

                    outpix = colordict.get(int.from_bytes(byte, "big"))
                    row = math.floor(k/256)
                    try:
                        if (outpix == None):
                            m[row][k%w*4]  = 0
                            m[row][k%w*4+1]= 0
                            m[row][k%w*4+2]= 0
                            m[row][k%w*4+3]= 0
                        else:
                            m[row][k%w*4]  =outpix[0]
                            m[row][k%w*4+1]=outpix[1]
                            m[row][k%w*4+2]=outpix[2]
                            m[row][k%w*4+3]=255
                    except IOError:
                        print('meh')
                i +=1
                if (i >= os.path.getsize(infilename)):
                    break

                
                byte = f.read(1)
                #print(byte
        outfilename = "out" + infilename[2:] + ".png"
        png.from_array(m, "RGBA").save(outfilename)
    except IOError:
        print('Error While Opening the file!')  

