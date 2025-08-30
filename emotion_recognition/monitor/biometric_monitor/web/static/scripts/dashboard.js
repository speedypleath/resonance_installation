// WebSocket connection
const socket = io();
const channelNames = ["TP9", "AF7", "AF8", "TP10"];

// Global state
let emotionCount = 0;
let eegFragmentCount = 0;
let gsrAnalysisCount = 0;
let oscMessageCount = 0;
let systemStartTime = Date.now();
let cameraFpsCounter = 0;
let lastCameraUpdate = Date.now();

// GSR data buffers
let gsrDataBuffer = [];
let gsrTimestampBuffer = [];
const maxBufferSize = 1000;

// Camera feed management
function initializeCameraFeed() {
  const cameraFeed = document.getElementById("cameraFeed");
  const cameraStatus = document.getElementById("cameraStatus");

  cameraFeed.onload = function () {
    cameraStatus.textContent = "Camera: Connected";
    updateCameraFPS();
  };

  cameraFeed.onerror = function () {
    cameraStatus.textContent = "Camera: Error";
    cameraFeed.style.display = "none";
    showCameraError();
  };

  setInterval(refreshCameraFeed, 5000);
}

function refreshCameraFeed() {
  const cameraFeed = document.getElementById("cameraFeed");
  if (cameraFeed.src) {
    const baseUrl = "/video_feed";
    const timestamp = new Date().getTime();
    cameraFeed.src = baseUrl + "?t=" + timestamp;
  }
}

function updateCameraFPS() {
  cameraFpsCounter++;
  const now = Date.now();
  const elapsed = (now - lastCameraUpdate) / 1000;

  if (elapsed >= 1.0) {
    const fps = cameraFpsCounter / elapsed;
    document.getElementById("fpsCounter").textContent = "FPS: " + fps.toFixed(1);
    cameraFpsCounter = 0;
    lastCameraUpdate = now;
  }
}

function showCameraError() {
  const cameraFeed = document.getElementById("cameraFeed");
  cameraFeed.style.display = "none";

  const container = cameraFeed.parentElement;
  if (!container.querySelector(".camera-error")) {
    const errorDiv = document.createElement("div");
    errorDiv.className = "camera-error";
    errorDiv.innerHTML = 
      '<div>' +
        '<div style="font-size: 2rem; margin-bottom: 10px;">📷</div>' +
        '<div>Camera not available</div>' +
        '<div style="font-size: 0.8rem; margin-top: 10px; opacity: 0.7;">' +
          'Start emotion recognition to enable camera feed' +
        '</div>' +
      '</div>';
    container.appendChild(errorDiv);
  }
}

function hideCameraError() {
  const cameraFeed = document.getElementById("cameraFeed");
  const container = cameraFeed.parentElement;
  const errorDiv = container.querySelector(".camera-error");

  if (errorDiv) {
    errorDiv.remove();
  }

  cameraFeed.style.display = "block";
}

// Connection handling
socket.on("connect", function () {
  document.getElementById("connectionStatus").className = "status-dot status-connected";
  document.getElementById("connectionText").textContent = "Connected";
  addLog("Connected to server");
  requestStats();
});

socket.on("disconnect", function () {
  document.getElementById("connectionStatus").className = "status-dot status-disconnected";
  document.getElementById("connectionText").textContent = "Disconnected";
  addLog("Disconnected from server");
});

// Pipeline control functions
function startPipeline(pipelineName) {
  socket.emit("request_pipeline_control", {
    action: "start",
    pipeline: pipelineName,
  });
}

function stopPipeline(pipelineName) {
  socket.emit("request_pipeline_control", {
    action: "stop",
    pipeline: pipelineName,
  });
}

function startAllPipelines() {
  startPipeline("facial_emotion");
  startPipeline("gsr_stress_detection");
  startPipeline("eeg_processing");
}

function stopAllPipelines() {
  stopPipeline("facial_emotion");
  stopPipeline("gsr_stress_detection");
  stopPipeline("eeg_processing");
}

