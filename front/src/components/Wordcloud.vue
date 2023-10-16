<script setup lang="ts">
import { ref } from 'vue'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

//Request parameter for /wordcloud
const alpha = ref()
const nToken = ref()
const lang = ref()
const score = ref()
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
    const params: {[k: string]: any} = {}
    params.alpha = alpha.value
    params.n = nToken.value
    params.lang = lang.value
    if (!isNaN(score.value)) {
        params.score = score.value
    }
    params.start1 = start1.value.toLocaleString()
    params.end1 = end1.value.toLocaleString()
    params.start2 = start2.value.toLocaleString()
    params.end2 = end2.value.toLocaleString()
    const query = new URLSearchParams(params)
    const res = await fetch(`http://localhost:5173/api/wordcloud/computeWords?${query}`)
    return res.json()
}

async function fetchImageWordcloud(words: [[string, Float32Array]]) {
  const res = await fetch(`http://localhost:5173/api/wordcloud/generateImage`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({'words': words})
  })
  return res.blob()
}

const computeWordcloud = async () => {
  const wordsRes = await fecthWords()
  console.log(wordsRes)
  const image1 = await fetchImageWordcloud(wordsRes[0])
  wordcloudImage1.value = URL.createObjectURL(image1)
  const image2 = await fetchImageWordcloud(wordsRes[1])
  wordcloudImage2.value = URL.createObjectURL(image2)
}
</script>

<template>
  <div class="row">
    <h3>
        Wordcloud
    </h3>
    <div class="input-analyzer mb-3 row">
        <div class="col">
            <label for="alpha" class="form-label">Alpha</label>
            <input v-model.number="alpha" min="0" class="form-control" name="alpha" aria-describedby="alphaHelp" placeholder="Alpha..."/> 
            <small id="alphaHelp" class="form-text text-muted">Parameters to reduce noises in data</small>
        </div>
        <div class="col">
            <label for="nToken" class="form-label">nToken</label>
            <input v-model.number="nToken" min="1" class="form-control" name="nToken" aria-describedby="nTokenHelp" placeholder="Number of word per token..."/> 
            <small id="nTokenHelp" class="form-text text-muted">Define the number of word per token vocabulary</small>
        </div>
        <div class="col">
            <label for="lang" class="form-label">Language</label>
            <select v-model="lang" class="form-control" name="lang" aria-describedby="langHelp" placeholder="Reviews language...">
                <option disabled value="">Reviews language...</option>
                <option v-for="language in languages" :value="language.value">
                    {{ language.text }}
                  </option>
            </select> 
            <small id="langHelp" class="form-text text-muted">Reviews and vocabulary language</small>
        </div>
        <div class="col">
            <label for="score" class="form-label">Score</label>
            <input v-model.number="score" min="0" max="5" step="1" class="form-control" name="score" aria-describedby="scoreHelp" placeholder="Reviews score targeted..."/> 
            <small id="scoreHelp" class="form-text text-muted">Filter reviews on score (take all if empty or 0)</small>
        </div>
    </div>
    <div class="input-analyzer mb-3 row">
        <div class="col">
			<label for="start1" class="form-label">Start date 1</label>
			<VueDatePicker v-model="start1" class="form-control" name="start1" aria-describedby="start1Help" placeholder="Start date..."></VueDatePicker>
			<small id="start1Help" class="form-text text-muted">First period start date to compare</small>
		</div>
        <div class="col">
			<label for="end1" class="form-label">End date 1</label>
			<VueDatePicker v-model="end1" class="form-control" name="end1" aria-describedby="end1Help" placeholder="End date..."></VueDatePicker>
			<small id="end1Help" class="form-text text-muted">First period end date to compare</small>
		</div>
        <div class="col">
			<label for="start2" class="form-label">Start date 2</label>
			<VueDatePicker v-model="start2" class="form-control" name="start2" aria-describedby="start2Help" placeholder="Start date..."></VueDatePicker>
			<small id="start2Help" class="form-text text-muted">Second period start date to compare</small>
		</div>
        <div class="col">
			<label for="end2" class="form-label">End date 2</label>
			<VueDatePicker v-model="end2" class="form-control" name="end2" aria-describedby="end2Help" placeholder="End date..."></VueDatePicker>
			<small id="end2Help" class="form-text text-muted">Second period end date to compare</small>
		</div>
    </div>
    <div class="mb-3">
        <button @click="computeWordcloud()" class="btn btn-primary">Compute</button>
    </div>
    <div class="mb-3">
      <h3>First period</h3>
      <picture v-if="wordcloudImage1">
				<source :srcset="wordcloudImage1" type="image/png">
				<img :src="wordcloudImage1" class="img-fluid" alt="First period wordcloud">
			</picture>
      <h3>Second period</h3>
      <picture v-if="wordcloudImage2">
				<source :srcset="wordcloudImage2" type="image/png">
				<img :src="wordcloudImage2" class="img-fluid" alt="Second period wordcloud">
			</picture>
    </div>
  </div>
</template>

<style scoped>
.input-analyzer {
  min-height: 120px;
}
</style>
