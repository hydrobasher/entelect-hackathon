import json
import math

def load_level(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def compute_max_corner(radius, friction, crawl):
    return math.sqrt(friction * 9.8 * radius) + crawl

def generate_strategy(level):
    car = level['car']
    max_speed = car['max_speed_m/s']
    accel = car['accel_m/se2']
    brake = car['brake_m/se2']
    crawl = car['crawl_constant_m/s']
    race = level['race']
    laps = race['laps']
    track = level['track']['segments']
    tyres = level['tyres']['properties']
    
    # Choose soft tyre
    tyre_compound = 'Soft'
    base_friction = 1.8  # soft
    friction_multiplier = tyres[tyre_compound]['dry_friction_multiplier']
    friction = base_friction * friction_multiplier
    initial_tyre_id = 1  # soft
    
    laps_list = []
    for lap in range(1, laps + 1):
        segments = []
        current_speed = 0  # start of lap
        for i, seg in enumerate(track):
            if seg['type'] == 'corner':
                radius = seg['radius_m']
                max_c = compute_max_corner(radius, friction, crawl)
                entry_speed = min(current_speed, max_c)
                current_speed = entry_speed  # constant
                segments.append({"id": seg['id'], "type": "corner"})
            else:  # straight
                length = seg['length_m']
                # next segment
                next_i = (i + 1) % len(track)
                next_seg = track[next_i]
                if next_seg['type'] == 'corner':
                    next_radius = next_seg['radius_m']
                    next_max_c = compute_max_corner(next_radius, friction, crawl)
                    exit_speed = min(next_max_c, max_speed)
                else:
                    exit_speed = max_speed
                
                # compute braking_dist from max_speed to exit_speed
                if max_speed > exit_speed:
                    braking_dist = (max_speed**2 - exit_speed**2) / (2 * brake)
                else:
                    braking_dist = 0
                
                if braking_dist <= length:
                    target = max_speed
                    brake_start = braking_dist
                else:
                    target = math.sqrt(exit_speed**2 + 2 * brake * length)
                    brake_start = length
                
                segments.append({
                    "id": seg['id'],
                    "type": "straight",
                    "target_m/s": round(target, 2),
                    "brake_start_m_before_next": round(brake_start, 2)
                })
                current_speed = exit_speed  # after braking
        
        laps_list.append({
            "lap": lap,
            "segments": segments,
            "pit": {"enter": False}
        })
    
    return {
        "initial_tyre_id": initial_tyre_id,
        "laps": laps_list
    }

level = load_level('1.txt')
strategy = generate_strategy(level)
with open('output.txt', 'w') as f:
    json.dump(strategy, f, indent=2)