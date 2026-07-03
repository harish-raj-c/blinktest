<script>
  export let onContinue;
</script>

<div class="instructions-container">
  <div class="content">
    <h1>Eye Blink Test</h1>
    
    <div class="instruction-card">
      <h2>Instructions</h2>
      <ol class="steps">
        <li>
          <strong>Position yourself:</strong> Sit comfortably in front of the camera at an optimal distance (approximately 60-80cm from the screen).
        </li>
        <li>
          <strong>Stay still:</strong> Keep your head steady and maintain a neutral facial expression during the test.
        </li>
        <li>
          <strong>Read naturally:</strong> Read the provided paragraph at your normal reading pace. Don't force yourself to blink or hold your eyes open.
        </li>
        <li>
          <strong>Duration:</strong> The test will run for approximately 30 seconds while you read.
        </li>
        <li>
          <strong>Results:</strong> After the test, you'll receive an eye comfort score and recommendations based on your blink patterns.
        </li>
      </ol>
    </div>

    <div class="tips-card">
      <h2>Tips for Accurate Results</h2>
      <ul class="tips">
        <li>Ensure good lighting on your face</li>
        <li>Remove glasses if they cause glare</li>
        <li>Avoid excessive head movements</li>
        <li>Don't consciously try to control your blinking</li>
      </ul>
    </div>

    <button class="continue-btn" on:click={onContinue}>
      Start Test →
    </button>
  </div>
</div>

<style>
  .instructions-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  .content {
    max-width: 800px;
    width: 100%;
    background: white;
    border-radius: 20px;
    padding: 3rem;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  }

  h1 {
    font-size: 2.5rem;
    color: #333;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 700;
  }

  .instruction-card, .tips-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  h2 {
    font-size: 1.5rem;
    color: #667eea;
    margin-bottom: 1rem;
  }

  .steps {
    padding-left: 1.5rem;
    line-height: 1.8;
    color: #555;
  }

  .steps li {
    margin-bottom: 1rem;
  }

  .steps strong {
    color: #333;
  }

  .tips {
    padding-left: 1.5rem;
    line-height: 1.8;
    color: #555;
  }

  .tips li {
    margin-bottom: 0.5rem;
  }

  .continue-btn {
    width: 100%;
    padding: 1.2rem;
    font-size: 1.2rem;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-top: 1rem;
  }

  .continue-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
  }

  .continue-btn:active {
    transform: translateY(0);
  }
</style>
