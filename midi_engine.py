import pretty_midi
import random
import os

from datetime import datetime

from config import (
    BASE_VELOCITY,
    VELOCITY_VARIATION
)


OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def apply_velocity(base_velocity):

    return base_velocity + random.randint(
        -VELOCITY_VARIATION,
        VELOCITY_VARIATION
    )


def create_midi(
    all_events,
    bpm,
    complexity_level=1,
    output_name=None
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    if output_name is None:

        output_name = (
            f"output_{bpm}"
            f"_c{complexity_level}"
            f"_{timestamp}.mid"
        )

    print("Creating MIDI file...")

    print(
        f"Number of events received: "
        f"{len(all_events)}"
    )

    midi = pretty_midi.PrettyMIDI(
        initial_tempo=bpm
    )

    harmony = pretty_midi.Instrument(
        program=0
    )

    bass = pretty_midi.Instrument(
        program=33
    )

    drums = pretty_midi.Instrument(
        program=0,
        is_drum=True
    )

    for event in all_events:

        if bpm < 80:

            base_velocity = 65

        elif bpm < 110:

            base_velocity = 80

        elif bpm < 140:

            base_velocity = 95

        else:

            base_velocity = 110

        if event["track"] == "harmony":

            velocity = (
                base_velocity - 5
                + random.randint(-6, 6)
            )

        elif event["track"] == "bass":

            if event["start"] % (
                4 * (60 / bpm)
            ) < 0.01:

                velocity = (
                    base_velocity + 10
                )

            else:

                velocity = (
                    base_velocity - 5
                    + random.randint(-5, 5)
                )

        else:

            if event["pitch"] == 36:

                velocity = (
                    base_velocity + 20
                )

            elif event["pitch"] == 38:

                velocity = (
                    base_velocity + 10
                )

            else:

                velocity = (
                    base_velocity - 20
                    + random.randint(-3, 3)
                )

        velocity = max(
            0,
            min(127, velocity)
        )

        note = pretty_midi.Note(
            velocity=velocity,
            pitch=event["pitch"],
            start=event["start"],
            end=event["end"]
        )

        if event["track"] == "harmony":

            harmony.notes.append(note)

        elif event["track"] == "bass":

            bass.notes.append(note)

        else:

            drums.notes.append(note)

    midi.instruments.extend([
        harmony,
        bass,
        drums
    ])

    output_path = os.path.join(
        OUTPUT_DIR,
        output_name
    )

    midi.write(output_path)

    print(f"MIDI saved as {output_path}")

    return output_path