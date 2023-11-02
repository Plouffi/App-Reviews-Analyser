<script setup lang="ts">
import { ref } from 'vue'
import araError from './Error.vue'
import GPSRestResource from '@/services/GPSRestResource';
import Utils from '@/utils';

const ENV = import.meta.env // Environment variable

const gpsResource = new GPSRestResource()
const date = ref() // Model value for the date parameter
const scoreDistribution = ref('') // Model value for the source url result
const scoreDistributionLoading = ref(false) // Loading flag on score distribution computing
const scoreDistributionError = ref('') // Error flag on score distribution computing

/**
 * Trigger the backend process to compute score distribution
 */
const computeScoreDistribution = async () => {
	scoreDistributionLoading.value = true
	try {
		const image = await gpsResource.getScoreDistribution(date.value)
		scoreDistribution.value = URL.createObjectURL(image)
	} catch (e) {
		if (ENV.MODE == Utils._MODE_MOCK) {
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
