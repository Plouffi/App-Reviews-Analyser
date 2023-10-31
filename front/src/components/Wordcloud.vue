<script setup lang="ts">
import { ref } from 'vue'
import { useLocale } from 'vuetify';
import araError from './Error.vue'
import Utils from '@/utils';

const ENV = import.meta.env // Environment variable
const { t } = useLocale()

// Input rules
const alphaRule = ref((alpha: number) => {
	return alpha >= 0 || t('analyser.wordcloud.alpha.rule')
})

const tokenRule = ref((token: number) => {
	return token > 0 || t('analyser.wordcloud.ntoken.rule')
})

const languageRule = ref((lang: string) => {
	return !!lang || t('analyser.wordcloud.language.rule')
})

// Request parameter for /wordcloud
const alpha = ref()
const nToken = ref()
const lang = ref()
const score = ref(0)
const start1 = ref()
const end1 = ref()
const start2 = ref()
const end2 = ref()
const wordcloudImage1 = ref('')
const wordcloudImage2 = ref('')
const wordcloud1Loading = ref(false) // Loading flag for the first wordcloud
const wordcloud2Loading = ref(false) // Loading flag for the second wordcloud
const wordcloudError = ref('') // Error flag


const languages = ref([
	{ text: 'Chinese', value: 'zh' },
	{ text: 'Deutsh', value: 'de' },
	{ text: 'English', value: 'en' },
	{ text: 'French', value: 'fr' },
	{ text: 'Italian', value: 'it' },
	{ text: 'Japan', value: 'jp' },
	{ text: 'Portuguese', value: 'pt' },
	{ text: 'Spanish', value: 'es' }
])

/**
 * Fetch the words and their frequencies from the backend API
 *
 * @returns The promise from the fetch API containing the words and their frequencies.
 */
async function fecthWords(): Promise<any> {
	try {
		const params: { [k: string]: any } = {}
		params.alpha = alpha.value
		params.n = nToken.value
		params.lang = lang.value.value
		if (!isNaN(score.value)) {
			params.score = score.value
		}
		params.start1 = start1.value.toLocaleString()
		params.end1 = end1.value.toLocaleString()
		params.start2 = start2.value.toLocaleString()
		params.end2 = end2.value.toLocaleString()
		const res = await fetch('http://localhost:5173/api/wordcloud/computeWords', {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(params)
		})
		if (!res.ok) throw `${res.statusText} - ${res.status}`
		return res.json()
	} catch (e) {
		let msg = `Error while requesting /wordcloud/computeWords : ${e}`
		console.error(msg)
		throw msg
	}
}

/**
 * Fetch the wordcloud image from the backend API
 *
 * @param words the words and their frequencies
 * 
 * @returns The promise from the fetch API containing the wordcloud image.
 * If it fails, return a promise with mocked data.
 */
async function fetchImageWordcloud(words: [[string, Float32Array]]) {
	const res = await fetch('http://localhost:5173/api/wordcloud/generateImage', {
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ 'words': words })
	})
	return res.blob()
}

/**
 * Trigger the backend process wordcloud
 */
const computeWordcloud = async () => {
	wordcloud1Loading.value = true;
	wordcloud2Loading.value = true;
	try {
		const wordsRes = await fecthWords()
		const image1 = await fetchImageWordcloud(wordsRes[0])
		wordcloudImage1.value = URL.createObjectURL(image1)
		const image2 = await fetchImageWordcloud(wordsRes[1])
		wordcloudImage2.value = URL.createObjectURL(image2)
		wordcloudError.value = ''
	} catch (e) {
		if (ENV.VITE_IS_MOCK) {
			wordcloudImage1.value = Utils.getMockImage('wordcloud_1')
			wordcloudImage2.value = Utils.getMockImage('wordcloud_2')
		} else {
			wordcloudError.value = `${e}`
		}
	}
	wordcloud1Loading.value = false;
	wordcloud2Loading.value = false;
}
</script>

