<script setup lang="ts">
import ScoreDistribution from './ScoreDistribution.vue'
import Means from './Means.vue'
import Wordcloud from './Wordcloud.vue'
</script>

<template>
  <v-container fluid id="analyser">
    <v-row dense>
      <v-col cols="6">
        <ScoreDistribution />
      </v-col>
      <v-col cols="6">
        <Means />
      </v-col>
      <v-col cols="12">
        <Wordcloud />
      </v-col>
    </v-row>
  </v-container>
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

.v-card {
  padding: 0 1em;
}
</style>