function pauseAllPipelines() {
  socket.emit("request_pipeline_control", {
    action: "pause",
    pipeline: "all",
  });
}

function resumeAllPipelines() {
  socket.emit("request_pipeline_control", {
    action: "resume",
    pipeline: "all",
  });
}

function testOSC() {
  fetch("/api/osc/test", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ client: "default" }),
  })
    .then((response) => response.json())
    .then((data) => {
      addLog("OSC test: " + (data.success ? "Success" : "Failed"));
    })
    .catch((error) => {
      addLog("OSC test error: " + error);
    });
}

function requestStats() {
  socket.emit("request_stats");
}

// Data handlers
socket.on("emotion_update", function (data) {
  updateEmotionDisplay(data);
  emotionCount++;
  updateStats();
});

socket.on("eeg_update", function (data) {
  updateEEGDisplay(data);
  eegFragmentCount += data.fragments ? data.fragments.length : 0;
  updateStats();
});

socket.on("gsr_update", function (data) {
  updateGSRDisplay(data);
  gsrAnalysisCount = data.prediction_count
  updateStats();
});

socket.on("pipeline_control_response", function (data) {
  addLog(data.message);
  updatePipelineStatus(data.pipeline, data.action, data.success);
});

socket.on("stats_update", function (data) {
  updateSystemStats(data);
});

socket.on("osc_message", function (data) {
  if (data.address && data.values !== undefined) {
    addOSCMessage(data.address, data.values);
  }
});

// GSR Display Functions
function updateGSRDisplay(data) {
  console.log("GSR Data received:", data);
  
  // Update buffer with raw GSR data
  if (data.raw_data && data.raw_data.samples) {
    const samples = data.raw_data.samples;
    let timestamps = data.raw_data.timestamps;
    
    // If no timestamps provided, generate them based on sampling rate
    if (!timestamps || timestamps.length !== samples.length) {
      const currentTime = Date.now() / 1000;
      timestamps = samples.map((_, i) => currentTime - (samples.length - 1 - i) * 0.25);
    }
    
    for (let i = 0; i < samples.length; i++) {
      if (!isNaN(samples[i]) && isFinite(samples[i])) {
        gsrDataBuffer.push(Number(samples[i]));
        gsrTimestampBuffer.push(Number(timestamps[i]));
      }
    }
    
    // Keep buffer size manageable
    while (gsrDataBuffer.length > maxBufferSize) {
      gsrDataBuffer.shift();
      gsrTimestampBuffer.shift();
    }
    
    // Update live GSR signal plot
    updateGSRSignalPlot();
    addLog("GSR signal updated - " + samples.length + " samples");
  }
  
  // Update stress predictions
  if (data.stress_level) {
      updateStressDisplay(data);
      addLog("GSR Analysis: " + data.stress_level + " (confidence: " + (data.confidence * 100).toFixed(1) + "%)");
    }
  }


function updateGSRSignalPlot() {
  if (gsrDataBuffer.length === 0) return;
  
  // Create time axis relative to first timestamp (in seconds from start)
  const timeAxis = gsrTimestampBuffer.map(ts => ts - gsrTimestampBuffer[0]);
  
  // Ensure we have valid numeric data
  const validData = gsrDataBuffer.filter(val => !isNaN(val) && isFinite(val));
  const validTimes = timeAxis.slice(0, validData.length);
  
  if (validData.length === 0) {
    console.log("No valid GSR data to plot");
    return;
  }
  
  const trace = {
    x: validTimes,
    y: validData,
    type: "scatter",
    mode: "lines",
    line: {
      width: 2,
      color: "#FF6B6B"
    },
    name: "GSR Signal"
  };

  const layout = {
    title: {
      text: "GSR Signal (" + validData.length + " samples)",
      font: { color: "white", size: 14 }
    },
    xaxis: {
      title: "Time (s)",
      color: "white",
      gridcolor: "rgba(255,255,255,0.1)",
      showline: true,
      linecolor: "rgba(255,255,255,0.3)",
      autorange: true
    },
    yaxis: {
      title: "GSR (µS)",
      color: "white",
      gridcolor: "rgba(255,255,255,0.1)",
      showline: true,
      linecolor: "rgba(255,255,255,0.3)",
      autorange: true
    },
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(255,255,255,0.05)",
    font: { color: "white", size: 12 },
    margin: { t: 50, b: 60, l: 60, r: 20 },
    showlegend: false
  };

  Plotly.react("gsrSignalPlot", [trace], layout, { responsive: true });
}

