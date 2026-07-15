Rule Based Adaptive MIDI Generator

This project is a rule based system that generates therapeutic MIDI music, built around the idea of personalized rhythmic and harmonic stimuli for music based interventions. It started as my undergraduate thesis at Universitas Gadjah Mada, and it grew into a working app rather than staying just a paper.

The core idea is that instead of using a black box machine learning model to generate music, the system relies on explicit rules to control harmony and rhythm. This makes the output predictable and explainable, which matters in a context like music based interventions where the goal is to understand and control exactly what the system produces and why, rather than trusting a model that can't easily be interpreted.

What it does

The app is built with Streamlit, so it runs as an interactive web app. When you open it, you pick a therapeutic preset first, either Relaxation, Motor Synchronization, or Cognitive Stimulation. Each preset auto fills a tempo and a rhythmic complexity level that fit that use case, calm and slow for relaxation, steady and moderate for motor synchronization, faster and more complex for cognitive stimulation, but both values can still be adjusted manually afterward if you want something more specific.

You also enter a chord progression using standard chord symbols, like C G Am F, mixing major and minor chords freely. Once you click Generate MIDI, the system produces a multi track MIDI file with separate harmony, bass, and drum parts, built entirely from the rule based logic rather than being sampled or predicted by a model.

After generation, you get a piano roll visualization showing all three tracks over time, an audio preview synthesized right in the browser through FluidSynth, and a button to download the actual MIDI file for use in any compatible Digital Audio Workstation.

How it's built

The system is split into a few core modules that each handle one part of the pipeline.

harmonic_engine.py handles the harmonic logic, turning chord symbols into triads and harmonic structure based on the defined rules.

pattern_engine.py handles rhythmic pattern generation, shaped by the complexity level chosen.

midi_engine.py takes the harmonic and rhythmic output and converts it into actual MIDI data across the harmony, bass, and drum tracks.

input_module.py manages how user input gets processed into parameters the engines can use.

config.py holds configuration and rule definitions that drive the system.

app.py is the Streamlit entry point, handling the interface, the piano roll visualization, and the audio synthesis preview. Additional pages for batch generation and run history live under the pages folder.

Running it locally

Clone the repo, then set up a virtual environment and install dependencies.

bashgit clone https://github.com/taibaik/skripsi-midi-generator.git
cd skripsi-midi-generator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

The app needs soundfont.sf2 for the audio preview to work, which is already included in this repo. If pyfluidsynth isn't installed, the app still runs and generates the MIDI file, it just skips the browser audio preview.

Background

This was originally developed as my undergraduate thesis, "Design and Development of a Rule Based Adaptive MIDI Generator for Personalized Rhythmic and Harmonic Stimuli in Music Based Interventions," supervised by Dr. Lukman Heryawan at Universitas Gadjah Mada.

Notes

This is still evolving past the thesis version. Some parts of the rule logic and interface may continue to be refined as I keep working on it.