<template>
	<v-card :title="$t('analyser.wordcloud.title')">
		<v-container fluid>
			<v-row class="input-analiser">
				<v-col cols="12" sm="6" md="3">
					<v-text-field v-model="alpha" :label="$t('analyser.wordcloud.alpha.label')" type="number" :rules="[alphaRule]"
						variant="underlined" :hint="$t('analyser.wordcloud.alpha.tooltip')">
					</v-text-field>
				</v-col>
				<v-col cols="12" sm="6" md="3">
					<v-text-field v-model="nToken" :label="$t('analyser.wordcloud.ntoken.label')" type="number" :rules="[tokenRule]"
						variant="underlined" :hint="$t('analyser.wordcloud.ntoken.tooltip')">
					</v-text-field>
				</v-col>
				<v-col cols="12" sm="6" md="3">
					<v-select v-model="lang" :items="languages" :label="$t('analyser.wordcloud.language.label')" item-title="text"
						item-value="value" variant="underlined" persistent-hint return-object single-line
						:hint="$t('analyser.wordcloud.language.tooltip')">
					</v-select>
				</v-col>
				<v-col cols="12" sm="6" md="3">
					<v-slider v-model="score" :ticks="[0, 1, 2, 3, 4, 5]" :min="0" :max="5" step="1"
						:label="$t('analyser.wordcloud.score.label')" thumb-label="always" :show-ticks="false" color="teal-darken-2"
						:hint="$t('analyser.wordcloud.score.tooltip')">
					</v-slider>
				</v-col>
			</v-row>

			<v-row class="input-analiser">
				<v-col cols="12" sm="6" md="3">
					<v-text-field v-model="start1" :label="$t('analyser.wordcloud.start1.label')" type="datetime-local" variant="underlined"
						:hint="$t('analyser.wordcloud.end1.label')">
					</v-text-field>
				</v-col>
				<v-col cols="12" sm="6" md="3">
					<v-text-field v-model="end1" :label="$t('analyser.wordcloud.end1.label')" type="datetime-local" variant="underlined"
						:hint="$t('analyser.wordcloud.end1.tooltip')">
					</v-text-field>
				</v-col>
				<v-col cols="12" sm="6" md="3">
					<v-text-field v-model="start2" :label="$t('analyser.wordcloud.start2.label')" type="datetime-local" variant="underlined"
						:hint="$t('analyser.wordcloud.start2.tooltip')">
					</v-text-field>
				</v-col>
				<v-col cols="12" sm="6" md="3">
					<v-text-field v-model="end2" :label="$t('analyser.wordcloud.end2.label')" type="datetime-local" variant="underlined"
						:hint="$t('analyser.wordcloud.end2.tooltip')">
					</v-text-field>
				</v-col>
			</v-row>
		</v-container>
		<v-card-actions>
			<v-btn @click="computeWordcloud()" color="teal-darken-2" variant="flat" elevation="4">{{ $t('analyser.wordcloud.button') }}</v-btn>
		</v-card-actions>
		<v-container fluid>
			<v-row dense>
				<v-col cols="12" md="6">
					<v-card :title="$t('analyser.wordcloud.result.title1')">
						<v-expand-transition>
							<picture v-if="wordcloudImage1">
								<source :srcset="wordcloudImage1" type="image/png">
								<v-img :src="wordcloudImage1" class="img-fluid" :alt="$t('analyser.wordcloud.result.alt1')"></v-img>
							</picture>
							<ara-error :msg="wordcloudError" v-if="wordcloudError.length"></ara-error>
						</v-expand-transition>
						<v-overlay v-model="wordcloud1Loading" contained class="align-center justify-center">
							<v-progress-circular :size="30" :witdh="30" color="teal-darken-2" indeterminate />
						</v-overlay>
					</v-card>
				</v-col>
				<v-col cols="12" md="6">
					<v-card :title="$t('analyser.wordcloud.result.title2')">
						<v-expand-transition>
							<picture v-if="wordcloudImage2">
								<source :srcset="wordcloudImage2" type="image/png">
								<v-img :src="wordcloudImage2" class="img-fluid" :alt="$t('analyser.wordcloud.result.alt2')"></v-img>
							</picture>
							<ara-error :msg="wordcloudError" v-if="wordcloudError.length"></ara-error>
						</v-expand-transition>
						<v-overlay v-model="wordcloud2Loading" contained class="align-center justify-center">
							<v-progress-circular :size="60" :witdh="60" color="teal-darken-2" indeterminate />
						</v-overlay>
					</v-card>
				</v-col>
			</v-row>
		</v-container>
	</v-card>
</template>

<style scoped>
.input-analyzer {
	min-height: 120px;
}
</style>
