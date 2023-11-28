<script setup lang="ts">
import { ref } from 'vue'
import { useLocale } from 'vuetify'
import araError from './Error.vue'
import AnalyserRestResource from '@/services/AnalyserRestResource'
import Utils from '@/utils'

const ENV = import.meta.env // Environment variable
const { t } = useLocale()

const analyserResource = new AnalyserRestResource()
const timeDelta = ref(30) // Model value for the time delta parameter
const ignore = ref(0) // Model value for the ignore parameter
const means = ref('') // Model value for the source url result
const meansLoading = ref(false) // Loading flag on means computing
const meansError = ref('') // Error flag on means computing

// Input rules
const timeDeltaRule = ref((timeDelta: number) => {
	return (timeDelta > 0 && timeDelta <= 365) || t('analyser.means.rule')
})
const maxDelta = 365 // one year
const timeDeltaTicks = ref(Array.from(Array(maxDelta).keys()).map(x => x++))

/**
 * Trigger the backend process to compute means
 */
const computeMeans = async () => {
	meansLoading.value = true
	try {
		const image = await analyserResource.getMeans(timeDelta.value, ignore.value)
		means.value = URL.createObjectURL(image)
		meansError.value = ''
	} catch (err) {
		if (ENV.MODE == Utils._MODE_MOCK) {
			means.value = Utils.getMockImage('means')
		} else {
			meansError.value = `${err}`
		}
	}
	meansLoading.value = false
}
</script>

<template>
	<v-card :title="$t('analyser.means.title')">
		<v-container fluid class="input-analiser">
			<v-row>
				<v-col cols="12">
					<v-slider v-model="timeDelta" :ticks="timeDeltaTicks" :min="1" :max="maxDelta" step="1" :label="$t('analyser.means.label')"
						thumb-color="teal-darken-2" color="teal-darken-2" :show-ticks="false"
						:hint="$t('analyser.means.tooltip')">
						<template v-slot:append>
							<v-text-field v-model="timeDelta" type="number" :rules="[timeDeltaRule]" density="compact"
								variant="underlined" class="timeDeltaInput" hide-details></v-text-field>
						</template>
					</v-slider>
				</v-col>
			</v-row>
		</v-container>
		<v-card-actions>
			<v-btn @click="computeMeans()" color="teal-darken-2" variant="flat" elevation="4">{{ $t('analyser.means.button') }}</v-btn>
		</v-card-actions>
		<v-container>
			<v-expand-transition>
				<picture v-if="means">
					<source :srcset="means" type="image/png">
					<v-img :src="means" :alt="$t('analyser.means.result.alt')"></v-img>
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