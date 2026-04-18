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

class segment:
    def __init__(self, id, type, length):
        self.id = id
        self.type = type
        self.length = length

class track:
    def __init__(self, name, segments):
        self.name = name
        self.segments = segments

    def print(self):
        print(f"Track Name: {self.name}")
        print("Segments:")
        for segment in self.segments:
            print(f"  ID: {segment.id}, Type: {segment.type}, Length: {segment.length} m")

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

class tyres:
    def __init__(self, soft, medium, hard, intermediate, wet):
        self.soft = soft
        self.medium = medium
        self.hard = hard
        self.intermediate = intermediate
        self.wet = wet

class set:
    