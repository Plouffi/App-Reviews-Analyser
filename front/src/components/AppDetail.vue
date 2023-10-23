<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { GpsApp } from '@/gpsApp';
import ColorThief from 'colorthief'

const props = defineProps({ appId: String })
const app = ref(new GpsApp())
const color = ref({ r: 0, g: 0, b: 0 })
const loadDetail = ref(true)
const loadScrapping = ref()
const urlBackground = computed(() => `url(${app.value.headerImage}`)
const gradientColorBackground = computed(() => `rgba(${color.value.r}, ${color.value.g}, ${color.value.b}, 1) 80%`)

const fetchAppDetail = async (id: string): Promise<GpsApp> => {
	const params: { [k: string]: any } = {}
	params.id = id
	const query = new URLSearchParams(params)
	const res = await fetch(`http://localhost:5173/api/appDetail?${query}`, {
		method: 'GET',
	})
	return res.json()
}

watchEffect(async () => {
	if (props.appId) {
		loadDetail.value = true
		const resApp = await fetchAppDetail(props.appId)
		app.value = resApp

		const colorThief = new ColorThief()
		colorThief.getColorFromUrl(app.value.headerImage, (c: any) => {
			color.value.r = c[0]
			color.value.g = c[1]
			color.value.b = c[2]
		}, 10)

		loadDetail.value = false
	}
})


const scrapApp = async () => {
	// TODO: call server to begin the scrapping
	console.log(loadDetail.value)
}
</script>

<template>
	<v-card :loading="loadDetail" class="gps-app-detail">
		<v-container fluid class="input-analiser">
			<v-card-title>{{ app.title }}</v-card-title>
			<v-card-subtitle><a :href="app.developerWebsite">{{ app.developer }}</a></v-card-subtitle>
			<v-row>
				<v-col>
					<v-img :src="app.icon" class="gps-app-icon"></v-img>
				</v-col>
				<v-col>
					<v-card-text>{{ app.score }}</v-card-text>
				</v-col>
				<v-col>
					<v-card-text>{{ app.reviews }}</v-card-text>
				</v-col>
				<v-col>
					<v-card-text>{{ app.realInstalls }}</v-card-text>
				</v-col>
			</v-row>
			<v-row>
				<template v-for="category in app.categories.sort((a, b) => a > b ? 1 : -1)">
					<v-chip variant="outlined" class="m-1">{{ category }}</v-chip>
				</template>
			</v-row>
			<v-overlay v-model="loadDetail" contained class="align-center justify-center">
				<v-progress-circular :size="60" :witdh="60" color="light-blue-darken-2" indeterminate />
			</v-overlay>
		</v-container>
		<v-card-actions class="mb-3">
			<v-btn @click="scrapApp()" color="light-blue-darken-2" variant="flat" elevation="4">Fetch Data</v-btn>
		</v-card-actions>
	</v-card>
</template>

<style scoped>
.gps-app-detail {
	background: linear-gradient(rgba(0, 0, 0, 0), v-bind(gradientColorBackground)), v-bind(urlBackground);
	background-repeat: no-repeat;
	background-size: cover;
	background-position: center center;
	color: white;

}

.gps-app-icon {
	width: 128px;
	margin: 2em;
	border-radius: 20%;
}
</style>