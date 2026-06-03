<p align="center">
  <h1 align="center">Entelect F1 Hackathon — Race Strategy Optimizer</h1>
  <p align="center">
    Physics-based lap-by-lap race strategy engine for the Entelect F1 Hackathon
    <br />
    <a href="#overview"><strong>Overview</strong></a> ·
    <a href="#file-structure"><strong>Structure</strong></a> ·
    <a href="#how-to-run"><strong>Usage</strong></a> ·
    <a href="#data-files-json"><strong>Data</strong></a> ·
    <a href="#how-data-is-parsed"><strong>Parsing</strong></a> ·
    <a href="#how-data-is-analysed"><strong>Analysis</strong></a>
  </p>
</p>

---

## Overview

Given car specs, track layouts, tyre compounds, and weather conditions, this project computes an **optimal driving strategy** for every lap — specifying per-segment target speeds and braking points to minimise race time while managing fuel consumption and tyre degradation.

| Level | Track | Laps | Weather | Scoring |
|-------|-------|------|---------|---------|
| 1 | Neo Kyalami | 50 | Dry | Time only |
| 2 | Silverstone | 60 | Dry | Time + fuel |
| 3 | Spa-Francorchamps | 70 | Changing (4 conditions) | Time + fuel |
| 4 | Circuit de Monaco | 80 | Complex (8 conditions) | Time + fuel |

---

## File Structure

```
entelect-hackathon/
 1-4.txt                  Track data files (JSON input)
 lvl*.txt                 Generated strategy outputs
 classes.py               Domain model (car, race, track, tyre, weather)
 classes2.py              Output DTOs (outSegment*, outLap, outLevel)
 functions.py             Physics engine (friction, degradation, fuel, scoring)
 kirk.py                  Primary strategy engine — braking point calculator
 main.py                  Entry point — runs all levels × tyre compounds
 optimizer.py             Alternative heuristic strategy generator + scorer
 readFile.py              JSON → domain object deserialiser
 writeFile.py             Domain object → JSON serialiser
 out1/                    Backup of earlier module versions
```

**Key modules explained:**

| Module | Role |
|--------|------|
| `classes.py` | Domain model — `car`, `race`, `segment`, `track`, `tyre`, `weather_condition`, `level` |
| `classes2.py` | Output DTOs with `to_dict()` serialisation for strategy output |
| `functions.py` | Physics constants, `wheel` (tyre state), `vehicle` (car state), scoring functions |
| `kirk.py` | Core strategy engine — iterates laps/segments, computes braking points |
| `main.py` | Drives `kirk()` across all 4 levels × 5 tyre compounds |
| `optimizer.py` | Alternative heuristic engine with full strategy simulation and scoring |
| `readFile.py` | Deserialises JSON input files into `level` objects |
| `writeFile.py` | Serialises `outLevel` strategies back to JSON output files |

---

## How to Run

### Requirements

Python 3 — **zero external dependencies** (stdlib only: `json`, `math`).

### Run all levels and compounds

```bash
python main.py
```

Produces one output file per combination: `lvl1-soft.txt`, `lvl1-medium.txt`, `lvl4-wet.txt`, etc.

### Run the alternative optimizer (Level 1 demo)

```bash
python optimizer.py
```

Loads `1.txt`, generates a heuristic strategy, scores it, and writes results to `output.txt` / `output80.txt`.

### Output format

```json
{
  "initial_tyre_id": 1,
  "laps": [
    {
      "lap": 1,
      "segments": [
        { "id": 1, "type": "straight", "target_m/s": 90, "brake_start_m_before_next": 155.81 },
        { "id": 2, "type": "corner" }
      ],
      "pit": { "enter": false, "tyre_change_set_id": 1, "fuel_refuel_amount_l": 100 }
    }
  ]
}
```

---

## Data Files (JSON)

Each `{n}.txt` contains a JSON object with these top-level keys:

```jsonc
{
  "car":      { /* max_speed, accel, brake, fuel_tank_capacity, ... */ },
  "race":     { /* laps, pit_stop_times, fuel_soft_cap, time_reference, ... */ },
  "track":    { /* name, segments: [{ id, type, length_m, radius_m? }] */ },
  "tyres":    { /* properties: { Soft, Medium, Hard, Intermediate, Wet } */ },
  "available_sets": [ /* { ids: [1], compound: "Soft" } */ ],
  "weather":  { /* conditions: [{ id, condition, duration_s, acceleration_multiplier, ... }] */ }
}
```

**Segment types:**
- `straight`: `id`, `type`, `length_m`
- `corner`: `id`, `type`, `length_m`, `radius_m`

---

## How Data Is Parsed

### Reading (`readFile.py`)

`read(filename)` loads JSON and constructs domain objects in 7 steps:

1. **Car** — vehicle specs mapped directly from JSON
2. **Race** — race configuration (laps, pit timing, fuel caps, weather)
3. **Track** — iterates segments, creates `segment` objects (includes `radius` for corners)
4. **Tyres** — iterates 5 compounds, builds `tyre` objects with per-weather friction + degradation
5. **Sets** — maps available tyre set IDs by compound name
6. **Weather** — creates `weather_condition` objects from the conditions array
7. **Level** — top-level container assembling everything above

### Writing (`writeFile.py`)

`write(filename, out_level_obj)` recursively serialises to JSON:
- Uses `to_dict()` if available (for custom key mapping like `target_m/s`)
- Falls back to `__dict__` introspection
- Skips the internal `level` reference on `outLevel` to avoid circular serialisation

---

## How Data Is Analysed

The project uses **physics-based simulation** to compute per-lap strategies. Two engines are available.

### Primary Engine — `kirk.py`

`kirk(levelNumber, wheelTypeId)`:
1. Reads and deserialises the level data
2. Selects the requested tyre compound
3. Initialises `wheel` (tyre state tracker) and `vehicle` (car state)
4. Iterates every lap and segment:
   - Skips corners (handled by the preceding straight)
   - For straights followed by corners, calls `vehicle.accelerateOverStraight()` to find the **optimal braking point**
   - Handles edge cases: no braking needed, hitting `max_speed` ceiling
5. Writes the strategy to `lvl{n}-{compound}.txt`

### Alternative Engine — `optimizer.py`

`generate_strategy(level_data)`:
- Conservative speed factor (95% of max)
- Tracks tyre life + fuel burn per lap
- Decides pit stops based on fuel thresholds and tyre degradation

`compute_score(level, strategy)`:
- Simulates the full race: acceleration, braking, cornering, pit stops
- Degrades tyres through the physics model
- Applies the competition scoring function

### Physics Model — `functions.py`

**Key constants:**

| Constant | Value |
|----------|-------|
| Gravity | 9.8 m/s² |
| Base friction (Soft) | 1.8 |
| Base friction (Medium) | 1.7 |
| Base friction (Hard) | 1.6 |
| Base friction (Intermediate) | 1.2 |
| Base friction (Wet) | 1.1 |
| K straight degradation | 1.66 × 10⁻⁵ |
| K braking degradation | 3.98 × 10⁻² |
| K corner degradation | 2.65 × 10⁻⁴ |

**Key calculations:**

| Quantity | Formula |
|----------|---------|
| Tyre friction | μ = (μ_base − d) × m_weather |
| Max corner speed | v_max = √(g · r · μ) + v_crawl |
| Straight degradation | d += k_str · L · m_deg |
| Braking degradation | d += k_brk · m_deg · ((v_i/100)² − (v_f/100)²) |
| Corner degradation | d += k_cor · m_deg · v² / r |
| Fuel usage | F = (k_base + k_drag · v̄²) · d |
| Pit stop time | t = t_refuel + t_swap + t_base |

**Scoring:**

| Level | Formula |
|-------|---------|
| Level 1 (time only) | score = 500000 × (T_ref / T)³ |
| Levels 2–4 (time + fuel) | score = 500000 × (T_ref / T)³ − 500000 × (1 − F / F_cap)² + 500000 |

---

## Dependencies

| Module | Used in |
|--------|---------|
| `json` | readFile.py, writeFile.py, optimizer.py |
| `math` | functions.py, optimizer.py |
