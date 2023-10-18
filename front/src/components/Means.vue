<script setup lang="ts">
import { ref } from 'vue'

// Input rules
const timeDeltaRule = ref((timeDelta: number) => {
	return (timeDelta > 0 && timeDelta <= 365) || "Must be between 1 and 365"
})

const maxDelta = 365 // one year
const timeDeltaTicks = ref(Array.from(Array(maxDelta).keys()).map(x => x++))

// Request parameter for /means
const timeDelta = ref(30)
const ignore = ref(0)
const means = ref("")

async function fecthMeans() {
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
	return res.blob()
}

const computeMeans = async () => {
	const image = await fecthMeans()
	means.value = URL.createObjectURL(image)
}
</script>

<template>
	<v-card title="Means">
		<v-container fluid  class="input-analiser">
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
		<div class="mb-3">
			<picture v-if="means">
				<source :srcset="means" type="image/png">
				<img :src="means" class="img-fluid" alt="Result of score Distribution">
			</picture>
		</div>
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