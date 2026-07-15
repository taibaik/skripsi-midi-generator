import streamlit as st
import pandas as pd
from main import run_generator
from harmonic_engine import get_triad

st.set_page_config(
    page_title="Batch Mode",
    page_icon="📦"
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

st.title("Batch Mode")
st.write(
    """
    This page generates multiple MIDI files across
    combinations of BPM and rhythmic complexity
    levels using the same chord progression.
    The workflow supports reproducible experimental
    evaluation for therapeutic MIDI generation.
    """
)

chord_input = st.text_input(
    "Chord Progression",
    "C G Am F"
)

bpm_values = st.multiselect(
    "Tempo Values (BPM)",
    options=[
        60, 70, 80, 90,
        100, 110, 120, 130, 140
    ],
    default=[
        60, 80, 100, 120, 140
    ]
)

complexity_levels = st.multiselect(
    "Complexity Levels",
    options=[1, 2, 3],
    default=[1, 2, 3]
)

total_runs = (
    len(bpm_values)
    * len(complexity_levels)
)

st.info(
    f"Total runs: {total_runs}"
)

if st.button("Run Batch Generation"):

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

    if len(bpm_values) == 0:
        st.error(
            "Select at least one BPM value"
        )
        st.stop()

    if len(complexity_levels) == 0:
        st.error(
            "Select at least one complexity level"
        )
        st.stop()

    progress_bar = st.progress(0)
    status_text = st.empty()
    results = []
    total = total_runs
    current_run = 0

    for bpm in bpm_values:
        for complexity in complexity_levels:
            status_text.text(
                f"Generating BPM {bpm} "
                f"| Complexity {complexity}..."
                f" ({current_run + 1} of {total})"
            )

            try:
                output_path, event_count = (
                    run_generator(
                        chords,
                        bpm=bpm,
                        complexity_level=complexity,
                        preset_name="Batch"
                    )
                )
                results.append({
                    "BPM": bpm,
                    "Complexity": complexity,
                    "Output File": (
                        output_path.split("/")[-1]
                    ),
                    "Events": event_count
                })

            except Exception as e:
                results.append({
                    "BPM": bpm,
                    "Complexity": complexity,
                    "Output File": "FAILED",
                    "Events": str(e)
                })

            current_run += 1
            progress_bar.progress(
                current_run / total
            )

    status_text.empty()

    st.success(
        f"Batch complete: {total} MIDI files "
        f"generated in outputs/ folder"
    )

    st.dataframe(
        pd.DataFrame(results)
    )