class outSegment:
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
            segments.append(outSegment(i+1, level.track.segments[i]))
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