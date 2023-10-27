<script setup lang="ts">
import { ref } from 'vue'
import AppDetail from './AppDetail.vue'
import Utils from '@/utils';

const searchTab = ref() // Model value for the search tab window
const appListResult = ref() // Model value for the result list from search
const searchTerm = ref() // Model value for the searched terms
const loadSearch = ref(false) // Loading flag for search
const selectedApp = ref() // Model value for the selected app ID

/**
 * Fetch the search result from the backend API
 *
 * @returns The promise from the fetch API containing search result.
 * If it fails, return a promise with mocked data.
 */
const searchApp = async (): Promise<[{ [k: string]: any }]> => {
	try {
		const params: { [k: string]: any } = {}
		if (searchTerm.value.length) {
			params.search = searchTerm.value
			const query = new URLSearchParams(params)
			const res = await fetch(`http://localhost:5173/api/searchApp?${query}`, {
				method: 'GET',
			})
			if (!res.ok) throw res.statusText
			return res.json()
		}
		throw 'Error params'
	} catch (e) {
		console.error(`Error while requesting /searchApp :${e}`)
		return new Promise<[{ [k: string]: any }]>(function (resolve) {
			resolve(Utils.getMockSearch('search'))
		})
	}
}

/**
 * Function triggered on search (enter key pressed on search bar) to fecth result
 * depending on search term
 */
const onSearch = async () => {
	if (searchTerm.value) {
		searchTab.value = 'list'
		loadSearch.value = true
		const res = await searchApp()
		appListResult.value = []
		res.forEach((appJson: { [k: string]: any }) => {
			appListResult.value.push({
				title: appJson.title,
				value: appJson.id,
				prependAvatar: appJson.icon,
				variant: 'elevated',
			})
		});
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
							v-if="searchTab == 'detail'" />
					</transition>
					<v-col cols="9" md="6" class="mx-4 p-0">
						<v-text-field label="Search app" v-model="searchTerm" v-on:keyup.enter="onSearch()" variant="solo"
							prepend-inner-icon="mdi-magnify" rounded hide-details>
						</v-text-field>
					</v-col>
				</v-row>
			</v-col>
			<v-col cols="12" lg="10" offset="0" offset-lg="1">
				<v-window v-model="searchTab">
					<v-window-item value="list">
						<v-card title="Search results" v-if="(appListResult && appListResult.length) || loadSearch">
							<v-list :items="appListResult" item-props @click:select="selectApp($event)" overflow="true"
								max-height="400" />
							<v-overlay v-model="loadSearch" contained class="align-center justify-center">
								<v-progress-circular :size="60" :witdh="60" color="light-blue-darken-2" indeterminate />
							</v-overlay>
						</v-card>
					</v-window-item>
					<v-window-item value="detail">
						<AppDetail :appId="selectedApp" />
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