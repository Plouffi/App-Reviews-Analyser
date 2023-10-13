<script setup lang="ts">
import { ref } from 'vue'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

//Request parameter for /means
const timeDelta = ref()
const ignore = ref()
const means = ref("")

async function fecthMeans() {
    const params: {[k: string]: any} = {}
    if (!isNaN(timeDelta.value)) {
        params.timeDelta = timeDelta.value
    }
    if (!isNaN(ignore.value)) {
        params.ignore = ignore.value
    }
    const query = new URLSearchParams(params)
    const res = await fetch(`http://localhost:5173/api/compute/means?${query}`)
    return res.blob()
}

const computeMeans = async () => {
  const image = await fecthMeans()
  means.value = URL.createObjectURL(image)
}
</script>

<template>
  <div class="row">
		<h3>
			Means
		</h3>
		<div class="input-analyzer mb-3 row">
			<div class="col">
				<label for="timeDelta" class="form-label">Time delta</label>
				<input v-model.number="timeDelta" min="0" class="form-control" name="timeDelta" aria-describedby="timeDeltaHelp" placeholder="Time Delta..."/> 
				<small id="timeDeltaHelp" class="form-text text-muted">Define the duration on which it computes cumulative results (default = 30)</small>
			</div>
			<div class="col">
				<label for="ignore" class="form-label">Ignore</label>
				<input v-model.number="ignore" min="0" class="form-control" name="ignore" aria-describedby="ignoreHelp" placeholder="Reviews ignored..."/> 
				<small id="ignoreHelp" class="form-text text-muted">Indicates the number of first reviews to skip (default = 0)</small>
			</div>
		</div>
		<div class="mb-3">
			<button @click="computeMeans()" class="btn btn-primary">Compute</button>
		</div>
		<div class="mb-3">
			<picture v-if="means">
				<source :srcset="means" type="image/png">
				<img :src="means" class="img-fluid" alt="Result of score Distribution">
			</picture>
		</div>
  </div>
</template>

<style scoped>
.input-analyzer {
  min-height: 120px;
}
</style>
