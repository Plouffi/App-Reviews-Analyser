<script setup lang="ts">
import { ref } from 'vue'
import { useDisplay, useTheme } from 'vuetify'
import ScraperView from './view/Scraper.view.vue'
import AnalyserView from './view/Analyser.view.vue'
import AboutView from './view/About.view.vue'

const { smAndDown } = useDisplay()
const theme = useTheme()

const ENV = import.meta.env // Environnements variables

const themeSelected = ref(theme.global.name.value) // Model value for the selected theme
const languages = ref([{code: 'en', name: 'English'}])
const lang = ref('en')
const tab = ref('scraper') // Init the model window to the Scraper tab

/**
 * Function to select the languague application
 * 
 * @param e The event triggered
 */
 const selectLang = (e: any) => {
	lang.value = e.code
	console.log(lang.value)
}

/**
 * Toggle theme between dark and light
 */
const switchTheme = () => {
	if (theme.global.current.value.dark) {
		themeSelected.value = 'myLightTheme'
		theme.global.name.value = 'myLightTheme'
	} else {
		themeSelected.value = 'myDarkTheme'
		theme.global.name.value = 'myDarkTheme'
	}
}

</script>

<template>
	<v-theme-provider style="height: 100%;" :theme="themeSelected" with-background>
		<header class="ara-header pa-5">
			<v-card class="ara-alert d-flex justify-center align-center pa-2" variant="flat" color="red-lighten-2"
				v-if="ENV.VITE_IS_MOCK">
				<v-icon icon="mdi-alert" size="large"></v-icon>
				<v-card-text>Backend API is down ! Mock data will be display.</v-card-text>
			</v-card>
			<v-toolbar collapse class="ara-toolbar">
				<v-menu location="bottom">
					<template v-slot:activator="{ props }">
						<v-btn icon="mdi-translate" v-bind="props"></v-btn>
					</template>
					<v-list :items="languages" item-title="name" item-value="code" @click:select="selectLang($event)"/>
				</v-menu>
				<v-btn @click="switchTheme()" icon>
					<v-icon :icon="theme.global.current.value.dark ? 'mdi-weather-night' : 'mdi-white-balance-sunny'"></v-icon>
				</v-btn>
			</v-toolbar>
			<img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
			<h1 class="text-center">App Review Analyser</h1>
		</header>
		<v-tabs v-model="tab" fixed-tabs bg-color="rgb(77, 182, 172, 1)" color="teal-darken-2" class="ara-tabs">
			<v-tab value="scraper">{{ $t('tabs.scraper') }}</v-tab>
			<v-tab value="analyser">{{ $t('tabs.analyser') }}</v-tab>
			<v-tab value="about">{{ $t('tabs.about') }}</v-tab>
		</v-tabs>
		<v-container :class="smAndDown ? 'main-content px-0' : 'main-content'">
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
	</v-theme-provider>
</template>

<style scoped>
.ara-header {
	line-height: 1.5;
	background: linear-gradient(rgb(var(--v-theme-header)), rgb(77, 182, 172));
	color: white;
}

.ara-alert {
	position: absolute;
	top: 0;
}

.ara-alert>.v-card-text {
	font-weight: bold;
}

.ara-toolbar {
	position: absolute;
	right: 1rem;
	background: transparent;
}

.logo {
	display: block;
	margin: 0 auto 2rem;
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
