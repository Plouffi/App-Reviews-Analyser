<script setup lang="ts">
import { ref } from 'vue';

const version = ref(VITE_APP_VERSION)
</script>

<template>
  <v-container id="about" class="d-flex justify-center flex-column">
    <v-row>
      <v-col cols="12">
        <v-icon icon="mdi-language-python" color="teal-darken-4"></v-icon>
        <v-icon icon="mdi-vuejs" color="teal-darken-4"></v-icon>
        <v-icon icon="mdi-vuetify" color="teal-darken-4"></v-icon>
      </v-col>
      <v-col cols="12">
        <p>
          App Reviews Analyser is a small tool developped in Python and Vue.js
          to analyse data from reviews data of playstore's application
        </p>
      </v-col>
    </v-row>
    <v-divider class="my-5"></v-divider>
    <v-row>
      <v-col cols="12">
        <v-icon icon="mdi-github" color="teal-darken-4"></v-icon>
      </v-col>
      <v-col cols="12">
        <p>
          You can find the project source on <a href="https://github.com/Plouffi/App-Reviews-Analyser">Github</a>
        </p>
      </v-col>
    </v-row>
    <v-divider class="my-5"></v-divider>
    <v-row>
      <v-col cols="12">
        <v-icon icon="mdi-email" color="teal-darken-4"></v-icon>
      </v-col>
      <v-col cols="12">
        <p>
          Contact me at <a href="mailto:plouffi.github@gmail.com">plouffi.github@gmail.com</a>
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <p class="text-caption">
          Version: {{ version }}
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#about {
  margin-top: 2em;
  text-align: center;
}

.v-icon {
  font-size: 4em;
  margin: 0 15px;
}
</style>