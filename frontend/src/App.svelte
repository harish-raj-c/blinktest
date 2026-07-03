<script>
  import Instructions from './pages/Instructions.svelte';
  import ReadingTest from './pages/ReadingTest.svelte';
  import Results from './pages/Results.svelte';

  let currentPage = 'instructions';
  let testResults = null;

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
