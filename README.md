# Resonance interactive installation

**Resonance** is an interactive audiovisual installation driven by real-time emotion detection and biometric feedback. It generates immersive soundscapes and visuals in response to participants' emotional states using a custom software pipeline.

## Dependencies

- [MediaMTX](https://github.com/bluenviron/mediamtx): Used for glitching video artifacts (via RTMP streaming)
- [Max 8](https://cycling74.com/products/max): For audio synthesis and signal processing
- [Syphon](https://github.com/Syphon/Simple/releases/tag/5): For grabbing video stream in OBS
- Node.js >= 20
- Python >= 3.9

## Visuals (TouchDesigner)

The visual component is created in TouchDesigner and integrated into the feedback loop via a real-time streaming pipeline.

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

## Audio / Max

### Melody

* generate melody using the generateMelody from the node server
* markov chains
