<script setup lang="ts">
import ScoreDistribution from './ScoreDistribution.vue'
import Means from './Means.vue'
import Wordcloud from './Wordcloud.vue'
import SelectApp from './SelectApp.vue';
import Utils from '@/utils';

const ENV = import.meta.env
</script>

<template>
  <v-container fluid id="analyser">
    <v-row dense>
      <v-col cols="12">
        <SelectApp v-if="!(ENV.MODE == Utils._MODE_MOCK)" />
        <v-card class="pa-2" variant="flat" color="red-lighten-2" v-if="ENV.VITE_IS_MOCK">
          <v-card-title>
            <v-icon icon="mdi-alert" size="large"></v-icon>
            Mock data come from Fire Emblem Heroes reviews. Parameters used to generate the mock:
          </v-card-title>
          <v-card-text>
            - Score distribution: 02/02/2020 04:00 <br />
            - Score distribution: 30 <br />
            - Score distribution: 10 / 2 / English / 0 / 02/02/2017 01:00 / 02/02/2020 04:00 / 02/02/2020 04:00 /
            09/09/2023 10:00
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="12" md="6">
        <ScoreDistribution />
      </v-col>
      <v-col cols="12" md="6">
        <Means />
      </v-col>
    </v-row>
    <v-row dense>
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