function updateStressDisplay(prediction) {
  // Update main stress display
  document.getElementById("currentStress").textContent = prediction.stress_level;
  document.getElementById("stressConfidenceText").textContent = (prediction.confidence * 100).toFixed(1) + "%";
  document.getElementById("stressConfidenceBar").style.width = (prediction.confidence * 100) + "%";
  
  // Update additional metrics
  if (prediction.arousal_score !== undefined) {
    document.getElementById("arousalScore").textContent = prediction.arousal_score.toFixed(3);
  }

  if (prediction.signal_quality !== undefined) {
    document.getElementById("signalQuality").textContent = prediction.signal_quality.toFixed(3);
  }
  
  if (prediction.features && prediction.features.num_peaks !== undefined) {
    document.getElementById("gsrPeaks").textContent = prediction.features.num_peaks || 0;
  }
  
  // Color code the stress level
  const stressElement = document.getElementById("currentStress");
  if (prediction.stress_level === "Stress") {
    stressElement.style.color = "#FF6B6B";
    document.getElementById("stressConfidenceBar").style.background = "linear-gradient(90deg, #FF6B6B, #FF8A80)";
  } else {
    stressElement.style.color = "#4CAF50";
    document.getElementById("stressConfidenceBar").style.background = "linear-gradient(90deg, #4caf50, #8bc34a)";
  }
}

// Update functions
function updateEmotionDisplay(data) {
  document.getElementById("currentEmotion").textContent = data.emotion;
  document.getElementById("confidenceText").textContent = (data.confidence * 100).toFixed(1) + "%";
  document.getElementById("confidenceBar").style.width = (data.confidence * 100) + "%";

  if (data.vad) {
    document.getElementById("valenceValue").textContent = data.vad.valence.toFixed(3);
    document.getElementById("arousalValue").textContent = data.vad.arousal.toFixed(3);
    document.getElementById("dominanceValue").textContent = data.vad.dominance.toFixed(3);
    
    // Log OSC messages for VAD values
    addOSCMessage("/valence", [data.vad.valence]);
    addOSCMessage("/arousal", [data.vad.arousal]);
    addOSCMessage("/dominance", [data.vad.dominance]);
  }

  // Log emotion label OSC message
  if (data.emotion) {
    addOSCMessage("/emotion", [data.emotion]);
  }

  // Update emotion probabilities chart
  if (data.probabilities) {
    updateEmotionProbChart(data.probabilities);
  }

  addLog("Emotion: " + data.emotion + " (" + (data.confidence * 100).toFixed(1) + "%)");
}

function updateEEGDisplay(data) {
  if (data.fragments && data.fragments.length > 0) {
    const fragment = data.fragments[0];
    updateEEGChannelPlots(fragment);
    addLog("EEG Fragment " + fragment.fragment_id + " processed");
  }
}

