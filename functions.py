import math

from classes import *

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

class wheel:
    def __init__(self, tyre, weather_condition, crawl_constant):
        self.tyre = tyre
        self.life_span = tyre.life_span
        self.degredation = 0
        self.weather_condition = weather_condition
        self.crawl_constant = crawl_constant

    def getWeatherMultiplier(self):
        if self.weather_condition == "dry":
            return self.tyre.dry_friction_multiplier
        elif self.weather_condition == "cold":
            return self.tyre.cold_friction_multiplier
        elif self.weather_condition == "light rain":
            return self.tyre.light_rain_friction_multiplier
        elif self.weather_condition == "heavy rain":
            return self.tyre.heavy_rain_friction_multiplier
        else:
            raise ValueError("Unknown weather condition multiplier")
        
    def getWeatherDegredation(self):
        if self.weather_condition == "dry":
            return self.tyre.dry_degradation
        elif self.weather_condition == "cold":
            return self.tyre.cold_degradation
        elif self.weather_condition == "light rain":
            return self.tyre.light_rain_degradation
        elif self.weather_condition == "heavy rain":
            return self.tyre.heavy_rain_degradation
        else:
            raise ValueError("Unknown weather condition degredation")

    def friction(self):
        return (BASE_FRICTIONS[self.tyre.name] - self.degredation) * self.getWeatherMultiplier()
    
    def degradeStraight(self, segmentLength):
        self.degredation += K_STRAIGHT_DEG * segmentLength * self.getWeatherDegredation()

    def degradeBraking(self, initSpeed, finalSpeed):
        self.degredation += K_BRAKING_DEG * self.getWeatherDegredation() * ((initSpeed / 100) ** 2 - (finalSpeed / 100) ** 2)

    def degradeCorner(self, radius, speed):
        self.degredation += K_CORNER_DEG * self.getWeatherDegredation() * (speed ** 2 / radius)

    def getMaxCornerSpeed(self, radius):
        return math.sqrt(GRAVITY * radius * self.friction()) + self.crawl_constant
    
class vehicle:
    def __init__(self, car):
        self.car = car
        self.speed = 0
        self.fuel = car.initial_fuel

    def accelerateOverStraight(self, length, v_limit=None):
        # 1. Handle default v_limit
        if v_limit is None:
            v_limit = self.car.max_speed

        # Using positive values for magnitudes to match your formula:
        a_plus = self.car.accel
        a_minus = -self.car.brake  # Convert braking magnitude to negative acceleration
        v0 = self.speed
        
        # 2. Calculate the theoretical distance to start braking (d_1)
        # Formula: d1 = (v_lim^2 - v0^2 - 2*a_minus*L) / (2 * (a_plus - a_minus))
        numerator = (v_limit**2 - v0**2 - 2 * a_minus * length)
        denominator = 2 * (a_plus - a_minus)
        d_1 = numerator / denominator

        # --- EDGE CASE: v_limit is so high we never need to brake ---
        if d_1 >= length:
            # Accelerate for the whole length
            final_v_sq = v0**2 + 2 * a_plus * length
            self.speed = min(math.sqrt(final_v_sq), self.car.max_speed)
            return length # Still accelerating at the very end

        # 3. Calculate the peak speed reached at d_1
        v_peak_sq = v0**2 + 2 * a_plus * d_1
        v_peak = math.sqrt(max(0, v_peak_sq)) # max(0...) prevents tiny precision errors

        # 4. Handle hitting v_max ceiling
        if v_peak > self.car.max_speed:
            v_peak = self.car.max_speed
            # Distance to reach v_max
            d_accel = (v_peak**2 - v0**2) / (2 * a_plus)
            # Distance required to brake from v_max to v_limit
            d_brake_dist = (v_limit**2 - v_peak**2) / (2 * a_minus)
            
            self.speed = v_limit
            # Cruising starts at d_accel, braking starts at (length - d_brake_dist)
            return length - d_brake_dist 
        
        else:
            # 5. Normal Accel -> Brake transition
            self.speed = v_limit
            return d_1

def max_corner_speed(typeFriction, radias, crawl_constant, totalDegredation, weatherMultiplier):
    return math.sqrt(GRAVITY * radias * tyre_friction(BASE_FRICTIONS[typeFriction], totalDegredation, weatherMultiplier)) + crawl_constant


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
