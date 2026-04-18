import json
from classes import *

def read(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    # 1. Create Car
    c = car(
        data['car']['max_speed_m/s'],
        data['car']['accel_m/se2'],
        data['car']['brake_m/se2'],
        data['car']['limp_constant_m/s'],
        data['car']['crawl_constant_m/s'],
        data['car']['fuel_tank_capacity_l'],
        data['car']['initial_fuel_l'],
        data['car']['fuel_consumption_l/m']
    )

    # 2. Create Race
    r = race(
        data['race']['name'],
        data['race']['laps'],
        data['race']['base_pit_stop_time_s'],
        data['race']['pit_tyre_swap_time_s'],
        data['race']['pit_refuel_rate_l/s'],
        data['race']['corner_crash_penalty_s'],
        data['race']['pit_exit_speed_m/s'],
        data['race']['fuel_soft_cap_limit_l'],
        data['race']['starting_weather_condition_id'],
        data['race']['time_reference_s']
    )

    # 3. Create Track and Segments
    segments_list = []
    for s in data['track']['segments']:
        segments_list.append(segment(s['id'], s['type'], s['length_m'], s['radius_m'] if 'radius_m' in s else None))
    t = track(data['track']['name'], segments_list)

    # 4. Create Tyres (Properties)
    tp = data['tyres']['properties']
    tyre_objects = {}
    for compound in ["Soft", "Medium", "Hard", "Intermediate", "Wet"]:
        tyre_objects[compound.lower()] = tyre(compound, **tp[compound])
    
    all_tyres = tyres(**tyre_objects)

    # 5. Create Sets (Available Sets)
    # Note: Your class 'sets' expects specific positional args, 
    # but the JSON provides a list. We map them by compound name.
    available_sets_map = {}
    for s_data in data['available_sets']:
        compound = s_data['compound']
        available_sets_map[compound.lower()] = set(s_data['ids'], compound)
    
    all_sets = sets(**available_sets_map)

    # 6. Create Weather
    conditions_list = []
    for w in data['weather']['conditions']:
        conditions_list.append(weather_condition(
            w['id'], 
            w['condition'], 
            w['duration_s'], 
            w['acceleration_multiplier'], 
            w['deceleration_multiplier']
        ))
    w_obj = weather(conditions_list)

    # 7. Final Level Object
    return level(r.name, c, r, t, all_tyres, all_sets, w_obj)

temp = read("4.txt")
temp.print()
