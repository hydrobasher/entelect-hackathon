from classes import *
from classes2 import *
from readFile import read
from writeFile import write

lvl = read("1.txt")
outLvl = outLevel(lvl)

speed = 0

for lapNum, lap in enumerate(outLvl.laps):
    for segNum, seg in enumerate(lap.segments):
        nextSeg = lap.segments[(segNum+1)%len(lap.segments)]

        if seg.type == "corner":
            continue

        if nextSeg.type == "corner":
            
            


write("output.txt", outLvl)