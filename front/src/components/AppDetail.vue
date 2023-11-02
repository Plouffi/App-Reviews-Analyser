<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { useDisplay } from 'vuetify';
import { GpsApp } from '@/gpsApp';
import araError from './Error.vue'
import GPSRestResource from '@/services/GPSRestResource';
import Utils from '@/utils';
//import ColorThief from 'colorthief'

const ENV = import.meta.env // Environnements variables

const props = defineProps({
	appId: String // App ID 
})
const emit = defineEmits(['loadScrapping', 'scrappingDone'])
const { mdAndUp, smAndDown, xs } = useDisplay()

const gpsResource = new GPSRestResource()
const app = ref(new GpsApp()) // The GPS app
const carousel = ref(0) // Model value to handle the main carousel
const screenshotDialog = ref(false) // Model value to display the dialog screenshot
const screenshotDialogAttr = ref({
	url: '', // Screenshot URL
	width: 0, // Screenshot width
	height: 0 // Screenshot height
})
const detailTab = ref() // Model value for detail tabs
const scrapColor = ref('teal-darken-2') // Scrapping color loading
const loadDetail = ref(true) // Loading flag to display detail
const loadScreenshot = ref(false) // Loading flag to screenshot
const loadScrapping = ref() // Loading flag for scraping process
const detailError = ref('') // Model value for error during detail process
const color = ref({ r: 0, g: 0, b: 0 }) // Model value for the background color
const urlBackground = computed(() => `url(${app.value.headerImage}`) // CSS rules for the background url
const gradientColorBackground = computed(() => `rgba(${color.value.r}, ${color.value.g}, ${color.value.b}, 0.4)`) // CSS rules for the background linear gradient
const gradientColor2Background = computed(() => `rgba(${color.value.r}, ${color.value.g}, ${color.value.b}, 1)`) // CSS rules for the background linear gradient

async function getDetail(): Promise<void> {
	if (props.appId) {
		detailError.value = ''
		detailTab.value = 'detail'
		loadDetail.value = true
		app.value = new GpsApp()
		try {
			const resApp = await gpsResource.getAppDetail(props.appId)
			app.value.init(resApp)
		} catch (err) {
			if (ENV.MODE == Utils._MODE_MOCK) {
				app.value.init(Utils.getMockDetail(props.appId))
			} else {
				detailError.value = `${err}`
				detailTab.value = 'error'
			}
		}

		// const colorThief = new ColorThief()
		// const sourceImage = document.createElement("img");
		// sourceImage.crossOrigin = "Anonymous"
		// sourceImage.addEventListener('load', () => {
		// 	const palette = colorThief.getPalette(sourceImage, 5, 10);
		// 	const c = palette[0];
		// 	color.value.r = c[0]
		// 	color.value.g = c[1]
		// 	color.value.b = c[2]
		// 	loadDetail.value = false
		// });
		// sourceImage.src = app.value.headerImage
		loadDetail.value = false
	}
}
/**
 * Display a screenshot app inside the dialog box
 *
 * @param url The screenshot url
 */
const showSreenshotDialog = async (url: string) => {
	loadScreenshot.value = true
	screenshotDialog.value = true

	const img = document.createElement("img")
	img.addEventListener('load', () => {
		screenshotDialogAttr.value.url = url
		screenshotDialogAttr.value.width = img.naturalWidth
		screenshotDialogAttr.value.height = img.naturalHeight
		loadScreenshot.value = false
	});
	img.src = url
}

/**
 * Function to trigger the scrapping process, disable search until completed
 * 
 * @param appID - The app ID
 */
const scrapApp = () => {
	emit('loadScrapping', true)
	loadScrapping.value = true
	detailTab.value = 'scrapping'
	console.log(props.appId)
}

const retryDetail = () => {
	getDetail()
}

/**
 * Effect to detect change in appID props value to change the detail display
 */
watchEffect(async () => {
	getDetail()
})

</script>

