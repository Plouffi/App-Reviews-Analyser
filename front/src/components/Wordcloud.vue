<script setup lang="ts">
import { ref } from 'vue'

// Input rules
const alphaRule = ref((alpha: number)  => {
	return alpha >= 0 || "Must be positive or zero"
})

const tokenRule = ref((token: number)  => {
	return token > 0 || "Must be strictly positive"
})

const languageRule = ref((lang: string) => {
	return !!lang || 'Language is required'
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
const wordcloudImage1 = ref("")
const wordcloudImage2 = ref("")


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

async function fecthWords() {
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
	return res.json()
}

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

const computeWordcloud = async () => {
	const wordsRes = await fecthWords()
	const image1 = await fetchImageWordcloud(wordsRes[0])
	wordcloudImage1.value = URL.createObjectURL(image1)
	const image2 = await fetchImageWordcloud(wordsRes[1])
	wordcloudImage2.value = URL.createObjectURL(image2)
}
</script>

<template>
	<v-card title="Wordcloud">
		<v-container fluid>
			<v-row class="input-analiser">
				<v-col cols="3">
					<v-text-field v-model="alpha"
						label="Alpha"
						type="number"
						:rules="[alphaRule]"
						variant="underlined"
						hint="Parameters to reduce noises in data">
					</v-text-field>
				</v-col>
				<v-col cols="3">
					<v-text-field v-model="nToken"
						label="nToken"
						type="number"
						:rules="[tokenRule]"
						variant="underlined"
						hint="Define the number of word per token vocabulary">
					</v-text-field>
				</v-col>
				<v-col cols="3">
					<v-select v-model="lang"
						:items="languages"
						label="Language"
						item-title="text"
						item-value="value"
						variant="underlined"
						persistent-hint
						return-object
						single-line
						hint="Reviews and vocabulary language">
					</v-select>
				</v-col>
				<v-col cols="3">
					<v-slider v-model="score"
						:ticks="[0,1,2,3,4,5]"
						:min="0"
						:max="5"
						step="1"
						label="Score"
						thumb-label="always"
						:show-ticks="false"
						color="light-blue-darken-2"
						hint="Filter reviews on score (take all reviews if 0)">
					</v-slider>
				</v-col>
			</v-row>

			<v-row class="input-analiser">
				<v-col cols="3">
					<v-text-field v-model="start1" 
						label="Start date 1" 
						type="datetime-local" 
						variant="underlined"
						hint="First period start date to compare">
					</v-text-field>
				</v-col>
				<v-col cols="3">
					<v-text-field v-model="end1" 
						label="End date 1" 
						type="datetime-local" 
						variant="underlined"
						hint="First period end date to compare">
					</v-text-field>
				</v-col>
				<v-col cols="3">
					<v-text-field v-model="start2" 
						label="Start date 2" 
						type="datetime-local" 
						variant="underlined"
						hint="Second period start date to compare">
					</v-text-field>
				</v-col>
				<v-col cols="3">
					<v-text-field v-model="end2" 
						label="End date 2" 
						type="datetime-local" 
						variant="underlined"
						hint="Second period end date to compare">
					</v-text-field>
				</v-col>
			</v-row>
		</v-container>
		<v-card-actions>
			<v-btn @click="computeWordcloud()" color="light-blue-darken-2" variant="flat" elevation="4">Compute</v-btn>
		</v-card-actions>
		<v-container fluid>
			<v-row dense>
				<v-col cols="6">
					<v-card title="First Period">
						<picture v-if="wordcloudImage1">
							<source :srcset="wordcloudImage1" type="image/png">
							<img :src="wordcloudImage1" class="img-fluid" alt="First period wordcloud">
						</picture>
					</v-card>
				</v-col>
				<v-col cols="6">
					<v-card title="Second Period">
						<picture v-if="wordcloudImage2">
							<source :srcset="wordcloudImage2" type="image/png">
							<img :src="wordcloudImage2" class="img-fluid" alt="Second period wordcloud">
						</picture>
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
