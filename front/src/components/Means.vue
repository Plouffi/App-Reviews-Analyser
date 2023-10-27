<script setup lang="ts">
import { ref } from 'vue'
import Utils from '@/utils';

// Input rules
const timeDeltaRule = ref((timeDelta: number) => {
	return (timeDelta > 0 && timeDelta <= 365) || "Must be between 1 and 365"
})
const maxDelta = 365 // one year
const timeDeltaTicks = ref(Array.from(Array(maxDelta).keys()).map(x => x++))

const timeDelta = ref(30) // Model value for the time delta parameter
const ignore = ref(0) // Model value for the ignore parameter
const means = ref("") // Model value for the the source url result

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
		if (!res.ok) throw res.statusText
		return res.blob()
	} catch (e) {
		console.error(`Error while requesting /compute/means :${e}`)
		return new Promise<any>(function (resolve) {
			resolve(Utils.getMockImage('means'))
		})
	}
}

/**
 * Trigger the backend process to compute means
 */
const computeMeans = async () => {
	const image = await fecthMeans()
	try {
		means.value = URL.createObjectURL(image)
	} catch (e) {
		means.value = image
	}
}
</script>

<template>
	<v-card title="Means">
		<v-container fluid class="input-analiser">
			<v-row>
				<v-col cols="12">
					<v-slider v-model="timeDelta" :ticks="timeDeltaTicks" :min="1" :max="maxDelta" step="1" label="Delta"
						thumb-color="light-blue-darken-2" color="light-blue-darken-2" :show-ticks="false"
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
			<v-btn @click="computeMeans()" color="light-blue-darken-2" variant="flat" elevation="4">Compute</v-btn>
		</v-card-actions>
		<v-container>
			<picture v-if="means">
				<source :srcset="means" type="image/png">
				<v-img :src="means" alt="Result of score Distribution"></v-img>
			</picture>
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