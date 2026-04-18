import json
from classes import *
from classes2 import *
from readFile import read

import json

def write(filename, out_level_obj):
    def serialize(obj):
        # 1. If the object has a manual to_dict method, use it
        if hasattr(obj, "to_dict"):
            return {k: serialize(v) for k, v in obj.to_dict().items()}
        
        # 2. Handle lists (like your 'laps' or 'segments' lists)
        if isinstance(obj, list):
            return [serialize(i) for i in obj]
        
        # 3. Handle basic types (int, float, str, bool, None)
        if not hasattr(obj, "__dict__"):
            return obj
            
        # 4. Fallback for objects without a to_dict (standard __dict__ unpacking)
        data = {}
        for key, value in obj.__dict__.items():
            if key == 'level': continue
            data[key] = serialize(value)
        return data

    output_dict = serialize(out_level_obj)
    with open(filename, 'w') as f:
        json.dump(output_dict, f, indent=4)

level1 = read("1.txt")
out_level1 = outLevel(level1)

for s in out_level1.laps[0].segments:
    print(f"  Segment {s.id} - Type: {s.type}, Target m/s: {s.target_ms if hasattr(s, 'target_ms') else 'N/A'}")

write("out1.txt", out_level1)  