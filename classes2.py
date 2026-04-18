class outSegmentStraight:
    def __init__(self, id, segment):
        self.id = id
        self.type = segment.type
        self.target_ms = 50
        self.brake_start_m_before_next = 100

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "target_m/s": self.target_ms, # Manually mapping the key
            "brake_start_m_before_next": self.brake_start_m_before_next
        }

class outSegmentCorner:
    def __init__(self, id, segment):
        self.id = id
        self.type = segment.type

class outPit:
    def __init__(self):
        self.enter = False      

class outLap:
    def __init__(self, lap, level):
        self.lap = lap
        
        segments = []
        for i in range(len(level.track.segments)):
            if level.track.segments[i].type == "straight":
                segments.append(outSegmentStraight(i+1, level.track.segments[i]))
            else:
                segments.append(outSegmentCorner(i+1, level.track.segments[i]))
        self.segments = segments

        self.pit = outPit()

class outLevel:
    def __init__(self, level):
        self.level = level

        self.initial_tyre_id = 1

        laps = []
        for i in range(self.level.race.laps):
            laps.append(outLap(i+1, self.level))
        self.laps = laps