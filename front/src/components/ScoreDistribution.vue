<script setup lang="ts">
import { ref } from 'vue'
import Utils from '@/utils';

const date = ref() // Model value for the date parameter
const scoreDistribution = ref("") // Model value for the source url result

/**
 * Fetch the score distribution graph from the backend API
 *
 * @returns The promise from the fetch API containing the score distribution graph.
 * If it fails, return a promise with mocked data.
 */
async function fecthScoreDistribution(): Promise<any> {
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

/**
 * Trigger the backend process to compute score distribution
 */
const computeScoreDistribution = async () => {
	const image = await fecthScoreDistribution()
	try {
		scoreDistribution.value = URL.createObjectURL(image)
	} catch (e) {
		scoreDistribution.value = image
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
			<v-btn @click="computeScoreDistribution()" color="teal-darken-2" variant="flat" elevation="4">Compute</v-btn>
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
