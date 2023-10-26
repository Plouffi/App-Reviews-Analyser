<script setup lang="ts">
import { ref } from 'vue'
import Utils from '@/utils';

//Request parameter for /scoreDistribution
const date = ref()
const scoreDistribution = ref("")

async function fecthScoreDistribution() {
	try {
		const res = await fetch('http://localhost:5173/api/compute/scoreDistribution', {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(date.value ? { 'date': date.value.toLocaleString() } : {})
		})
		if (!res.ok) throw res.statusText
		return res.blob()
	} catch (e) {
		console.error(`Error while requesting /compute/scoreDistribution :${e}`)
		return new Promise<any>(function (resolve) {
			resolve(Utils.getMockImage('score_distribution'))
		})
	}
}

const computeScoreDistribution = async () => {
	const image = await fecthScoreDistribution()
	try {
		scoreDistribution.value = URL.createObjectURL(image)
	} catch (e) {
		scoreDistribution.value = new URL(image, import.meta.url).toString()
	}
}
</script>

<template>
	<v-card title="Score Distribution">
		<v-container fluid class="input-analyser">
			<v-row>
				<v-col cols="12">
					<v-text-field v-model="date" label="Date" type="datetime-local" variant="underlined"
						hint="Date to compare score distribution (if empty, no comparaison)">
					</v-text-field>
				</v-col>
			</v-row>
		</v-container>
		<v-card-actions>
			<v-btn @click="computeScoreDistribution()" color="light-blue-darken-2" variant="flat" elevation="4">Compute</v-btn>
		</v-card-actions>
		<v-container>
			<picture v-if="scoreDistribution.length">
				<source :srcset="scoreDistribution" type="image/png">
				<v-img :src="scoreDistribution" alt="Result of score Distribution"></v-img>
			</picture>
		</v-container>
	</v-card>
</template>

<style scoped>
.input-analyser {
	min-height: 120px;
}
</style>
