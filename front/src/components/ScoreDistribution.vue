<script setup lang="ts">
import { ref } from 'vue'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

//Request parameter for /scoreDistribution
const date = ref()
const scoreDistribution = ref("")

async function fecthScoreDistribution() {
	const query = date.value ? `?date=${date.value.toLocaleString()}` : ""
  const res = await fetch(`http://localhost:5173/api/compute/scoreDistribution${query}`)
  return res.blob()
}

const computeScoreDistribution = async () => {
  const image = await fecthScoreDistribution()
  scoreDistribution.value = URL.createObjectURL(image)
}
</script>

<template>
  <div class="row">
		<h3>
			Score Distribution
		</h3>
		<div class="input-analyzer mb-3">
			<label for="date" class="form-label">Date</label>
			<VueDatePicker v-model="date" class="form-control" name="date" aria-describedby="dateHelp" placeholder="Date..."></VueDatePicker>
			<small id="dateHelp" class="form-text text-muted">Date to compare score distribution (if empty, no comparaison)</small>
		</div>
		<div class="mb-3">
			<button @click="computeScoreDistribution()" class="btn btn-primary">Compute</button>
		</div>
		<div class="mb-3">
			<picture v-if="scoreDistribution.length">
				<source :srcset="scoreDistribution" type="image/png">
				<img :src="scoreDistribution" class="img-fluid" alt="Result of score Distribution">
			</picture>
		</div>
  </div>
</template>

<style scoped>
.input-analyzer {
  min-height: 120px;
}
</style>
