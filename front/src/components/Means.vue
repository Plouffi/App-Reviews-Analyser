<script setup lang="ts">
import { ref } from 'vue'
import araError from './Error.vue'
import Utils from '@/utils'

const ENV = import.meta.env // Environment variable

// Input rules
const timeDeltaRule = ref((timeDelta: number) => {
	return (timeDelta > 0 && timeDelta <= 365) || "Must be between 1 and 365"
})
const maxDelta = 365 // one year
const timeDeltaTicks = ref(Array.from(Array(maxDelta).keys()).map(x => x++))

const timeDelta = ref(30) // Model value for the time delta parameter
const ignore = ref(0) // Model value for the ignore parameter
const means = ref('') // Model value for the source url result
const meansLoading = ref(false) // Loading flag on means computing
const meansError = ref('') // Error flag on means computing

/**
 * Fetch the means graph from the backend API
 *
 * @returns The promise from the fetch API containing the means graph.
 * If it fails, return a promise with mocked data.
 */
async function fecthMeans(): Promise<any> {
	try {
		const params: { [k: string]: any } = {}
		if (!isNaN(timeDelta.value)) {
			params.timeDelta = timeDelta.value
		}
		if (!isNaN(ignore.value)) {
			params.ignore = ignore.value
		}
		const query = new URLSearchParams(params)
		const res = await fetch('http://localhost:5173/api/compute/means', {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(params)
		})
		if (!res.ok) throw `${res.statusText} - ${res.status}`
		return res.blob()
	} catch (e) {
		let msg = `Error while requesting /compute/means : ${e}`
		console.error(msg)
		throw msg
	}
}

/**
 * Trigger the backend process to compute means
 */
const computeMeans = async () => {
	meansLoading.value = true
	try {
		const image = await fecthMeans()
		means.value = URL.createObjectURL(image)
		meansError.value = ''
	} catch (e) {
		if (ENV.VITE_IS_MOCK) {
			means.value = Utils.getMockImage('means')
		} else {
			meansError.value = `${e}`
		}
	}
	meansLoading.value = false
}
</script>

<template>
	<v-card title="Means">
		<v-container fluid class="input-analiser">
			<v-row>
				<v-col cols="12">
					<v-slider v-model="timeDelta" :ticks="timeDeltaTicks" :min="1" :max="maxDelta" step="1" label="Delta"
						thumb-color="teal-darken-2" color="teal-darken-2" :show-ticks="false"
						hint="Define the duration in days on which it computes cumulative results">
						<template v-slot:append>
							<v-text-field v-model="timeDelta" type="number" :rules="[timeDeltaRule]" density="compact"
								variant="underlined" class="timeDeltaInput" hide-details></v-text-field>
						</template>
					</v-slider>
				</v-col>
			</v-row>
		</v-container>
		<v-card-actions>
			<v-btn @click="computeMeans()" color="teal-darken-2" variant="flat" elevation="4">Compute</v-btn>
		</v-card-actions>
		<v-container>
			<v-expand-transition>
				<picture v-if="means">
					<source :srcset="means" type="image/png">
					<v-img :src="means" alt="Result of score Distribution"></v-img>
				</picture>
				<ara-error :msg="meansError" v-if="meansError.length"></ara-error>
			</v-expand-transition>
			<v-overlay v-model="meansLoading" contained class="align-center justify-center">
				<v-progress-circular :size="60" :witdh="60" color="teal-darken-2" indeterminate />
			</v-overlay>
		</v-container>
	</v-card>
</template>

<style scoped>
.input-analiser {
	min-height: 120px;
}

.timeDeltaInput {
	width: 50px
}
</style>