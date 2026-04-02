import pretty_midi
import random
import os
from config import BASE_VELOCITY, VELOCITY_VARIATION


def apply_velocity(base_velocity):
    return base_velocity + random.randint(-VELOCITY_VARIATION, VELOCITY_VARIATION)


def create_midi(all_events, bpm, complexity_level=1, output_name=None):

    if output_name is None:
        output_name = f"output_{bpm}_c{complexity_level}.mid"

    print("Creating MIDI file...")
    print(f"Number of events received: {len(all_events)}")

    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)

    harmony = pretty_midi.Instrument(program=0)
    bass = pretty_midi.Instrument(program=33)
    drums = pretty_midi.Instrument(program=0, is_drum=True)

    for event in all_events:

        # Base intensity from the tempo

        if bpm < 80:
            base_velocity = 65
        elif bpm < 110:
            base_velocity = 80
        elif bpm < 140:
            base_velocity = 95
        else:
            base_velocity = 110

        # Instrument adjustments (specific)

        if event["track"] == "harmony":
            velocity = base_velocity - 5 + random.randint(-6, 6)

        elif event["track"] == "bass":
            # Accent first beat more strongly
            if event["start"] % (4 * (60 / bpm)) < 0.01:
                velocity = base_velocity + 10
            else:
                velocity = base_velocity - 5 + random.randint(-5, 5)

        else: # drums
            if event["pitch"] == 36: # Kick
                velocity = base_velocity + 20
            elif event["pitch"] == 38: # Snare
                velocity = base_velocity + 10
            else: # Hi-hat
                velocity = base_velocity - 20 + random.randint(-3, 3)

        #Clamp to MIDI safe range
        velocity = max(0, min(127, velocity))

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

    # VERY IMPORTANT: must be OUTSIDE the loop
    midi.instruments.extend([harmony, bass, drums])

    output_path = os.path.join(os.getcwd(), output_name)
    midi.write(output_path)

    print(f"MIDI saved as {output_path}")