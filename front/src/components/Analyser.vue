<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ScoreDistribution from './ScoreDistribution.vue'
import Means from './Means.vue'
import Wordcloud from './Wordcloud.vue'
import araError from './Error.vue'
import GPSRestResource from '@/services/GPSRestResource';
import Utils from '@/utils';

const ENV = import.meta.env

const gpsResource = new GPSRestResource()
const appId = ref('')
const analyserTab = ref('selectTab') // Model value for the select tab window
const filter = ref('')
const loadSelectApp = ref(false)
const apps = ref() //an app have: id, name, icon -> class ?
const selectError = ref('') // Model value for error message while search proccess

const loadApps = async () => {
	loadSelectApp.value = true
	apps.value = []
	selectError.value = ''
	try {
		const res = await gpsResource.getApps()
		res.forEach((appJson: { [k: string]: any }) => {
			apps.value.push({
				title: appJson.title,
				value: appJson.id,
				prependAvatar: appJson.icon,
				variant: 'elevated',
			})
		})
	} catch (err) {
		if (ENV.MODE == Utils._MODE_MOCK) {
			const res = Utils.getMockSearch('search')
			res.forEach((appJson: { [k: string]: any }) => {
				apps.value.push({
					title: appJson.title,
					value: appJson.id,
					prependAvatar: appJson.icon,
					variant: 'elevated',
				})
			});
		} else {
			selectError.value = `${err}`
		}
	}
	loadSelectApp.value = false
}

onMounted(() => {
	loadApps()
})

const filterApps = (apps: [{ [k: string]: any; }], filter: string) => {
	return filter && filter.trim().toLocaleLowerCase().length ? apps.filter(app => app.title.toLocaleLowerCase().includes(filter)) : apps
}

const selectApp = async (e: any) => {
	appId.value = e.id
	analyserTab.value = 'analyserTab'
}

const returnToSelect = () => {
	filter.value = ''
	analyserTab.value = 'selectTab'
	loadApps()
}
</script>

<template>
	<v-container fluid id="analyser">
		<v-row dense>
			<v-col cols="12">
				<v-row class="d-flex flex-row justify-center align-center px-lg-16" v-if="!(ENV.MODE == Utils._MODE_MOCK)">
					<transition name="fade">
						<v-btn @click="returnToSelect()" icon="mdi-chevron-left" variant="text" class="btn-return"
							v-if="analyserTab == 'analyserTab'" />
					</transition>
					<v-col cols="9" md="6" class="mx-4 p-0">
						<v-text-field :label="$t('analyser.select.title')" v-model="filter" :disabled="loadSelectApp" variant="solo"
							prepend-inner-icon="mdi-magnify" rounded>
						</v-text-field>
					</v-col>
					<v-card class="pa-2" variant="flat" color="red-lighten-2" v-if="ENV.VITE_IS_MOCK">
						<v-card-title>
							<v-icon icon="mdi-alert" size="large"></v-icon>
							Mock data come from Fire Emblem Heroes reviews. Parameters used to generate the mock:
						</v-card-title>
						<v-card-text>
							- Score distribution: 02/02/2020 04:00 <br />
							- Means: 30 <br />
							- Wordcloud: 10 / 2 / English / 0 / 02/02/2017 01:00 / 02/02/2020 04:00 / 02/02/2020 04:00 /
							09/09/2023 10:00
						</v-card-text>
					</v-card>
				</v-row>
			</v-col>
			<v-col cols="12">
				<v-window v-model="analyserTab">
					<v-window-item value="selectTab">
						<v-card :title="$t('analyser.select.result')" v-if="(apps && apps.length) || loadSelectApp">
							<v-list :items="filterApps(apps, filter)" item-props @click:select="selectApp($event)" overflow="true"
								max-height="400" />
							<v-overlay v-model="loadSelectApp" contained class="align-center justify-center">
								<v-progress-circular :size="60" :witdh="60" color="teal-darken-2" indeterminate />
							</v-overlay>
						</v-card>
						<ara-error :msg="selectError" v-if="selectError.length"></ara-error>
					</v-window-item>
					<v-window-item value="analyserTab">
						<div v-if="appId.length">
							<v-row dense>
								<v-col cols="12" md="6">
									<ScoreDistribution :appId="appId" />
								</v-col>
								<v-col cols="12" md="6">
									<Means :appId="appId" />
								</v-col>
							</v-row>
							<v-row dense>
								<v-col cols="12">
									<Wordcloud :appId="appId" />
								</v-col>
							</v-row>
						</div>
					</v-window-item>
				</v-window>
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
