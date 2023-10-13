<script setup lang="ts">
import ScoreDistribution from './ScoreDistribution.vue'
import Means from './Means.vue'
import Wordcloud from './Wordcloud.vue'
</script>

<template>
  <div class="row">
    <div class="col">
      <ScoreDistribution/>
    </div>
    <div class="col">
      <Means/>
    </div>
    <div class="row">
      <Wordcloud/>
    </div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}
</style>
