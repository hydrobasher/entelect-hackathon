class car:
    def __init__(self, max_speed, accel, brake, limp_constant, crawl_constant, fuel_tank_capacity, initial_fuel, fuel_consumption):
        self.max_speed = max_speed
        self.accel = accel
        self.brake = brake
        self.limp_constant = limp_constant
        self.crawl_constant = crawl_constant
        self.fuel_tank_capacity = fuel_tank_capacity
        self.initial_fuel = initial_fuel
        self.fuel_consumption = fuel_consumption
        
    def print(self):
        print(f"Max Speed: {self.max_speed} km/h")
        print(f"Acceleration: {self.accel} m/s^2")
        print(f"Braking: {self.brake} m/s^2")
        print(f"Limp Constant: {self.limp_constant}")
        print(f"Crawl Constant: {self.crawl_constant}")
        print(f"Fuel Tank Capacity: {self.fuel_tank_capacity} liters")
        print(f"Initial Fuel: {self.initial_fuel} liters")
        print(f"Fuel Consumption: {self.fuel_consumption} liters/100km")

class race:
    def __init__(self, name, laps, base_pit_stop_time, pit_tyre_swap_time, pit_refuel_rate, corner_crash_penalty, pit_exit_speed, fuel_soft_cap_limit, starting_weather_condition_id, time_reference):
        self.name = name
        self.laps = laps
        self.base_pit_stop_time = base_pit_stop_time
        self.pit_tyre_swap_time = pit_tyre_swap_time
        self.pit_refuel_rate = pit_refuel_rate
        self.corner_crash_penalty = corner_crash_penalty
        self.pit_exit_speed = pit_exit_speed
        self.fuel_soft_cap_limit = fuel_soft_cap_limit
        self.starting_weather_condition_id = starting_weather_condition_id
        self.time_reference = time_reference 

    def print(self):
        print(f"Race Name: {self.name}")
        print(f"Laps: {self.laps}")
        print(f"Base Pit Stop Time: {self.base_pit_stop_time} s")
        print(f"Pit Tyre Swap Time: {self.pit_tyre_swap_time} s")     
        print(f"Pit Refuel Rate: {self.pit_refuel_rate} l/s")
        print(f"Corner Crash Penalty: {self.corner_crash_penalty} s")
        print(f"Pit Exit Speed: {self.pit_exit_speed} m/s")
        print(f"Fuel Soft Cap Limit: {self.fuel_soft_cap_limit} l")
        print(f"Starting Weather Condition ID: {self.starting_weather_condition_id}")
        print(f"Time Reference: {self.time_reference} s")

class segment:
    def __init__(self, id, type, length, radius=None):
        self.id = id
        self.type = type
        self.radius = radius
        self.length = length

class track:
    def __init__(self, name, segments):
        self.name = name
        self.segments = segments

    def print(self):
        print(f"Track Name: {self.name}")
        print("Segments:")
        for segment in self.segments:
            print(f"  ID: {segment.id}, Type: {segment.type}, Length: {segment.length} m, Radius: {segment.radius if segment.radius is not None else 'N/A'} m")

class tyre:
    def __init__(self, name, life_span, dry_friction_multiplier, cold_friction_multiplier, light_rain_friction_multiplier, heavy_rain_friction_multiplier, dry_degradation, cold_degradation, light_rain_degradation, heavy_rain_degradation):
        self.name = name
        self.life_span = life_span
        self.dry_friction_multiplier = dry_friction_multiplier
        self.cold_friction_multiplier = cold_friction_multiplier
        self.light_rain_friction_multiplier = light_rain_friction_multiplier
        self.heavy_rain_friction_multiplier = heavy_rain_friction_multiplier
        self.dry_degradation = dry_degradation
        self.cold_degradation = cold_degradation
        self.light_rain_degradation = light_rain_degradation
        self.heavy_rain_degradation = heavy_rain_degradation

    def print(self):
        print(f"Tyre Compound: {self.name}")
        print(f"  Life Span: {self.life_span} laps")
        print(f"  Dry Friction Multiplier: {self.dry_friction_multiplier}")
        print(f"  Cold Friction Multiplier: {self.cold_friction_multiplier}")
        print(f"  Light Rain Friction Multiplier: {self.light_rain_friction_multiplier}")
        print(f"  Heavy Rain Friction Multiplier: {self.heavy_rain_friction_multiplier}")
        print(f"  Dry Degradation: {self.dry_degradation} per lap")
        print(f"  Cold Degradation: {self.cold_degradation} per lap")
        print(f"  Light Rain Degradation: {self.light_rain_degradation} per lap")
        print(f"  Heavy Rain Degradation: {self.heavy_rain_degradation} per lap")

class tyres:
    def __init__(self, soft, medium, hard, intermediate, wet):
        self.soft = soft
        self.medium = medium
        self.hard = hard
        self.intermediate = intermediate
        self.wet = wet

class set:
    def __init__(self, ids, compound):
        self.ids = ids
        self.compound = compound
    
class sets:
    def __init__(self, soft, medium, hard, intermediate, wet):
        self.soft = soft
        self.medium = medium
        self.hard = hard
        self.intermediate = intermediate
        self.wet = wet

class weather_condition:
    def __init__(self, id, condition, duration, acceleration_multiplier, deceleration_multiplier):
        self.id = id
        self.condition = condition
        self.duration = duration
        self.acceleration_multiplier = acceleration_multiplier
        self.deceleration_multiplier = deceleration_multiplier

    def print(self):
        print(f"ID: {self.id}, Condition: {self.condition}, Duration: {self.duration} s, Acceleration Multiplier: {self.acceleration_multiplier}, Deceleration Multiplier: {self.deceleration_multiplier}")

class weather:
    def __init__(self, conditions):
        self.conditions = conditions

class level:
    def __init__(self, levelname, car, race, track, tyres, sets, weather):
        self.levelname = levelname
        self.car = car
        self.race = race
        self.track = track
        self.tyres = tyres
        self.sets = sets
        self.weather = weather

    def print(self):
        print(f"Level Name: {self.levelname}")
        print("\nCar:")
        self.car.print()
        print("\nRace:")
        self.race.print()
        print("\nTrack:")
        self.track.print()
        print("\nTyres:")
        self.tyres.soft.print()
        self.tyres.medium.print()
        self.tyres.hard.print()
        self.tyres.intermediate.print()
        self.tyres.wet.print()
        print("\nSets:")
        print(f"  Soft: {self.sets.soft.ids}")
        print(f"  Medium: {self.sets.medium.ids}")
        print(f"  Hard: {self.sets.hard.ids}")
        print(f"  Intermediate: {self.sets.intermediate.ids}")
        print(f"  Wet: {self.sets.wet.ids}")
        print("\nWeather Conditions:")
        for condition in self.weather.conditions:
            condition.print()