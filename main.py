from input_module import parse_input
from harmonic_engine import get_triad
from pattern_engine import generate_patterns
from midi_engine import create_midi
from config import BAR_BEATS

import csv
import os
from datetime import datetime


OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    OUTPUT_DIR,
    "run_log.csv"
)


if not os.path.exists(LOG_FILE):

    with open(
        LOG_FILE,
        mode="w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "bpm",
            "complexity",
            "preset",
            "chord_progression",
            "output_filename",
            "number_of_events"
        ])


def write_run_log(
    bpm,
    complexity,
    preset_name,
    chords,
    output_filename,
    event_count
):

    with open(
        LOG_FILE,
        mode="a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().isoformat(),
            bpm,
            complexity,
            preset_name,
            " ".join(chords),
            output_filename,
            event_count
        ])


def run_generator(
    chords,
    bpm=100,
    complexity_level=1,
    preset_name="Manual"
):

    data = parse_input(chords, bpm)

    seconds_per_beat = (
        60 / data["bpm"]
    )

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

        current_time += (
            BAR_BEATS
            * seconds_per_beat
        )

    output_path = create_midi(
        all_events,
        bpm,
        complexity_level=complexity_level
    )

    output_filename = (
        output_path.split("/")[-1]
    )

    write_run_log(
        bpm=bpm,
        complexity=complexity_level,
        preset_name=preset_name,
        chords=chords,
        output_filename=output_filename,
        event_count=len(all_events)
    )

    return output_path, len(all_events)