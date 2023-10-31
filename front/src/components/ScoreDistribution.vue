<script setup lang="ts">
import { ref } from 'vue'
import araError from './Error.vue'
import Utils from '@/utils';

const ENV = import.meta.env // Environment variable

const date = ref() // Model value for the date parameter
const scoreDistribution = ref('') // Model value for the source url result
const scoreDistributionLoading = ref(false) // Loading flag on score distribution computing
const scoreDistributionError = ref('') // Error flag on score distribution computing

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
		if (!res.ok) throw `${res.statusText} - ${res.status}`
		return res.blob()
	} catch (e) {
		let msg = `Error while requesting /compute/scoreDistribution : ${e}`
		console.error(msg)
		throw msg
	}
}

/**
 * Trigger the backend process to compute score distribution
 */
const computeScoreDistribution = async () => {
	scoreDistributionLoading.value = true
	try {
		const image = await fecthScoreDistribution()
		scoreDistribution.value = URL.createObjectURL(image)
	} catch (e) {
		if (ENV.VITE_IS_MOCK) {
			scoreDistribution.value = Utils.getMockImage('score_distribution')
		} else {
			scoreDistributionError.value = `${e}`
		}
	}
	scoreDistributionLoading.value = false
}
</script>

<template>
	<v-card :title="$t('analyser.scoreDistribution.title')">
		<v-container fluid class="input-analyser">
			<v-row>
				<v-col cols="12">
					<v-text-field v-model="date" :label="$t('analyser.scoreDistribution.label')" type="datetime-local" variant="underlined"
						:hint="$t('analyser.scoreDistribution.tooltip')">
					</v-text-field>
				</v-col>
			</v-row>
		</v-container>
		<v-card-actions>
			<v-btn @click="computeScoreDistribution()" color="teal-darken-2" variant="flat" elevation="4">{{ $t('analyser.scoreDistribution.button') }}</v-btn>
		</v-card-actions>
		<v-container>
			<v-expand-transition>
				<picture v-if="scoreDistribution.length">
					<source :srcset="scoreDistribution" type="image/png">
					<v-img :src="scoreDistribution" :alt="$t('analyser.scoreDistribution.result.alt')"></v-img>
				</picture>
				<ara-error :msg="scoreDistributionError" v-if="scoreDistributionError.length"></ara-error>
			</v-expand-transition>
			<v-overlay v-model="scoreDistributionLoading" contained class="align-center justify-center">
				<v-progress-circular :size="60" :witdh="60" color="teal-darken-2" indeterminate />
			</v-overlay>
		</v-container>
	</v-card>
</template>

<style scoped>
.input-analyser {
	min-height: 120px;
}
</style>
