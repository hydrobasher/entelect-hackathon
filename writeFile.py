import json
from classes import *
from classes2 import *
from readFile import read

import json

def write(filename, out_level_obj):
    # We use a helper function to recursively turn objects into dictionaries
    def serialize(obj):
        # If it's a list, serialize every item in it
        if isinstance(obj, list):
            return [serialize(i) for i in obj]
        
        # If it has a __dict__, it's one of our classes
        if hasattr(obj, "__dict__"):
            data = {}
            for key, value in obj.__dict__.items():
                # We skip the original 'level' reference in outLevel/outLap 
                # to avoid massive redundant data or circular references
                if key == 'level':
                    continue
                data[key] = serialize(value)
            return data
        
        # Return basic types (int, str, float) as they are
        return obj

    # Convert the object tree to a dictionary
    output_dict = serialize(out_level_obj)

    with open(filename, 'w') as f:
        # indent=4 makes the JSON file human-readable
        json.dump(output_dict, f, indent=4)

level1 = read("1.txt")
out_level1 = outLevel(level1)
write("out1.txt", out_level1)  