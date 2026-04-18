import json
import math

from classes import *
from classes2 import *
from functions import *
from readFile import read
from writeFile import write


def load_level(filename):
    with open(filename, "r") as f:
        return json.load(f)


def compute_max_corner(radius, friction, crawl):
    return math.sqrt(friction * 9.8 * radius) + crawl


def generate_strategy(level_data):
    car = level_data["car"]
    max_speed = car["max_speed_m/s"]
    accel = car["accel_m/se2"]
    brake = car["brake_m/se2"]
    crawl = car["crawl_constant_m/s"]
    race = level_data["race"]
    laps = race["laps"]
    track = level_data["track"]["segments"]
    tyres = level_data["tyres"]["properties"]

    # Race constraints
    initial_fuel = car["initial_fuel_l"]
    fuel_soft_cap = race.get("fuel_soft_cap_limit_l", 9999)

    # Choose initial tyre (soft for now, but could be optimized)
    tyre_compound = "Soft"
    base_friction = 1.8  # soft
    friction_multiplier = tyres[tyre_compound]["dry_friction_multiplier"]
    initial_friction = base_friction * friction_multiplier
    initial_tyre_id = 1  # soft

    # Tyre degradation parameters (using dry_degradation from JSON)
    tyre_degradation_rate = (
        tyres[tyre_compound]["dry_degradation"] / 1000.0
    )  # per meter

    # Fuel usage parameters
    K_BASE_FUEL = 0.001  # base fuel per meter
    K_DRAG_FUEL = 0.00001  # drag-related fuel coefficient

    # Estimate fuel per lap and tyre life
    track_length = sum(seg["length_m"] for seg in track)

    # Conservative speed factors to manage fuel and tyres
    speed_factor = 0.95  # Don't always go at max speed to save fuel/tyres
    max_lap_fuel = initial_fuel / laps * 1.1  # Allow 10% buffer per lap

    laps_list = []
    current_fuel = initial_fuel
    current_friction = initial_friction
    tyre_life_remaining = 1.0  # 1.0 = new, 0.0 = worn out
    min_tyre_life = 0.3  # Pit when tyre life drops below this

    for lap in range(1, laps + 1):
        segments = []
        current_speed = 0  # start of lap
        lap_fuel_used = 0.0
        need_pit = False

        # Check if we need a pit stop for fuel or tyres
        if lap > 1:
            # Estimate if we'll run out of fuel or tyres
            avg_fuel_per_lap = initial_fuel / laps
            remaining_laps = laps - lap + 1
            if current_fuel < avg_fuel_per_lap * remaining_laps * 0.8:
                need_pit = True
            if tyre_life_remaining < min_tyre_life:
                need_pit = True

        for i, seg in enumerate(track):
            if seg["type"] == "corner":
                radius = seg["radius_m"]
                # Adjust max corner speed based on tyre degradation
                degraded_friction = current_friction * (0.7 + 0.3 * tyre_life_remaining)
                max_c = math.sqrt(degraded_friction * 9.8 * radius) + crawl
                entry_speed = min(current_speed, max_c * speed_factor)
                current_speed = entry_speed

                # Estimate fuel used in corner (simplified)
                corner_fuel = (
                    K_BASE_FUEL * seg["length_m"]
                    + K_DRAG_FUEL * entry_speed * seg["length_m"]
                )
                lap_fuel_used += corner_fuel

                segments.append({"id": seg["id"], "type": "corner"})

            else:  # straight
                length = seg["length_m"]
                next_i = (i + 1) % len(track)
                next_seg = track[next_i]

                if next_seg["type"] == "corner":
                    next_radius = next_seg["radius_m"]
                    degraded_friction = current_friction * (
                        0.7 + 0.3 * tyre_life_remaining
                    )
                    next_max_c = (
                        math.sqrt(degraded_friction * 9.8 * next_radius) + crawl
                    )
                    exit_speed = min(
                        next_max_c * speed_factor, max_speed * speed_factor
                    )
                else:
                    exit_speed = max_speed * speed_factor

                # Compute braking distance
                target_speed = max_speed * speed_factor
                if target_speed > exit_speed:
                    braking_dist = (target_speed**2 - exit_speed**2) / (2 * brake)
                else:
                    braking_dist = 0

                if braking_dist <= length:
                    target = target_speed
                    brake_start = braking_dist
                else:
                    target = math.sqrt(exit_speed**2 + 2 * brake * length)
                    brake_start = length

                # Estimate fuel used on straight
                avg_straight_speed = (current_speed + target) / 2
                straight_fuel = (
                    K_BASE_FUEL * length + K_DRAG_FUEL * avg_straight_speed * length
                )
                lap_fuel_used += straight_fuel

                segments.append(
                    {
                        "id": seg["id"],
                        "type": "straight",
                        "target_m/s": round(target, 2),
                        "brake_start_m_before_next": round(brake_start, 2),
                    }
                )
                current_speed = exit_speed

        # Update tyre life based on lap distance
        tyre_life_remaining -= (track_length / 1000.0) * tyre_degradation_rate
        tyre_life_remaining = max(0.0, tyre_life_remaining)

        # Update fuel
        current_fuel -= lap_fuel_used

        # Determine if pit stop is needed
        pit_enter = need_pit or (
            lap < laps
            and (
                current_fuel < max_lap_fuel * 0.5 or tyre_life_remaining < min_tyre_life
            )
        )

        laps_list.append(
            {"lap": lap, "segments": segments, "pit": {"enter": pit_enter}}
        )

        # Reset if pitting
        if pit_enter:
            current_fuel = initial_fuel * 0.95  # Refuel to 95% to be safe
            tyre_life_remaining = 1.0
            current_friction = initial_friction

    return {"initial_tyre_id": initial_tyre_id, "laps": laps_list}


