<script>
  export let testResults;
  export let onRestart;

  $: score = testResults?.eye_comfort_score || 0;
  $: category = testResults?.category || 'Unknown';
  $: blinkRate = testResults?.blink_rate || 0;
  $: totalBlinks = testResults?.total_blinks || 0;
  $: duration = testResults?.duration || 0;
  $: avgEar = testResults?.avg_ear || 0;
  $: avgDistance = testResults?.avg_distance || 0;
  $: recommendation = testResults?.recommendation || 'No recommendation available';

  $: scoreColor = score >= 80 ? '#10b981' : score >= 60 ? '#f59e0b' : score >= 40 ? '#f97316' : '#ef4444';
  $: scoreLabel = score >= 80 ? 'Excellent' : score >= 60 ? 'Good' : score >= 40 ? 'Fair' : 'Needs Attention';
</script>

<div class="results-container">
  <div class="content">
    <h1>Test Results</h1>

    <div class="score-card">
      <div class="score-circle" style="--score-color: {scoreColor}">
        <div class="score-value">{score}</div>
        <div class="score-label">Eye Comfort Score</div>
      </div>
      <div class="score-category">{scoreLabel}</div>
    </div>

    <div class="metrics-grid">
      <div class="metric-card">
        <div class="metric-icon">👁️</div>
        <div class="metric-value">{blinkRate}/min</div>
        <div class="metric-label">Blink Rate</div>
      </div>
      <div class="metric-card">
        <div class="metric-icon">⏱️</div>
        <div class="metric-value">{duration}s</div>
        <div class="metric-label">Duration</div>
      </div>
      <div class="metric-card">
        <div class="metric-icon">✨</div>
        <div class="metric-value">{totalBlinks}</div>
        <div class="metric-label">Total Blinks</div>
      </div>
      <div class="metric-card">
        <div class="metric-icon">📏</div>
        <div class="metric-value">{avgEar}</div>
        <div class="metric-label">Avg EAR</div>
      </div>
    </div>

    <div class="category-card">
      <h2>Category: {category}</h2>
    </div>

    <div class="recommendation-card">
      <h2>Recommendation</h2>
      <p class="recommendation-text">{recommendation}</p>
    </div>

    <div class="tips-card">
      <h2>Eye Care Tips</h2>
      <ul class="tips">
        <li>Follow the 20-20-20 rule: Every 20 minutes, look at something 20 feet away for 20 seconds</li>
        <li>Ensure proper lighting when reading or using screens</li>
        <li>Stay hydrated to maintain healthy tear production</li>
        <li>Take regular breaks from digital devices</li>
        <li>Consider using artificial tears if you experience dry eyes</li>
      </ul>
    </div>

    <button class="restart-btn" on:click={onRestart}>
      Take Test Again
    </button>
  </div>
</div>

<style>
  .results-container {
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

  .score-card {
    text-align: center;
    margin-bottom: 2rem;
  }

  .score-circle {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: var(--score-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  }

  .score-value {
    font-size: 4rem;
    font-weight: 700;
    color: white;
  }

  .score-label {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
  }

  .score-category {
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .metric-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
  }

  .metric-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }

  .metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 0.25rem;
  }

  .metric-label {
    font-size: 0.9rem;
    color: #666;
  }

  .category-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
  }

  .category-card h2 {
    color: white;
    font-size: 1.5rem;
    margin: 0;
  }

  .recommendation-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .recommendation-card h2 {
    color: #667eea;
    font-size: 1.3rem;
    margin-bottom: 1rem;
  }

  .recommendation-text {
    color: #555;
    line-height: 1.8;
    white-space: pre-line;
  }

  .tips-card {
    background: #fff3cd;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }

  .tips-card h2 {
    color: #856404;
    font-size: 1.3rem;
    margin-bottom: 1rem;
  }

  .tips {
    padding-left: 1.5rem;
    line-height: 1.8;
    color: #856404;
  }

  .tips li {
    margin-bottom: 0.5rem;
  }

  .restart-btn {
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
  }

  .restart-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
  }

  .restart-btn:active {
    transform: translateY(0);
  }
</style>
