#harmonic engine for triad harmonies

NOTE_TO_MIDI = {
    "C": 60,
    "C#": 61,
    "D": 62,
    "D#": 63,
    "E": 64,
    "F": 65,
    "F#": 66,
    "G": 67,
    "G#": 68,
    "A": 69,
    "A#": 70,
    "B": 71
}

def get_triad(chord_symbol):
    if chord_symbol.endswith("m"):
        chord_type = "minor"
        root = chord_symbol[:-1]
    else:
        chord_type = "major"
        root = chord_symbol

    root_midi = NOTE_TO_MIDI[root]

    if chord_type == "major":
        return [root_midi, root_midi + 4, root_midi + 7]
    else:
        return [root_midi, root_midi + 3, root_midi + 7]