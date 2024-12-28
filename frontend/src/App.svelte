<script lang="ts">
  import type { BannerType, BannerRequest, BannerResponse } from './types';

  let bannerType: BannerType = 'standard';
  let currentPity = 0;
  let plannedPulls = 1;
  let guaranteed = false;
  let result: BannerResponse | null = null;
  let error: string | null = null;
  let loading = false;

  async function calculateProbability() {
    try {
      loading = true;
      error = null;
      
      const endpoint = `/api/${bannerType}`;
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          current_pity: currentPity,
          planned_pulls: plannedPulls,
          guaranteed
        } as BannerRequest)
      });

      if (!response.ok) {
        throw new Error('Failed to calculate probabilities');
      }

      result = await response.json();
    } catch (e) {
      error = e instanceof Error ? e.message : 'An error occurred';
    } finally {
      loading = false;
    }
  }
</script>

<main class="main-container">
  <div class="content-wrapper">
    <h1 class="page-title">
      HSR Banner Calculator
    </h1>
    <section class="form-container">
      <form on:submit|preventDefault={calculateProbability} class="form-group">
        <div class="form-input-container">
          <label class="form-label" for="bannerType">
            Banner Type
          </label>
          <select
            id="bannerType"
            bind:value={bannerType}
            class="form-input"
          >
            <option value="standard">Standard Banner</option>
            <option value="limited">Limited Banner</option>
          </select>
        </div>

        <div class="form-input-container">
          <label class="form-label" for="currentPity">
            Current Pity
          </label>
          <input
            type="number"
            id="currentPity"
            bind:value={currentPity}
            min="0"
            max="89"
            class="form-input"
          />
          <p class="form-helper">Number of pulls since last 5★ (0-89)</p>
        </div>

        <div class="form-input-container">
          <label class="form-label" for="plannedPulls">
            Planned Pulls
          </label>
          <input
            type="number"
            id="plannedPulls"
            bind:value={plannedPulls}
            min="1"
            class="form-input"
          />
        </div>

        {#if bannerType === 'limited'}
          <div class="flex items-center space-x-2 justify-center">
            <input
              type="checkbox"
              id="guaranteed"
              bind:checked={guaranteed}
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label class="checkbox-label" for="guaranteed">
              Guaranteed Rate-Up (Lost previous 50/50)
            </label>
          </div>
        {/if}

        <button
          type="submit"
          disabled={loading}
          class="w-full bg-blue-600 text-white rounded-md py-2 px-4 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {loading ? 'Calculating...' : 'Calculate'}
        </button>
      </form>

      {#if error}
        <div class="error-message">
          {error}
        </div>
      {/if}

      {#if result}
        <div class="results-container">
          <h2 class="results-title">Results</h2>
          <div class="results-text">
            <p>5★ Probability: <span class="font-medium">{result.total_5_star_probability?.toFixed(2) || '0.00'}%</span></p>
            
            {#if bannerType === 'standard'}
              <p>Character Probability: <span class="font-medium">{result.character_probability?.toFixed(2) || '0.00'}%</span></p>
              <p>Light Cone Probability: <span class="font-medium">{result.light_cone_probability?.toFixed(2) || '0.00'}%</span></p>
            {:else}
              <p>Rate-Up Probability: <span class="font-medium">{result.rate_up_probability?.toFixed(2) || '0.00'}%</span></p>
              <p>Standard Character Probability: <span class="font-medium">{result.standard_char_probability?.toFixed(2) || '0.00'}%</span></p>
            {/if}
          </div>
        </div>
      {/if}
    </section>
  </div>
</main> 