def compute_score(level, strategy):
    """
    Compute the actual score for a given level and strategy.
    Uses the scoring functions from functions.py
    """
    car = level.car
    race = level.race
    track = level.track
    tyres = level.tyres
    weather = level.weather

    # Get initial tyre based on strategy
    initial_tyre_id = strategy["initial_tyre_id"]
    tyre_compound = None
    if initial_tyre_id == 1:
        tyre_compound = tyres.soft
    elif initial_tyre_id == 2:
        tyre_compound = tyres.medium
    elif initial_tyre_id == 3:
        tyre_compound = tyres.hard
    elif initial_tyre_id == 4:
        tyre_compound = tyres.intermediate
    elif initial_tyre_id == 5:
        tyre_compound = tyres.wet

    # Create wheel object for tyre management
    # Get the starting weather condition string (e.g., "dry", "cold", etc.)
    starting_weather_condition = weather.conditions[0].condition
    wheel_obj = wheel(tyre_compound, starting_weather_condition, car.crawl_constant)

    total_time = 0.0
    total_fuel_used = 0.0
    current_fuel = car.initial_fuel
    current_speed = 0.0

    K_BASE_FUEL = 0.001
    K_DRAG_FUEL = 0.00001

    num_laps = race.laps
    segments = track.segments
    for lap_idx, lap_strategy in enumerate(strategy["laps"]):
        lap_time = 0.0

        for seg_idx, seg_strategy in enumerate(lap_strategy["segments"]):
            seg = segments[seg_idx]

            if seg.type == "corner":
                # Corner segment
                radius = seg.radius
                max_corner_speed = wheel_obj.getMaxCornerSpeed(radius)

                # Assume we enter at max corner speed (simplified)
                entry_speed = min(current_speed, max_corner_speed)
                exit_speed = entry_speed

                # Time through corner
                corner_length = seg.length
                avg_speed = (entry_speed + exit_speed) / 2
                if avg_speed > 0:
                    seg_time = corner_length / avg_speed
                else:
                    seg_time = 0

                lap_time += seg_time
                current_speed = exit_speed

                # Degrade tyre
                wheel_obj.degradeCorner(radius, exit_speed)

                # Fuel usage
                fuel = fuel_usage(
                    K_BASE_FUEL, K_DRAG_FUEL, entry_speed, exit_speed, corner_length
                )
                total_fuel_used += fuel
                current_fuel -= fuel

            else:  # straight
                # Straight segment
                length = seg.length
                target_speed = seg_strategy.get("target_m/s", car.max_speed)
                brake_start = seg_strategy.get("brake_start_m_before_next", 0)

                # Acceleration phase
                accel_dist = length - brake_start
                if accel_dist > 0:
                    # Accelerate to target or max possible
                    possible_speed = math.sqrt(
                        current_speed**2 + 2 * car.accel * accel_dist
                    )
                    final_accel_speed = min(possible_speed, target_speed, car.max_speed)
                    accel_time = (
                        (final_accel_speed - current_speed) / car.accel
                        if car.accel > 0
                        else 0
                    )
                    lap_time += accel_time

                    # Fuel during acceleration
                    fuel = fuel_usage(
                        K_BASE_FUEL,
                        K_DRAG_FUEL,
                        current_speed,
                        final_accel_speed,
                        accel_dist,
                    )
                    total_fuel_used += fuel
                    current_fuel -= fuel

                # Braking phase
                if brake_start > 0:
                    # Determine exit speed based on next segment
                    next_seg_idx = (seg_idx + 1) % len(segments)
                    next_seg = segments[next_seg_idx]

                    if next_seg.type == "corner":
                        exit_speed = wheel_obj.getMaxCornerSpeed(next_seg.radius)
                    else:
                        exit_speed = target_speed

                    # Brake from final_accel_speed to exit_speed
                    init_brake_speed = final_accel_speed
                    if init_brake_speed > exit_speed:
                        brake_time = (
                            (init_brake_speed - exit_speed) / car.brake
                            if car.brake > 0
                            else 0
                        )
                        lap_time += brake_time

                        # Fuel during braking
                        fuel = fuel_usage(
                            K_BASE_FUEL,
                            K_DRAG_FUEL,
                            init_brake_speed,
                            exit_speed,
                            brake_start,
                        )
                        total_fuel_used += fuel
                        current_fuel -= fuel

                    current_speed = exit_speed

                # Tyre degradation for straight
                wheel_obj.degradeStraight(length)

        # Check for pit stop
        if lap_strategy["pit"]["enter"]:
            # Add pit stop time
            pit_time = pitstop_time(0, race.pit_tyre_swap_time, race.base_pit_stop_time)
            lap_time += pit_time

            # Reset tyre degradation if tyre change
            wheel_obj.degredation = 0

        total_time += lap_time

    # Calculate score based on level type
    time_reference = race.time_reference
    fuel_soft_cap = race.fuel_soft_cap_limit

    if fuel_soft_cap >= 9999:  # Level 1 - time only
        score = base_score(time_reference, total_time)
    else:  # Level 2/3 - time and fuel
        score = level2n3Score(
            total_fuel_used, fuel_soft_cap, time_reference, total_time
        )

    return {
        "total_time": total_time,
        "total_fuel_used": total_fuel_used,
        "score": score,
        "tyre_degradation": wheel_obj.degredation,
    }


# Main execution
if __name__ == "__main__":
    # Load level data
    level_data = load_level("1.txt")

    # Generate strategy
    strategy = generate_strategy(level_data)

    # Save strategy to file
    with open("output.txt", "w") as f:
        json.dump(strategy, f, indent=2)

    # Load parsed level objects for scoring
    level = read("2.txt")

    # Compute score
    result = compute_score(level, strategy)

    print(f"Total Time: {result['total_time']:.2f} seconds")
    print(f"Total Fuel Used: {result['total_fuel_used']:.2f} liters")
    print(f"Tyre Degradation: {result['tyre_degradation']:.4f}")
    print(f"Score: {result['score']:.2f}")
    write("output80.txt", strategy)
