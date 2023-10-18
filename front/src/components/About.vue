<script setup lang="ts">
</script>

<template>
  <div id="about" class="offset-3 col-6">
    <v-icon icon="mdi-language-python" class="mb-5"></v-icon>
    <v-icon icon="mdi-vuejs" class="mb-5"></v-icon>
    <v-icon icon="mdi-vuetify" class="mb-5"></v-icon>
    <p>
      App Reviews Analyser is a small tool developped in Python and Vue.js
       to analyse data from reviews data of playstore's application
    </p>
    <v-divider></v-divider>
    <v-icon icon="mdi-github" class="mb-5"></v-icon>
    <p>
      You can find the project source on <a href="https://github.com/Plouffi/App-Reviews-Analyser">Github</a>
    </p>
    <v-divider></v-divider>
    <v-icon icon="mdi-email" class="mb-5"></v-icon>
    <p>
      Contact me at <a href="mailto:plouffi.github@gmail.com">plouffi.github@gmail.com</a>
    </p>
  </div>
</template>

<style scoped>
#about {
  margin-top: 2em;
  text-align: center;
}
.v-icon {
  font-size: 4em;
  margin: 0 1em;
}
</style>