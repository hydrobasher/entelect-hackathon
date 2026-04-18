from classes import *
from classes2 import *
from functions import *
from readFile import read
from writeFile import write

lvl = read("1.txt")
outLvl = outLevel(lvl)

speed = 0

myWheel = wheel(lvl.tyres.medium, lvl.weather.conditions[0].condition, lvl.car.crawl_constant)
myVehicle = vehicle(lvl.car)

for lapNum, lap in enumerate(outLvl.laps):
    for segNum, seg in enumerate(lap.segments):
        nextSeg = lvl.track.segments[(segNum+1)%len(lap.segments)]

        if seg.type == "corner":
            continue

        if nextSeg.type == "corner":
            maxSpeed = myWheel.getMaxCornerSpeed(nextSeg.radius)
            
            L = myVehicle.accelerateOverStraight(lvl.track.segments[segNum].length, maxSpeed)
            seg.target_ms = myVehicle.car.max_speed
            seg.brake_start_m_before_next = L    

write("output.txt", outLvl)