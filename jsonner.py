import json
import os
import re 

prefix = os.path.dirname(os.path.realpath(__file__))
prefix = prefix.split("\\")[-1].upper()
prefix += "_" 

#remove to have it perfix with foldername, set manually or leave empty
prefix = ""

data = []
tdarr = []
fparr = []

#for infilename in glob.iglob('**/*.png', recursive=False):
for subdir, dirs, files in os.walk("."):
    if subdir == ".":
        continue
    
    if subdir.endswith("_fp"):
        tdfp = "fp"
    elif subdir.endswith("_td"):
        tdfp = "td"
    else:
        tdfp = "both"


    anim = subdir.replace(subdir[:2], '')


    if subdir.endswith("_fp") or subdir.endswith("_td"):
        if subdir.endswith("_fp"):
            tdarr = []
            fparr = []
            fp_offset_x = 999
            fp_offset_y = 999
            td_offset_x = 999
            td_offset_y = 999
    else:
        tdarr = []
        fparr = []
        fp_offset_x = 999
        fp_offset_y = 999
        td_offset_x = 999
        td_offset_y = 999
            
    if tdfp == "fp" or tdfp == "td":
        name = prefix + anim[:-3].upper()
    else:
        name = prefix + anim.upper()


    rotatable = any(ch.startswith("r2") for ch in files)
    r1 = []
    r2 = []
    r3 = []
    r4 = []
    r5 = []

    for file in files:
        if file.startswith("r1"):
            r1.append({"file":anim + "/" + file})
        elif file.startswith("r2"):
            r2.append({"file":anim + "/" + file})
        elif file.startswith("r3"):
            r3.append({"file":anim + "/" + file})
        elif file.startswith("r4"):
            r4.append({"file":anim + "/" + file})
        elif file.startswith("r5"):
            r5.append({"file":anim + "/" + file})
        elif file.startswith("filelist"):
            with open(subdir + "/" + file) as f:
                first_line = f.readline()
                first_line = re.sub(' +', ' ',first_line).rstrip()
                offsets = first_line.split(" ")
                if tdfp == "fp" or tdfp == "both":
                    fp_offset_x = -int(offsets[-2])
                    fp_offset_y = -int(offsets[-1])
                if tdfp == "td" or tdfp == "both":
                    td_offset_x = -int(offsets[-2])
                    td_offset_y = -int(offsets[-1])
                

        else:
            print("unrecognised file " + file)
    
    if tdfp == "fp" or tdfp == "both":
        fparr.append(r1)
        if r2:
            fparr.append(r2)
            fparr.append(r3)
            fparr.append(r4)
            fparr.append(r5)
    

    if tdfp == "td" or tdfp == "both":
        tdarr.append(r1)
        if r2:
            tdarr.append(r2)
            tdarr.append(r3)
            tdarr.append(r4)
            tdarr.append(r5)

    if rotatable:
        if len(r1) != len(r2) \
        or  len(r1) != len(r3) \
        or  len(r1) != len(r4) \
        or  len(r1) != len(r5):
            print("rotation counts not matching %d,%d,%d,%d,%d",len(r1),len(r2),len(r3),len(r4),len(r5))

        
    if tdfp == "td" or tdfp == "both":
        data.append({"name": name,
                 "rotatable": rotatable,
                 "fp_offset_x": fp_offset_x,
                 "fp_offset_y": fp_offset_y,
                 "td_offset_x": td_offset_x,
                 "td_offset_y": td_offset_y,
                 "fp":fparr,
                 "td":tdarr})

	

	
with open("sprites.json", "w") as write_file:
    json.dump(data, write_file, indent=4)
