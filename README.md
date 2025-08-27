# Resonance interactive installation

**Resonance** is an interactive audiovisual installation driven by real-time emotion detection and biometric feedback. It generates an audio-visual output in response to participants' emotional states.

## Dependencies

- [MediaMTX](https://github.com/bluenviron/mediamtx): Used for glitching video artifacts (via RTMP streaming)
- [Max 8](https://cycling74.com/products/max): For audio synthesis and signal processing
- [Syphon](https://github.com/Syphon/Simple/releases/tag/5): For grabbing video stream in OBS
- Node.js >= 20
- Python >= 3.9

## Visuals (TouchDesigner)

### Streaming Pipeline for MPEG artifacts

1. **Start the MediaMTX Server**  
   Ensure that the MediaMTX server is running locally. This is required for RTMP streaming and glitch effects.

2. **Capture Video in OBS**  
   Use **Syphon** (macOS) or **NDI** (cross-platform) to grab the TouchDesigner output in OBS.

3. **Stream to TouchDesigner**  
    In OBS, configure a custom RTMP stream and set the server URL to `rtmp://localhost/camera`. In TouchDesigner, use a `Video Stream In` TOP to receive the stream. You can adjust the buffer size on the `Video Stream In` TOP to control how glitchy the incoming video appears. Smaller buffers introduce more artifacts and make the output glitchier.

### Camera Background Removal (macOS Workaround)

The built-in Chroma Key tool in TouchDesigner is made for Intel and doesn’t work well on macOS. To remove the background, use macOS’s FaceTime camera effects and add a virtual green screen. A custom TouchDesigner component (`background.tox`) then keys it out.

#### Steps

1. **Enable Virtual Green Screen**
   - On macOS, open the **Control Center** from the menu bar.
   - Under **Video Effects**, select **Background** and choose a **solid green background**.
   - This creates a virtual green screen using Apple’s built-in FaceTime camera processing.

2. **Capture in TouchDesigner**
   - In TouchDesigner, use a `Video Device In` TOP and set the input to **FaceTime HD Camera**.
   - The video feed will include the virtual green background.

3. **Remove the Background**
   - Use the custom `background.tox` component included with this project to process the camera feed.
   - This component takes the green-screened input and applies chroma keying internally.

## Audio (Max)

The audio engine is built in Max and structured around three core components: **harmony**, **melody**, and **percussive** elements. The project also contains a node server that exposes an API to Max for different methods.

### Harmony

The harmony system uses **modal harmony**, with chords generated based on a root note and mode (e.g., Dorian, Phrygian, Lydian). A custom Node.js function handles the generation of triads by analyzing the mode's scale, filtering out harmonically unstable chords (like those with diatonic tritones), and weighting chords that contain the mode’s characteristic note. Emotional data influences chord selection: lower valence favors minor and diminished chords, while higher valence favors major chords.

### Melody

- generate melody using the generateMelody from the node server
- markov chains