function updateEEGChannelPlots(fragment) {
  const colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"];

  for (let ch = 0; ch < channelNames.length && ch < fragment.data[0].length; ch++) {
    const channelData = fragment.data.map((sample) => sample[ch]);
    const timeAxis = fragment.timestamps
      ? fragment.timestamps.map((ts, idx) => idx / 256)
      : fragment.data.map((_, idx) => idx / 256);

    const trace = {
      x: timeAxis,
      y: channelData,
      type: "scatter",
      mode: "lines",
      line: {
        width: 2,
        color: colors[ch],
      },
      showlegend: false,
    };

    const layout = {
      xaxis: {
        title: "Time (s)",
        color: "white",
        gridcolor: "rgba(255,255,255,0.1)",
        showline: true,
        linecolor: "rgba(255,255,255,0.3)",
      },
      yaxis: {
        title: "µV",
        color: "white",
        gridcolor: "rgba(255,255,255,0.1)",
        showline: true,
        linecolor: "rgba(255,255,255,0.3)",
      },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(255,255,255,0.05)",
      font: { color: "white", size: 10 },
      margin: { t: 20, b: 40, l: 50, r: 20 },
    };

    const plotId = "eegPlot" + channelNames[ch];
    Plotly.react(plotId, [trace], layout, { responsive: true });
  }
}

function updateEmotionProbChart(probabilities) {
  const emotions = Object.keys(probabilities);
  const values = Object.values(probabilities);
  const maxIndex = values.indexOf(Math.max(...values));

  const trace = {
    x: emotions,
    y: values,
    type: "bar",
    marker: {
      color: values.map((val, idx) =>
        idx === maxIndex ? "#FFD700" : "#4CAF50"
      ),
      line: {
        color: "rgba(255,255,255,0.2)",
        width: 1,
      },
    },
  };

  const layout = {
    title: {
      text: "Current Emotion Probabilities",
      font: { color: "white" },
    },
    xaxis: {
      color: "white",
      gridcolor: "rgba(255,255,255,0.1)",
    },
    yaxis: {
      title: "Probability",
      color: "white",
      gridcolor: "rgba(255,255,255,0.1)",
      range: [0, 1],
    },
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(255,255,255,0.05)",
    font: { color: "white" },
    margin: { t: 50, b: 60, l: 60, r: 20 },
  };

  Plotly.react("emotionProbPlot", [trace], layout);
}

function updateStats() {
  document.getElementById("emotionCount").textContent = emotionCount;
  document.getElementById("gsrAnalyses").textContent = gsrAnalysisCount;
  document.getElementById("eegFragments").textContent = eegFragmentCount;
  document.getElementById("oscMessages").textContent = oscMessageCount;

  const uptime = Math.floor((Date.now() - systemStartTime) / 1000);
  document.getElementById("uptime").textContent = formatUptime(uptime);
}

function formatUptime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  if (hours > 0) {
    return hours + "h " + minutes + "m";
  } else if (minutes > 0) {
    return minutes + "m " + secs + "s";
  } else {
    return secs + "s";
  }
}

function updatePipelineStatus(pipeline, action, success) {
  let statusElement;

  if (pipeline === "facial_emotion") {
    statusElement = document.getElementById("emotionStatus");
  } else if (pipeline === "eeg_processing") {
    statusElement = document.getElementById("eegStatus");
  } else if (pipeline === "gsr_stress_detection") {
    statusElement = document.getElementById("gsrStatus");
  }

  if (statusElement) {
    if (action === "start" && success) {
      statusElement.className = "status-dot status-processing";
    } else if (action === "stop") {
      statusElement.className = "status-dot status-disconnected";
    }
  }
}

function updateSystemStats(data) {
  if (data.server) {
    const uptime = Math.floor(data.server.uptime);
    document.getElementById("uptime").textContent = formatUptime(uptime);
  }

  if (data.osc && data.osc.clients) {
    let totalMessages = 0;
    Object.values(data.osc.clients).forEach((client) => {
      totalMessages += client.message_count || 0;
    });
    oscMessageCount = totalMessages;
    document.getElementById("oscMessages").textContent = totalMessages;
  }
}

