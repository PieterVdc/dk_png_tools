import os
import png
import glob

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
w = 32 * 8
vpr = 4 * w

for infilename in glob.iglob("in/" + '**/*.*', recursive=True):
    try:
        with open(infilename, "rb") as f:
            data = f.read()

        if len(data) <= offset:
            continue

        pixel_data = data[offset:]
        rows = (len(pixel_data) + w - 1) // w
        m = [[0] * vpr for _ in range(rows)]

        for k, value in enumerate(pixel_data):
            outpix = colordict.get(value)
            row = k // w
            col = (k % w) * 4

            if outpix is None:
                m[row][col] = 0
                m[row][col + 1] = 0
                m[row][col + 2] = 0
                m[row][col + 3] = 0
            else:
                m[row][col] = outpix[0]
                m[row][col + 1] = outpix[1]
                m[row][col + 2] = outpix[2]
                m[row][col + 3] = 255

        relname = os.path.relpath(infilename, "in")
        outfilename = os.path.join("out", relname + ".png")
        os.makedirs(os.path.dirname(outfilename), exist_ok=True)
        png.from_array(m, "RGBA").save(outfilename)
    except IOError:
        print('Error While Opening the file!')  

