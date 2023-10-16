<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="mb-5">
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
    <h1 class="text-center">App Review Analyser</h1>
  </header>
  <nav class="navbar navbar-expand-lg navbar-light bg-light rounded mb-5">
    <a class="navbar-brand" href="#">
      <img alt="Vue logo" class="logonav" src="@/assets/logo.svg" width="40" height="40" />
    </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <RouterLink to="/home" class="nav-link">About</RouterLink>
        </li>
        <li class="nav-item active">
          <RouterLink to="/scraper" class="nav-link">Scraper</RouterLink>
        </li>
        <li class="nav-item active">
          <RouterLink to="/analyser" class="nav-link">Analyser</RouterLink>
        </li>
      </ul>
    </div>
  </nav>

  <RouterView></RouterView>
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
