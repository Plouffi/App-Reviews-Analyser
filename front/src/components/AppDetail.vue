<script setup lang="ts">
import { ref, onUpdated, onMounted } from 'vue'

const props = defineProps({
	appId: String
})
const loadDetail = ref(true)
const app = ref({
	title: ''
})
const loadScrapping = ref()

const fetchAppDetail = async (id: string) => {
	const params: { [k: string]: any } = {}
	params.id = id
	const query = new URLSearchParams(params)
	const res = await fetch(`http://localhost:5173/api/appDetail?${query}`, {
		method: 'GET',
	})
	return res.json()
}

const loadAppDetail = async () => {
	if (props.appId) {
		loadDetail.value = true
		const res = await fetchAppDetail(props.appId)
		console.log(res)
		loadDetail.value = false
	}
}

onMounted(loadAppDetail)
onUpdated(loadAppDetail)


const scrapApp = async () => {
	// TODO: call server to begin the scrapping
	console.log(loadDetail.value)
}
</script>

<template>
	<v-card :title="app.title">
		<v-container fluid class="input-analiser">
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
.input-analiser {
	min-height: 120px;
}
</style>