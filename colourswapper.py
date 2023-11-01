import os
import png
import glob
from os.path import exists


colordict = {}


inpal =png.Reader("pal_in.png")
outpal=png.Reader("pal_out.png")
_,_,inrows,_ = inpal.asRGBA()
_,_,outrows,_ = outpal.asRGBA()

inl = list(inrows)
outl = list(outrows)

for y in range(11, 354, +22):
    for x in range(5*4, (481*4), +(30*4)):
        inpix =  (inl[y][x], inl[y][x+1], inl[y][x+2])
        outpix = [outl[y][x],outl[y][x+1],outl[y][x+2]]
        colordict[inpix] = outpix



colordictprint = "\n".join("{0} {1}".format(k, v)  for k,v in colordict.items())
print(colordictprint)

for infilename in glob.iglob("in/" + '**/*.png', recursive=True):
    outfilename = "out" + infilename[2:]
    maskfilename = "mask" + infilename[2:]
    print(outfilename)

    r=png.Reader(infilename)
    w,h,rows,info = r.asRGBA()

    # values per row
    vpr = 4 * w

    # Create a 2D matrix, a sequence of rows. Each row has vpr values.
    m = [[0] * vpr for y_ in range(h)]

    mask_exists = exists(maskfilename)
    if(mask_exists):
        mask=png.Reader(maskfilename)
        _,_,maskrows,_ = mask.asRGBA()
        maskl = list(maskrows)

    rowno = 0
    for row in rows:
        
        l = list(row)
        
        for i in range(0, len(l), +4):
            if l[i+3] == 255:

                inpix =  (l[i], l[i+1], l[i+2])
                
                if mask_exists and maskl[rowno][i+3] == 0:
                    outpix = inpix
                else:
                    outpix = colordict[inpix]

                m[rowno][i]  =outpix[0]
                m[rowno][i+1]=outpix[1]
                m[rowno][i+2]=outpix[2]
                m[rowno][i+3]=255

            else:
                m[rowno][i+3]=0
                
        rowno += 1


    os.makedirs(os.path.dirname(outfilename), exist_ok=True)
    png.from_array(m, "RGBA").save(outfilename)