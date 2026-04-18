from classes import *
from classes2 import *
from functions import *
from readFile import read
from writeFile import write

def kirk(levelNumber, wheelTypeId):
    lvl = read(f"{levelNumber}.txt")
    outLvl = outLevel(lvl)

    wheelType = None
    if wheelTypeId == "soft":
        wheelType = lvl.tyres.soft
    elif wheelTypeId == "medium":
        wheelType = lvl.tyres.medium
    elif wheelTypeId == "hard":
        wheelType = lvl.tyres.hard
    elif wheelTypeId == "intermediate":
        wheelType = lvl.tyres.intermediate
    elif wheelTypeId == "wet":
        wheelType = lvl.tyres.wet

    myWheel = wheel(wheelType, lvl.weather.conditions[0].condition, lvl.car.crawl_constant)
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

        # lap.pit.enter = True

    write(f"lvl{levelNumber}-{wheelTypeId}.txt", outLvl)