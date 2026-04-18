from classes import *
from classes2 import *
from functions import *
from readFile import read
from writeFile import write

lvl = read("1.txt")
outLvl = outLevel(lvl)

speed = 0

wheel = wheel(lvl.tyres.medium, lvl.weather.conditions[0].condition, lvl.car.crawl_constant)

for lapNum, lap in enumerate(outLvl.laps):
    for segNum, seg in enumerate(lap.segments):
        nextSeg = lvl.track.segments[(segNum+1)%len(lap.segments)]

        if seg.type == "corner":
            continue

        if nextSeg.type == "corner":
            maxSpeed = wheel.getMaxCornerSpeed(nextSeg.radius)
            


write("output.txt", outLvl)