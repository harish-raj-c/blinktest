<script>
  export let onComplete;

  let status = "initializing";
  let calibrationStatus = "Checking camera...";
  let isReady = false;
  let testRunning = false;
  let elapsed = 0;
  let blinkCount = 0;
  let websocket = null;
  let testDuration = 30;
  let face_detected = false;
  let depth_center = null;
  const MIN_DEPTH = 100;
  const MAX_DEPTH = 150;

  const readingText = `The human eye is a remarkable organ that allows us to perceive the world around us. It works by capturing light and converting it into electrical signals that the brain can interpret. The eye consists of several parts including the cornea, lens, retina, and optic nerve. When we read, our eyes perform rapid movements called saccades to scan across the text. During reading, it's important to blink regularly to keep the eyes moist and comfortable. Blinking helps spread tears across the surface of the eye, preventing dryness and irritation. Many people tend to blink less frequently when focusing on screens or reading, which can lead to eye strain and discomfort. This test measures your natural blinking patterns while you read to assess your eye comfort and provide personalized recommendations for maintaining healthy vision.`;

  async function connectWebSocket() {
    try {
      websocket = new WebSocket("ws://localhost:8008/ws");

      websocket.onopen = () => {
        console.log("WebSocket connected");
        status = "connected";
      };

      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "status") {
          calibrationStatus = data.status;
          isReady = data.ready;
          testRunning = data.running;
          elapsed = data.elapsed || 0;
          blinkCount = data.blink_count || 0;
          face_detected = data.face_detected || false;
          depth_center = data.depth_center || null;

          if (testRunning && elapsed >= testDuration) {
            stopTest();
          }
        }
      };

      websocket.onerror = (error) => {
        console.error("WebSocket error:", error);
        calibrationStatus = "Connection error";
      };

      websocket.onclose = () => {
        console.log("WebSocket closed");
        if (testRunning) {
          // Attempt to reconnect
          setTimeout(connectWebSocket, 1000);
        }
      };
    } catch (error) {
      console.error("Failed to connect:", error);
      calibrationStatus = "Failed to connect to server";
    }
  }

  async function startTest() {
    try {
      const response = await fetch("http://localhost:8008/api/start", {
        method: "POST",
      });
      const data = await response.json();

      if (data.success) {
        testRunning = true;
      } else {
        calibrationStatus = data.message;
      }
    } catch (error) {
      console.error("Failed to start test:", error);
      calibrationStatus = "Failed to start test";
    }
  }

  async function stopTest() {
    testRunning = false;

    try {
      const response = await fetch("http://localhost:8008/api/stop", {
        method: "POST",
      });
      const data = await response.json();

      if (data.success && websocket) {
        websocket.close();
      }

      onComplete(data.results || {});
    } catch (error) {
      console.error("Failed to stop test:", error);
      onComplete({});
    }
  }

  function handleStart() {
    if (isReady) {
      startTest();
    }
  }

  // Connect on mount
  connectWebSocket();

  // Cleanup on unmount
  import { onDestroy } from "svelte";
  onDestroy(() => {
    if (websocket) {
      websocket.close();
    }
  });
</script>