<template>
	<v-card :loading="loadDetail || loadScrapping" id="gps-app-detail" class="mb-2 pa-2" max-height="450">
		<v-window v-model="detailTab">
			<v-window-item value="detail" class="gps-app-detail-tab">
				<v-carousel v-model="carousel" class="detail-app-carousel" direction="vertical" :continuous="false"
					hide-delimiters height="434">
					<template v-slot:prev="{ props }">
						<v-btn class="carousel-btn-top" icon="mdi-chevron-up" variant="plain" @click="carousel--;"
							v-if="carousel > 0" />
					</template>
					<template v-slot:next="{ props }">
						<v-btn class="carousel-btn-bottom" icon="mdi-chevron-down" variant="plain" @click="carousel++;"
							v-if="carousel < 2" />
					</template>
					<v-carousel-item value="0">
						<v-card class="overflow-auto" variant="text" height="434">
							<v-card-item :class="mdAndUp ? '' : 'd-flex justify-center text-center'">
								<v-card-title>{{ app.title }}</v-card-title>
								<v-card-subtitle>
									<a :href="app.developerWebsite" target="_blank">{{ app.developer }}</a>
								</v-card-subtitle>
							</v-card-item>
							<v-card-item>
								<v-row class="gps-app-stats justify-center text-center ma-4" align="center">
									<v-col cols="12" md="3" class="d-flex justify-center mb-sm-4 mb-md-0">
										<v-img :src="app.icon" class="gps-app-icon" max-height="128" max-width="128"
											style="border-radius: 20%;"></v-img>
									</v-col>
									<v-col cols="12" sm="4" md="3">
										<v-card variant="text">
											<v-card-subtitle>{{ $t('scraper.detail.score').toLocaleUpperCase() }}</v-card-subtitle>
											<v-card-text>
												<v-rating :model-value="app.score" :length="5" density="compact" half-increments readonly
													color="white" active-color="white" />
											</v-card-text>
										</v-card>
									</v-col>
									<v-divider :vertical="!xs"></v-divider>
									<v-col cols="12" sm="4" md="3">
										<v-card variant="text">
											<v-card-subtitle>{{ $t('scraper.detail.reviews').toLocaleUpperCase() }}</v-card-subtitle>
											<v-card-text>
												{{ new Intl.NumberFormat("en-US").format(app.reviews) }}
											</v-card-text>
										</v-card>
									</v-col>
									<v-divider :vertical="!xs"></v-divider>
									<v-col cols="12" sm="4" md="3">
										<v-card variant="text">
											<v-card-subtitle>{{ $t('scraper.detail.installs').toLocaleUpperCase() }}</v-card-subtitle>
											<v-card-text>
												{{ new Intl.NumberFormat("en-US").format(app.realInstalls) }}
											</v-card-text>
										</v-card>
									</v-col>
								</v-row>
							</v-card-item>
							<v-card-item>
								<v-row class="ma-2 d-flex justify-center">
									<v-chip v-for="category in app.categories.sort((a, b) => a > b ? 1 : -1)" variant="outlined"
										class="ma-1">
										{{ category }}
									</v-chip>
								</v-row>
							</v-card-item>
						</v-card>
					</v-carousel-item>
					<v-carousel-item value="1" class="gps-description">
						<v-card :class="smAndDown ? 'overflow-auto' : ''" variant="text" height="434">
							<v-row>
								<v-col cols="12" md="6">
									<v-card-item>
										<v-card class="gps-app-summary pa-2" color="white" variant="text" height="400">
											<v-card-title class="d-block text-wrap text-center" style="word-break: break-word">
												{{ app.summary }}
											</v-card-title>
											<v-card class="gps-app-description overflow-auto pa-2" color="white" variant="text" height="400">
												<v-card-text v-html="app.descriptionHTML">
												</v-card-text>
											</v-card>
										</v-card>
									</v-card-item>
								</v-col>
								<v-col cols="12" md="6" class="d-flex align-center">
									<v-container>
										<v-carousel cycle interval="3000" :show-arrows="false" hide-delimiters height="300">
											<v-carousel-item v-for="screenshot in app.screenshots">
												<v-img :src="screenshot" @click="showSreenshotDialog(screenshot)"
													class="gps-screenshot-carousel"></v-img>
											</v-carousel-item>
											<v-dialog v-model="screenshotDialog" eager close-on-content-click width="auto">
												<v-img :src="screenshotDialogAttr.url" :width="screenshotDialogAttr.width"
													:height="screenshotDialogAttr.height"></v-img>
												<v-overlay v-model="loadScreenshot" contained class="align-center justify-center">
													<v-progress-circular :size="60" :witdh="60" color="teal-darken-2" indeterminate />
												</v-overlay>
											</v-dialog>
										</v-carousel>
									</v-container>
								</v-col>
							</v-row>
						</v-card>
					</v-carousel-item>
					<v-carousel-item value="2">
						<v-container class="fill-height text-center" align="center" style="justify-content: center;">
							<iframe width="560" height="315" :src="app.video" frameborder="0"
								allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
						</v-container>
					</v-carousel-item>
				</v-carousel>
			</v-window-item>
			<v-window-item value="scrapping" class="gps-app-detail-tab">
				<v-row class="text-center mx-auto">
					<v-col cols="12" class="flex-column justify-center pa-2 mt-4">
						<v-card-title>{{ $t('scraper.detail.scrapping.title').toLocaleUpperCase() }}</v-card-title>
						<v-card-title>{{ $t('scraper.detail.scrapping.message') }}</v-card-title>
					</v-col>
					<v-col cols="12" class="d-flex justify-center pa-2">
						<v-carousel cycle :interval="10000" :hide-delimiters="true" :hide-delimiter-background="false"
							:show-arrows="false" height="200">
							<v-carousel-item v-for="comment in app.comments" class="mx-2 px-6">
								<v-card-text class="overflow-auto">
									{{ comment }}
								</v-card-text>
							</v-carousel-item>
						</v-carousel>
					</v-col>
					<v-col cols="12" class="d-flex justify-center">
						<v-progress-circular :size="60" :witdh="60" color="teal-darken-2" indeterminate v-if="loadScrapping" />
					</v-col>
				</v-row>
			</v-window-item>
			<v-window-item value="error">
				<v-row class="text-center">
					<v-col cols="12" class="d-flex justify-center align-center pa-2 ma-4">
						<ara-error :msg="detailError" v-if="detailError.length"></ara-error>
					</v-col>
					<v-col cols="12" class="d-flex justify-center align-center pa-2 ma-4">
						<v-btn @click="retryDetail()" color="teal-darken-2" variant="flat" elevation="4">
							{{ $t('scraper.detail.button.retry') }}
						</v-btn>
					</v-col>
				</v-row>
			</v-window-item>
		</v-window>
		<v-overlay v-model="loadDetail" contained class="align-center justify-center">
			<v-progress-circular :size="60" :witdh="60" color="teal-darken-2" indeterminate />
		</v-overlay>
	</v-card>
	<v-container class="text-center">
		<v-btn @click="scrapApp()" color="teal-darken-2" variant="flat" elevation="4">
			{{ $t('scraper.detail.button.extract') }}
		</v-btn>
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

#gps-app-detail .v-window-item,
#gps-app-detail .v-window,
.v-sheet,
.gps-app-detail-tab * {
	background: none !important;
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
	color: rgba(0, 121, 107, 1);
}

.v-card-subtitle>a:hover {
	text-decoration: underline;
	background: none;
}

.gps-app-icon {
	width: 128px;
	border-radius: 20%;
}

.gps-app-stats .v-card-text {
	min-height: 64px;
	font-size: 1em;
}

.v-divider {
	opacity: 0.8;
}

.gps-app-description {
	-ms-overflow-style: none;
	scrollbar-width: none;
}

.gps-app-description::-webkit-scrollbar {
	display: none;
}

.gps-screenshot-carousel {
	cursor: pointer;
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