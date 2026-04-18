import math

# Constants from specs
GRAVITY = 9.8
K_BASE_FUEL = 0.0005
K_DRAG_FUEL = 0.0000000015
K_STRAIGHT_DEG = 0.0000166
K_BRAKING_DEG = 0.0398
K_CORNER_DEG = 0.000265

# Base friction coefficients
BASE_FRICTIONS = {
    "Soft": 1.8,
    "Medium": 1.7,
    "Hard": 1.6,
    "Intermediate": 1.2,
    "Wet": 1.1,
}


def max_corner_speed(typeFriction, radias, crawl_constant):
    return math.sqrt(GRAVITY * radias * BASE_FRICTIONS[typeFriction]) + crawl_constant


def total_straight_degredation(tyreDegredations, segmentLength, kStraight):
    return kStraight * (tyreDegredations) * segmentLength


# degredation rate depends on tire itself
def degredation_while_breaking(initSpeed, finalSpeed, kBreaking, tyreDegredations):
    return (
        kBreaking
        * tyreDegredations
        * ((initSpeed / 100) ** 2 - (finalSpeed / 100) ** 2)
    )


def total_corner_degredation(tyreDegredations, radius, kCorner, speed):
    return kCorner * (tyreDegredations) * (speed) ** 2 / radius


def tyre_friction(frictionCoeff, totalDegredation, weatherMultiplier):
    return (frictionCoeff - totalDegredation) * weatherMultiplier


def fuel_usage(kBase, kDrag, initSpeed, finalSpeed, distance):
    return (kBase + kDrag * ((initSpeed + finalSpeed) / 2) ** 2) * distance


def pitstop_refuel(amount, rate):
    return amount / rate


def pitstop_time(refuelTime, pitTyreSwapTime, basePitStopType):
    return refuelTime + pitTyreSwapTime + basePitStopType


# scoring
def base_score(timeReference, time):
    return 500000 * (timeReference / time) ** 3


def level2n3Score(fuelUsed, fuelSoftCap, timeReference, time):
    return (
        base_score(timeReference, time)
        + -500000 * (1 - fuelUsed / fuelSoftCap) ** 2
        + 500000
    )


# def level4Score(tyreDegredations, numberOfBlowouts, timeReference, time):
#     tyreBonus =
#     return base_score(timeReference, time) + tyreBonus
