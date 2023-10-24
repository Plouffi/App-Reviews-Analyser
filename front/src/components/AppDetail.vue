<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { GpsApp } from '@/gpsApp';
import ColorThief from 'colorthief'

const props = defineProps({ appId: String })
const app = ref(new GpsApp())
const carousel = ref(0)
// Loading flags
const loadDetail = ref(true)
const loadScrapping = ref()
// Ref and computed values to handle the detail background card
const color = ref({ r: 0, g: 0, b: 0 })
const urlBackground = computed(() => `url(${app.value.headerImage}`)
const gradientColorBackground = computed(() => `rgba(${color.value.r}, ${color.value.g}, ${color.value.b}, 0.4)`)
const gradientColor2Background = computed(() => `rgba(${color.value.r}, ${color.value.g}, ${color.value.b}, 1)`)

const fetchAppDetail = async (id: string): Promise<GpsApp> => {
	const params: { [k: string]: any } = {}
	params.id = id
	const query = new URLSearchParams(params)
	const res = await fetch(`http://localhost:5173/api/appDetail?${query}`, {
		method: 'GET',
	})
	return res.json()
}

const scrapApp = async () => {
	// TODO: call server to begin the scrapping
	console.log(loadDetail.value)
}

watchEffect(async () => {
	if (props.appId) {
		loadDetail.value = true
		app.value = new GpsApp()
		const resApp = await fetchAppDetail(props.appId)
		console.log(resApp)
		app.value.init(resApp)

		const colorThief = new ColorThief()
		const sourceImage = document.createElement("img");
		sourceImage.crossOrigin = "Anonymous"
		sourceImage.addEventListener('load', () => {
			const palette = colorThief.getPalette(sourceImage, 5, 10);
			const c = palette[0];
			color.value.r = c[0]
			color.value.g = c[1]
			color.value.b = c[2]
			loadDetail.value = false
		});
		sourceImage.src = app.value.headerImage
	}
})

</script>

<template>
	<v-card :loading="loadDetail" id="gps-app-detail" class="mb-2 p-2 overflow-auto" max-height="450">
		<v-carousel v-model="carousel" class="detail-app-carousel" direction="vertical" hide-delimiters :continuous="false"
			height="434" :touch="true">
			<template v-slot:prev="{ props }">
				<v-btn class="carousel-btn-top" icon="mdi-chevron-up" variant="plain"
					@click="props.onClick; carousel = Math.max(carousel - 1, 0)" v-if="carousel > 0" />
			</template>
			<template v-slot:next="{ props }">
				<v-btn class="carousel-btn-bottom" icon="mdi-chevron-down" variant="plain"
					@click="props.onClick; carousel = Math.max(carousel - 1, 1)" v-if="carousel < 1" />
			</template>
			<v-carousel-item>
				<v-card-item>
					<v-card-title>{{ app.title }}</v-card-title>
					<v-card-subtitle>
						<a :href="app.developerWebsite" target="_blank">{{ app.developer }}</a>
					</v-card-subtitle>
				</v-card-item>
				<v-card-item>
					<v-row class="text-center m-4" align="center">
						<v-col>
							<v-img :src="app.icon" class="gps-app-icon"></v-img>
						</v-col>
						<v-col>
							<v-card-subtitle>SCORE</v-card-subtitle>
							<v-card-text>
								{{ new Intl.NumberFormat("en-US", { maximumSignificantDigits: 2 }).format(app.score) }}
								<v-icon icon="mdi-star"></v-icon>
							</v-card-text>
						</v-col>
						<v-divider vertical></v-divider>
						<v-col>
							<v-card-subtitle>REVIEWS</v-card-subtitle>
							<v-card-text>{{ app.reviews }}</v-card-text>
						</v-col>
						<v-divider vertical></v-divider>
						<v-col>
							<v-card-subtitle>INSTALLS</v-card-subtitle>
							<v-card-text>{{ app.realInstalls }}</v-card-text>
						</v-col>
					</v-row>
				</v-card-item>
				<v-card-item>
					<v-row class="m-2">
						<v-chip v-for="category in app.categories.sort((a, b) => a > b ? 1 : -1)" variant="outlined" class="m-1">
							{{ category }}
						</v-chip>
					</v-row>
				</v-card-item>
			</v-carousel-item>
			<v-carousel-item class="gps-description">
				<v-row>
					<v-col cols="6">
						<v-card-item>
							<v-card-title>{{ app.summary }}</v-card-title>
						</v-card-item>
						<v-carousel cycle interval="3000" :show-arrows="false" hide-delimiters height="250" :touch="true">
							<v-carousel-item v-for="screenshot in app.screenshots" :src="screenshot"></v-carousel-item>
						</v-carousel>
					</v-col>
					<v-col cols="6">
						<v-card-item>
							<v-card class="gps-app-description overflow-auto p-2" color="white" variant="text" height="400">
								<v-card-text v-html="app.descriptionHTML">
								</v-card-text>
							</v-card>
						</v-card-item>
					</v-col>
				</v-row>
			</v-carousel-item>
		</v-carousel>
		<v-overlay v-model="loadDetail" contained class="align-center justify-center">
			<v-progress-circular :size="60" :witdh="60" color="light-blue-darken-2" indeterminate />
		</v-overlay>
	</v-card>
	<v-container class="text-center">
		<v-btn @click="scrapApp()" color="light-blue-darken-2" variant="flat" elevation="4">Fetch Data</v-btn>
	</v-container>
</template>

<style scoped>
#gps-app-detail {
	height: 450px;
	background: linear-gradient(v-bind(gradientColorBackground), v-bind(gradientColor2Background)), v-bind(urlBackground);
	background-repeat: no-repeat;
	background-size: cover;
	background-position: center center;
	color: white;
}

.v-card-title {
	font-weight: bold;
}

.v-card-subtitle {
	font-weight: bold;
	opacity: 1;
}

.v-card-subtitle>a {
	text-decoration: none;
	font-weight: bold;
	color: #0288D1;
}

.v-card-subtitle>a:hover {
	text-decoration: underline;
	background: none;
}

.gps-app-icon {
	width: 128px;
	border-radius: 20%;
}

.v-divider {
	opacity: 1;
}

.gps-app-description {
	-ms-overflow-style: none;
	scrollbar-width: none;
}

.gps-app-description::-webkit-scrollbar {
	display: none;
}
</style>

<style>
.detail-app-carousel .v-window__controls {
	justify-content: center;
}

.carousel-btn-top {
	position: absolute !important;
	top: 0 !important;
	height: 2em !important;
}

.carousel-btn-bottom {
	position: absolute !important;
	bottom: 0 !important;
	height: 2em !important;
}
</style>