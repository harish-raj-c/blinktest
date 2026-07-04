<script>
  import { onDestroy } from 'svelte';
  import Instructions from './pages/Instructions.svelte';
  import ReadingTest from './pages/ReadingTest.svelte';
  import Results from './pages/Results.svelte';

  let currentPage = 'instructions';
  let testResults = null;
  let watcherSocket = null;``

  function goToReading() {
    currentPage = 'reading';
  }

  function goToResults(results) {
    testResults = results;
    currentPage = 'results';
  }

  function restart() {
    currentPage = 'instructions';
    testResults = null;
  }

  function connectWatcher() {
    watcherSocket = new WebSocket('ws://localhost:8008/ws');

    watcherSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'status' && data.running && currentPage === 'instructions') {
        goToReading();
      }
    };

    watcherSocket.onclose = () => {
      setTimeout(connectWatcher, 1000);
    };
  }

  connectWatcher();

  onDestroy(() => {
    watcherSocket?.close();
  });
</script>

<main>
  {#if currentPage === 'instructions'}
    <Instructions onContinue={goToReading} />
  {:else if currentPage === 'reading'}
    <ReadingTest onComplete={goToResults} />
  {:else if currentPage === 'results'}
    <Results {testResults} onRestart={restart} />
  {/if}
</main>

<style>
  main {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
</style>
