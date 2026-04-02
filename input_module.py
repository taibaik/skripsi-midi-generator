# input_module.py

def parse_input(chord_list, bpm=None):
    if bpm is None:
        from config import DEFAULT_BPM
        bpm = DEFAULT_BPM

    return {
        "chords": chord_list,
        "bpm": bpm
    }