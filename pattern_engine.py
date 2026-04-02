import random
from config import BAR_BEATS

def generate_patterns(triad, start_time, seconds_per_beat, complexity_level):

    events = []
    bar_duration = BAR_BEATS * seconds_per_beat

    # Harmony Location ->

    harmony_duration = bar_duration
    for note in triad:
        events.append({
            "pitch": note,
            "start": start_time,
            "end": start_time + harmony_duration,
            "track": "harmony"
        })

    # Bass Location ->

    root = triad[0] - 12

    if complexity_level == 1:
        beats = [0]
    elif complexity_level == 2:
        beats = [0, 2]
    else:
        beats = [0, 1, 2, 3]

    for beat in beats:
        base_start = start_time + beat * seconds_per_beat

        # expressive groove: slightly early on beat 3
        if beat == 2:
            offset = -0.01
        else:
            offset = 0

        events.append({
            "pitch": root,
            "start": base_start + offset,
            "end": base_start + seconds_per_beat,
            "track": "bass"
        })

    # Drums Location ->

    drum_map = {
        0: 36,  # Kick
        1: 38,  # Snare
        2: 36,
        3: 38
    }

    for beat in range(4):

        base_start = start_time + beat * seconds_per_beat

        if drum_map[beat] == 38:
            # Snare slightly late for groove (consistantly)
            offset = 0.012
        else:
            # the kick stable
            offset = 0

        events.append({
            "pitch": drum_map[beat],
            "start": base_start + offset,
            "end": base_start + (0.5 * seconds_per_beat),
            "track": "drums"
        })

    # Hi-Hat Location ->

    if complexity_level >= 2:

        subdivisions = 8 if complexity_level == 2 else 16

        for i in range(subdivisions):

            base_position = start_time + (i / subdivisions) * bar_duration

            # light swing untuk ngedelat off beat
            if i % 2 == 1:
                offset = 0.01
            else:
                offset = -0.003

            events.append({
                "pitch": 42,
                "start": base_position + offset,
                "end": base_position + 0.02,
                "track": "drums"
            })

    return events