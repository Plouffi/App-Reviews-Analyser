<script setup lang="ts">
import { ref } from 'vue'
import AppDetail from './AppDetail.vue'
import Utils from '@/utils';

const result = ref()
const appListResult = ref()
const searchTerm = ref()
const loadSearch = ref(false)
const selectedApp = ref()

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
	} catch(e) {
		console.error(`Error while requesting /searchApp :${e}`)
		return new Promise<[{ [k: string]: any }]>(function(resolve) {
			resolve(Utils.getListMock('search'))
		})
	}
}

const onSearch = async () => {
	if (searchTerm.value) {
		result.value = 'list'
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

const selectApp = (e: any) => {
	selectedApp.value = e.id
	result.value = 'detail'
}

const returnToList = () => {
	result.value = 'list'
}

</script>

<template>
	<v-container fluid id="scraper">
		<v-row dense>
			<v-col cols="12">
				<v-row>
					<v-col cols="1" offset="2">
						<transition name="fade">
							<v-btn @click="returnToList()" icon="mdi-chevron-left" variant="elevated" elevation="4"
								class="btn-return" min-height="56" :min-width="56" v-if="result == 'detail'"/>
						</transition>
					</v-col>
					<v-col cols="6">
						<v-text-field label="Search app" v-model="searchTerm" v-on:keyup.enter="onSearch()" variant="solo"
							prepend-inner-icon="mdi-magnify" rounded hide-details>
						</v-text-field>
					</v-col>
				</v-row>
			</v-col>
			<v-col cols="10" offset="1">
				<v-window v-model="result">
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
</style>