import streamlit as st


st.set_page_config(
    page_title="History",
    page_icon="📜"
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


st.title("Generation History")

st.write(
    """
    This page will display previously generated MIDI
    outputs and historical generation metadata from
    outputs/run_log.csv.

    The feature will support traceability, evaluation
    review, and generation auditing.
    """
)