<script setup lang="ts">
import Analyzer from './components/Analyzer.vue'
</script>

<template>
  <header class="mb-5">
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
    <h1 class="text-center">App Review Analyzer</h1>
  </header>
  <Analyzer/>

</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}
</style>
