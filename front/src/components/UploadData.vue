<script setup lang="ts">
import { ref } from 'vue'

// Input rules
const fileRule = ref((file: any) => {
	return !!file || "Cannot be empty"
})

// Request parameter for /means
const hash = ref()
const file = ref()

async function uploadFile() {
    console.log(file.value)
    let data = {}
	const res = await fetch('http://localhost:5173/api/uploadData', {
		method: 'POST',
		headers: {
			'Accept': 'multipart/form-data',
			'Content-Type': 'multipart/form-data'
		},
		body: JSON.stringify(data)
	})
	return res.text()
}

const upload = async () => {
	const hashFilename = await uploadFile()
	hash.value = hashFilename
}
</script>

<template>
	<v-card title="Load data">
		<v-container fluid  class="input-analiser">
			<v-row>
				<v-col cols="12">
					<v-file-input v-model="file" label="File data" accept="file/csv" variant="underlined"></v-file-input>
				</v-col>
			</v-row>
		</v-container>
		<v-card-actions class="mb-3">
			<v-btn @click="upload()" color="light-blue-darken-2" variant="flat" elevation="4">Upload</v-btn>
		</v-card-actions>
	</v-card>
</template>

<style scoped>
.input-analiser {
  min-height: 120px;
}
</style>