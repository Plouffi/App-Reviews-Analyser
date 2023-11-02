<script setup lang="ts">
import { ref } from 'vue'
import AppDetail from './AppDetail.vue'
import araError from './Error.vue'
import GPSRestResource from '@/services/GPSRestResource';
import Utils from '@/utils';

const ENV = import.meta.env // Environnements variables

const gpsResource = new GPSRestResource()
const searchTab = ref('scraping') // Model value for the search tab window
const appListResult = ref() // Model value for the result list from search
const searchTerm = ref() // Model value for the searched terms
const selectedApp = ref() // Model value for the selected app ID
const loadSearch = ref(false) // Loading flag for search
const loadScraping = ref(false) // Loading flag for scraping
const searchError = ref('') // Model value for error message while search proccess

/**
 * Function triggered on search (enter key pressed on search bar) to fecth result
 * depending on search term
 */
const onSearch = async () => {
	if (searchTerm.value) {
		searchTab.value = 'list' // Return to the list tab if we were on detail tab
		loadSearch.value = true
		searchError.value =''
		appListResult.value = []
		try {
			const res = await gpsResource.searchApp(searchTerm.value)
			res.forEach((appJson: { [k: string]: any }) => {
				appListResult.value.push({
					title: appJson.title,
					value: appJson.id,
					prependAvatar: appJson.icon,
					variant: 'elevated',
				})
			});
		} catch (err) {
			if (ENV.MODE == Utils._MODE_MOCK) {
				const res = Utils.getMockSearch('search')
				res.forEach((appJson: { [k: string]: any }) => {
					appListResult.value.push({
						title: appJson.title,
						value: appJson.id,
						prependAvatar: appJson.icon,
						variant: 'elevated',
					})
				});
			} else {
				searchError.value = `${err}`
			}
		}
		loadSearch.value = false
	}
}

/**
 * Function triggered when an app is selected from the result list.
 * Change the window tab to go the detail window.
 * 
 * @param e - Event fired on click containing the app ID
 */
const selectApp = (e: any) => {
	selectedApp.value = e.id
	searchTab.value = 'detail'
}

/**
 * Function triggered when clicking the return button from the detail window or on a new search.
 * Return to search window
 */
const returnToList = () => {
	searchTab.value = 'list'
}

</script>

<template>
	<v-container fluid id="scraper">
		<v-row dense>
			<v-col cols="12">
				<v-row class="d-flex flex-row justify-center align-center px-lg-16">
					<transition name="fade">
						<v-btn @click="returnToList()" icon="mdi-chevron-left" variant="text" class="btn-return"
							v-if="searchTab == 'detail'" :disabled="loadScraping" />
					</transition>
					<v-col cols="9" md="6" class="mx-4 p-0">
						<v-text-field :label="$t('scraper.search.label')" v-model="searchTerm" v-on:keyup.enter="onSearch()"
							:disabled="loadScraping" variant="solo" prepend-inner-icon="mdi-magnify" rounded hide-details>
						</v-text-field>
					</v-col>
				</v-row>
			</v-col>
			<v-col cols="12" lg="10" offset="0" offset-lg="1">
				<v-window v-model="searchTab">
					<v-window-item value="list">
						<v-card :title="$t('scraper.search.result')" v-if="(appListResult && appListResult.length) || loadSearch">
							<v-list :items="appListResult" item-props @click:select="selectApp($event)" overflow="true"
								max-height="400" />
							<v-overlay v-model="loadSearch" contained class="align-center justify-center">
								<v-progress-circular :size="60" :witdh="60" color="teal-darken-2" indeterminate />
							</v-overlay>
						</v-card>
						<ara-error :msg="searchError" v-if="searchError.length"></ara-error>
					</v-window-item>
					<v-window-item value="detail">
						<AppDetail :appId="selectedApp" @load-scraping="(status) => loadScraping = status"/>
					</v-window-item>
				</v-window>
			</v-col>
		</v-row>
	</v-container>
</template>

<style scoped>
.btn-return {
	font-size: 1.5em;
	height: 56px;
	width: 56px;
}

.fade-enter-active,
.fade-leave-active {
	transition: opacity .5s
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0
}

.v-card {
	padding: 1em;
}

.v-list {
	-ms-overflow-style: none;
	scrollbar-width: none;
}

.v-list::-webkit-scrollbar {
	display: none;
}

.v-window-item {
	padding: 1em;
}

@media (width <=960px) {
	.btn-return {
		height: 36px;
		width: 36px;
	}
}
</style>