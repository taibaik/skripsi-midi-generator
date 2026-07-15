import streamlit as st
import pretty_midi
import matplotlib.pyplot as plt
import numpy as np

from main import run_generator
from harmonic_engine import get_triad


st.set_page_config(
    page_title="Rule-Based Generator",
    page_icon="🎵",
    layout="centered"
)


st.markdown("""
<style>
h1, h2, h3 { color: #1e2d3a; font-weight: 600; }

.stButton > button {
    background-color: #4a9b8e;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    transition: background-color 0.2s ease;
}
.stButton > button:hover {
    background-color: #3d8478;
    color: #ffffff;
}

.stSlider [role="slider"] {
    background-color: #4a9b8e;
}

.stAlert {
    border-radius: 8px;
}

[data-testid="stExpander"] {
    border-radius: 8px;
    border: 1px solid #d4cfbc;
}

[data-testid="stMarkdownContainer"] code {
    background-color: #e8e2d0;
    color: #1e2d3a;
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)


PRESET_CONFIG = {
    "Relaxation": {
        "bpm": 70,
        "complexity": 1
    },
    "Motor Synchronization": {
        "bpm": 110,
        "complexity": 2
    },
    "Cognitive Stimulation": {
        "bpm": 135,
        "complexity": 3
    }
}


SOUNDFONT_PATH = "soundfont.sf2"


st.title("Rule-Based Generator")

st.subheader(
    "Rule-Based Therapeutic MIDI Generator"
)

st.write(
    """
    Rule-Based Generator is a rule-based symbolic music
    generation system designed to create therapeutic
    MIDI accompaniment patterns using configurable
    tempo, rhythmic complexity, and chord progression
    parameters.
    """
)


with st.expander(
    "How to use this generator",
    expanded=False
):

    st.markdown("""
    1. **Select a therapeutic preset** that matches your intended use — Relaxation for slow calming stimuli, Motor Synchronization for steady rhythmic entrainment, or Cognitive Stimulation for higher-tempo engagement. The preset will auto-fill the tempo and complexity controls below, but you can adjust them manually afterward.

    2. **Enter a chord progression** in the text field. Use standard chord symbols separated by spaces (for example: `C G Am F`). Both major chords (`C`, `G`, `F`) and minor chords (`Cm`, `Am`, `Dm`) are supported.

    3. **Click Generate MIDI**. The system will produce a multi-track MIDI file containing harmony, bass, and drum patterns based on your inputs.

    4. **Review the output**. You will see a piano roll visualization of the generated material, hear an audio preview synthesized in your browser, and have the option to download the MIDI file for use in any compatible Digital Audio Workstation.
    """)


if "preset" not in st.session_state:

    st.session_state.preset = "Relaxation"

if "tempo" not in st.session_state:

    st.session_state.tempo = 70

if "complexity" not in st.session_state:

    st.session_state.complexity = 1


def apply_preset():

    preset = PRESET_CONFIG[
        st.session_state.preset
    ]

    st.session_state.tempo = preset["bpm"]

    st.session_state.complexity = (
        preset["complexity"]
    )


st.selectbox(
    "Therapeutic Preset",
    list(PRESET_CONFIG.keys()),
    key="preset",
    on_change=apply_preset
)


tempo = st.slider(
    "Tempo (BPM)",
    60,
    140,
    key="tempo"
)


complexity = st.selectbox(
    "Rhythmic Complexity",
    [1, 2, 3],
    key="complexity"
)


chord_input = st.text_input(
    "Chord Progression",
    "C G Am F"
)


if st.button("Generate MIDI"):

    chords = chord_input.split()

    invalid_chords = []

    for chord in chords:

        try:

            get_triad(chord)

        except Exception:

            invalid_chords.append(chord)

    if invalid_chords:

        st.error(
            f"Invalid chord: "
            f"{', '.join(invalid_chords)}"
        )

        st.stop()

    output_path, total_events = run_generator(
        chords,
        bpm=tempo,
        complexity_level=complexity,
        preset_name=st.session_state.preset
    )

    st.success(
        "MIDI Generated Successfully"
    )

    st.write(
        f"Generated Events: {total_events}"
    )

    midi_data = pretty_midi.PrettyMIDI(
        output_path
    )

    fig, ax = plt.subplots(
        figsize=(10, 4)
    )

    track_colors = {
        0: "#1f77b4",
        1: "#2ca02c",
        2: "#d62728"
    }

    track_labels = {
        0: "Harmony",
        1: "Bass",
        2: "Drums"
    }

    used_labels = set()

    for instrument_index, instrument in enumerate(
        midi_data.instruments
    ):

        color = track_colors.get(
            instrument_index,
            "#000000"
        )

        label = track_labels.get(
            instrument_index,
            "Track"
        )

        for note in instrument.notes:

            if label not in used_labels:

                ax.barh(
                    note.pitch,
                    note.end - note.start,
                    left=note.start,
                    height=0.8,
                    color=color,
                    label=label
                )

                used_labels.add(label)

            else:

                ax.barh(
                    note.pitch,
                    note.end - note.start,
                    left=note.start,
                    height=0.8,
                    color=color
                )

    ax.set_xlabel("Time (s)")

    ax.set_ylabel("MIDI Pitch")

    ax.set_title(
        "Generated MIDI — Piano Roll"
    )

    ax.legend()

    st.pyplot(fig)

    plt.close(fig)

    try:

        with st.spinner(
            "Synthesizing audio..."
        ):

            audio_data = midi_data.fluidsynth(
                sf2_path=SOUNDFONT_PATH,
                fs=44100
            )

            max_val = np.max(
                np.abs(audio_data)
            )

            if max_val > 0:

                audio_data = (
                    audio_data / max_val
                )

            st.caption(
                "Audio preview "
                "(synthesized via FluidSynth)"
            )

            st.audio(
                audio_data,
                sample_rate=44100
            )

    except FileNotFoundError:

        st.warning(
            "Audio preview unavailable: "
            "soundfont.sf2 not found "
            "in project root."
        )

    except (
        ImportError,
        ModuleNotFoundError
    ):

        st.warning(
            "Audio preview unavailable: "
            "pyfluidsynth not installed."
        )

    except Exception as e:

        st.warning(
            f"Audio preview unavailable: "
            f"{str(e)}"
        )

    with open(output_path, "rb") as file:

        st.download_button(
            label="Download MIDI File",
            data=file,
            file_name=output_path.split("/")[-1],
            mime="audio/midi"
        )