<div class="reading-container">
  <div class="header">
    <div class="status-bar">
      <div class="status-item">
        <span class="label">Status:</span>
        <span class="value" class:ready={isReady} class:not-ready={!isReady}>
          {calibrationStatus}
        </span>
      </div>
      {#if testRunning}
        <div class="status-item">
          <span class="label">Time:</span>
          <span class="value">{elapsed}s / {testDuration}s</span>
        </div>
        <div class="status-item">
          <span class="label">Blinks:</span>
          <span class="value">{blinkCount}</span>
        </div>
      {/if}
    </div>
  </div>

  <div class="content">
    {#if !testRunning}
      <div class="calibration-message">
        <div
          class="icon"
          class:icon-success={isReady}
          class:icon-warning={!isReady}
        >
          {isReady ? "✅" : "⚠️"}
        </div>
        <h2 class:success={isReady} class:warning={!isReady}>
          {isReady ? "Ready to Start" : "Calibration Required"}
        </h2>
        <div class="status-details">
          <p class="status-message">{calibrationStatus}</p>
          {#if !isReady}
            <div class="checklist">
              <div
                class="check-item"
                class:checked={status ===
                  "Your face is not detected. Please position yourself in front of the camera."}
              >
                <span class="check-icon">{face_detected ? "✓" : "✗"}</span>
                <span>Face detected</span>
              </div>
              <div
                class="check-item"
                class:checked={depth_center !== null &&
                  depth_center >= MIN_DEPTH &&
                  depth_center <= MAX_DEPTH}
              >
                <span class="check-icon"
                  >{depth_center !== null &&
                  depth_center >= MIN_DEPTH &&
                  depth_center <= MAX_DEPTH
                    ? "✓"
                    : "✗"}</span
                >
                <span>Correct distance ({MIN_DEPTH}-{MAX_DEPTH}mm)</span>
              </div>
            </div>
          {/if}
        </div>
        {#if isReady}
          <button class="start-btn" on:click={handleStart}>
            Start Reading Test
          </button>
        {/if}
      </div>
    {:else}
      <div class="reading-content">
        <h2>Read the following text naturally:</h2>
        <p class="text">{readingText}</p>
        <div class="progress-bar">
          <div
            class="progress"
            style="width: {(elapsed / testDuration) * 100}%"
          ></div>
        </div>
        <p class="instruction">
          Keep reading naturally. The test will complete automatically.
        </p>
      </div>
    {/if}
  </div>
</div>

<style>
  .reading-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  .header {
    background: rgba(255, 255, 255, 0.95);
    padding: 1rem 2rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .status-bar {
    display: flex;
    gap: 2rem;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
  }

  .status-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .label {
    font-weight: 600;
    color: #666;
  }

  .value {
    font-weight: 700;
    color: #333;
  }

  .value.ready {
    color: #10b981;
  }

  .value.not-ready {
    color: #ef4444;
  }

  .content {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .calibration-message {
    background: white;
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    max-width: 500px;
  }

  .icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }

  .icon-success {
    animation: pulse 2s infinite;
  }

  .icon-warning {
    animation: shake 0.5s ease-in-out;
  }

  @keyframes pulse {
    0%,
    100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.1);
    }
  }

  @keyframes shake {
    0%,
    100% {
      transform: translateX(0);
    }
    25% {
      transform: translateX(-5px);
    }
    75% {
      transform: translateX(5px);
    }
  }

  .calibration-message h2 {
    font-size: 1.8rem;
    color: #333;
    margin-bottom: 1rem;
  }

  .calibration-message h2.success {
    color: #10b981;
  }

  .calibration-message h2.warning {
    color: #f59e0b;
  }

  .status-details {
    margin-bottom: 1.5rem;
  }

  .status-message {
    color: #666;
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
    font-weight: 500;
  }

  .checklist {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1rem;
    margin-top: 1rem;
  }

  .check-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }

  .check-item:last-child {
    margin-bottom: 0;
  }

  .check-item.checked {
    background: #d1fae5;
    color: #065f46;
  }

  .check-item:not(.checked) {
    background: #fee2e2;
    color: #991b1b;
  }

  .check-icon {
    font-size: 1.2rem;
    font-weight: bold;
  }

  .calibration-message p {
    color: #666;
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
  }

  .start-btn {
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition:
      transform 0.2s,
      box-shadow 0.2s;
  }

  .start-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
  }

  .reading-content {
    background: white;
    border-radius: 20px;
    padding: 3rem;
    max-width: 900px;
    width: 100%;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  }

  .reading-content h2 {
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 1.5rem;
  }

  .text {
    font-size: 1.2rem;
    line-height: 1.8;
    color: #444;
    margin-bottom: 2rem;
    text-align: justify;
  }

  .progress-bar {
    height: 8px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 1rem;
  }

  .progress {
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    transition: width 0.3s ease;
  }

  .instruction {
    color: #666;
    font-style: italic;
    text-align: center;
  }
</style>