// Logging
function addLog(message) {
  const logContainer = document.getElementById("logContainer");
  const logEntry = document.createElement("div");
  logEntry.className = "log-entry";

  const timestamp = new Date().toLocaleTimeString();
  logEntry.innerHTML = '<span class="log-timestamp">[' + timestamp + ']</span> ' + message;

  logContainer.appendChild(logEntry);
  logContainer.scrollTop = logContainer.scrollHeight;

  // Keep only last 100 log entries
  while (logContainer.children.length > 100) {
    logContainer.removeChild(logContainer.firstChild);
  }
}

function clearLogs() {
  document.getElementById("logContainer").innerHTML = "";
  addLog("Logs cleared");
}

// OSC message logging functions
function addOSCMessage(address, values) {
  const oscContainer = document.getElementById("oscLogContainer");
  const oscEntry = document.createElement("div");
  oscEntry.className = "osc-entry";

  const timestamp = new Date().toLocaleTimeString();
  const valuesStr = Array.isArray(values) ? values.map(v => 
    typeof v === 'number' ? v.toFixed(3) : v
  ).join(', ') : values;

  oscEntry.innerHTML = 
    '<span class="osc-timestamp">[' + timestamp + ']</span>' +
    '<span class="osc-address">' + address + '</span>' +
    '<span class="osc-values">' + valuesStr + '</span>';

  oscContainer.appendChild(oscEntry);

  // Auto-scroll if enabled
  const autoScroll = document.getElementById("oscAutoScroll").checked;
  if (autoScroll) {
    oscContainer.scrollTop = oscContainer.scrollHeight;
  }

  // Keep only last 200 OSC entries
  while (oscContainer.children.length > 200) {
    oscContainer.removeChild(oscContainer.firstChild);
  }

  // Update OSC message counter
  oscMessageCount++;
}

function clearOSCMessages() {
  const oscContainer = document.getElementById("oscLogContainer");
  oscContainer.innerHTML = "";
  addOSCMessage("/system", "OSC log cleared");
}

// Initialize dashboard
window.addEventListener("load", function () {
  addLog("Dashboard initialized");
  initializeCameraFeed();
  initializeEmptyPlots();
  setTimeout(requestStats, 1000);
  setInterval(requestStats, 5000);
  setInterval(updateStats, 1000);
});

function initializeEmptyPlots() {
  const emptyLayout = {
    title: { text: "Waiting for data...", font: { color: "white" } },
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(255,255,255,0.05)",
    font: { color: "white" },
  };

  const emptyEEG = {
    xaxis: {
      title: "Time (s)",
      color: "white",
      gridcolor: "rgba(255,255,255,0.1)",
      showline: true,
      linecolor: "rgba(255,255,255,0.3)",
    },
    yaxis: {
      title: "µV",
      color: "white",
      gridcolor: "rgba(255,255,255,0.1)",
      showline: true,
      linecolor: "rgba(255,255,255,0.3)",
    },
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(255,255,255,0.05)",
    font: { color: "white", size: 10 },
    margin: { t: 20, b: 40, l: 50, r: 20 },
  };

  const emptyGSR = {
    title: { text: "Waiting for GSR data...", font: { color: "white" } },
    xaxis: {
      title: "Time (s)",
      color: "white",
      gridcolor: "rgba(255,255,255,0.1)",
      showline: true,
      linecolor: "rgba(255,255,255,0.3)",
    },
    yaxis: {
      title: "GSR (µS)",
      color: "white",
      gridcolor: "rgba(255,255,255,0.1)",
      showline: true,
      linecolor: "rgba(255,255,255,0.3)",
    },
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(255,255,255,0.05)",
    font: { color: "white", size: 12 },
    margin: { t: 50, b: 60, l: 60, r: 20 },
    showlegend: false
  };

  // Initialize all plots
  Plotly.newPlot("emotionProbPlot", [], emptyLayout);
  Plotly.newPlot("gsrSignalPlot", [], emptyGSR);
  
  for (let ch = 0; ch < channelNames.length; ch++) {
    const plotId = "eegPlot" + channelNames[ch];
    Plotly.newPlot(plotId, [], emptyEEG);
  }
}