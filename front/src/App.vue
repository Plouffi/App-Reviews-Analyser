<script setup lang="ts">
import { ref, computed } from 'vue'
import ScraperView from './view/Scraper.view.vue';
import AnalyserView from './view/Analyser.view.vue';
import AboutView from './view/About.view.vue';

const tab = ref("scraper") // Init the model window to the Scraper tab
const ENV = import.meta.env // Environnementsvariables
</script>

<template>
	<header class="ara-header pa-5">
		<v-card class="ara-alert d-flex justify-center align-center pa-2" variant="flat" color="red-lighten-2"
			v-if="ENV.VITE_IS_MOCK">
			<v-icon icon="mdi-alert" size="large"></v-icon>
			<v-card-text>Backend API is down ! Mock data will be display.</v-card-text>
		</v-card>
		<img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
		<h1 class="text-center">App Review Analyser</h1>
	</header>
	<v-tabs v-model="tab" fixed-tabs bg-color="rgba(178, 223, 219, 1)" color="teal-darken-2" class="ara-tabs">
		<v-tab value="scraper">Scraper</v-tab>
		<v-tab value="analyser">Analyser</v-tab>
		<v-tab value="about">About</v-tab>
	</v-tabs>
	<v-container class="main-content">
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
	</v-container>
</template>

<style scoped>
.ara-header {
	line-height: 1.5;
	background: linear-gradient(rgb(255, 255, 255), rgb(178, 223, 219, 1));
	color: white;
}

.ara-alert {
	position: absolute;
	top: 0;
}

.ara-alert>.v-card-text {
	font-weight: bold;
}

.logo {
	display: block;
	margin: 0 auto 2rem;
}

.logonav {
	display: block;
	margin-left: 1rem;
}

.ara-tabs {
	color: white !important;
	box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.24);
}

.main-content {
	max-width: 1280px;
	padding: 2rem;
}
</style>
