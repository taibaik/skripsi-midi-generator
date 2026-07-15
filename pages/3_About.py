import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="About",
    page_icon="ℹ️"
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


st.title("About RG-MBI Generator")


st.write(
    """
    RG-MBI Generator is a rule-based therapeutic MIDI
    generation system designed to create symbolic
    accompaniment patterns for therapeutic and
    music-based intervention research.

    The system focuses on controllable generation
    through deterministic musical rules involving
    harmonic structure, rhythmic complexity, and
    tempo-based behavioral modulation.
    """
)


st.subheader("Rule-Based Generation Approach")

st.write(
    """
    The generation process uses predefined harmonic
    and rhythmic rules instead of machine learning
    models. Musical structures are generated through
    symbolic mapping, pattern assignment, and
    parameter-driven event sequencing.

    This approach improves explainability,
    reproducibility, and controllability within
    therapeutic generation scenarios.
    """
)


st.subheader(
    "Therapeutic Preset Mapping"
)


preset_table = pd.DataFrame({
    "Preset": [
        "Relaxation",
        "Motor Synchronization",
        "Cognitive Stimulation"
    ],
    "Tempo Range": [
        "60–80 BPM",
        "100–120 BPM",
        "130–140 BPM"
    ],
    "Complexity": [
        "1",
        "2",
        "3"
    ]
})


st.table(preset_table)


st.subheader("Credits")

st.write(
    """
    Author — Muhammad Haiqal Dwikusuma

    Supervisor — Dr. Lukman Heryawan

    Institution — International Undergraduate Program
    in Computer Science, Gadjah Mada University
    """
)