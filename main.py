print("MAIN FILE IS RUNNING")

from input_module import parse_input
from harmonic_engine import get_triad
from pattern_engine import generate_patterns
from midi_engine import create_midi
from config import BAR_BEATS

def run_generator(chords, bpm=100, complexity_level=1):

    data = parse_input(chords, bpm)

    seconds_per_beat = 60 / data["bpm"]
    current_time = 0
    all_events = []

    for chord in data["chords"]:
        triad = get_triad(chord)

        events = generate_patterns(
            triad,
            current_time,
            seconds_per_beat,
            complexity_level
        )

        all_events.extend(events)

        current_time += BAR_BEATS * seconds_per_beat

    create_midi(all_events, bpm, complexity_level=complexity_level)


if __name__ == "__main__":

    progression = ["C", "G", "Am", "F"]

    for bpm in [60, 80, 100, 120, 140]:
        for complexity in [1, 2, 3]:
            print(f"\nGenerating BPM {bpm} | Complexity {complexity}")

            run_generator(
                progression,
                bpm=bpm,
                complexity_level=complexity
            )