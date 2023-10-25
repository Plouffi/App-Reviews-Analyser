<script setup lang="ts">
import { ref } from 'vue'
import ScraperView from './view/Scraper.view.vue';
import AnalyserView from './view/Analyser.view.vue';
import AboutView from './view/About.view.vue';

const tab = ref("scraper")
</script>

<template>
  <header class="mb-5">
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
    <h1 class="text-center">App Review Analyser</h1>
  </header>
  <v-tabs v-model="tab" bg-color="grey-lighten-3" color="light-blue-darken-2" align-tabs="center" class="mb-5 rounded"
    grow>
    <v-tab value="scraper">Scraper</v-tab>
    <v-tab value="analyser">Analyser</v-tab>
    <v-tab value="about">About</v-tab>
  </v-tabs>
  <v-window v-model="tab">
    <v-window-item value="scraper">
      <ScraperView />
    </v-window-item>
    <v-window-item value="analyser">
      <AnalyserView />
    </v-window-item>
    <v-window-item value="about">
      <AboutView />
    </v-window-item>
  </v-window>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

.logonav {
  display: block;
  margin-left: 1rem;
}
</style>
