<script setup lang="ts">
import { ref } from 'vue'

const app = ref()
const apps = ref([]) //an app have: id, name, icon -> class ?

// TODO: onInitEvent -> loads all apps from server into the select


const selectApp = async () => {
	// TODO: Send value to parent component
	console.log(app.value)
}
</script>

<template>
	<v-card :title="$t('analyser.select.title')">
		<v-container fluid class="input-analiser">
			<v-row>
				<v-col cols="12">
					<v-select v-model="app" :items="apps" :label="$t('analyser.select.label')" item-title="nam" item-value="id" variant="underlined"
						persistent-hint return-object single-line :hint="$t('analyser.select.tooltip')">
					</v-select>
				</v-col>
			</v-row>
		</v-container>
		<v-card-actions class="mb-3">
			<v-btn @click="selectApp()" color="teal-darken-2" variant="flat" elevation="4">{{ $t('analyser.select.button') }}</v-btn>
		</v-card-actions>
	</v-card>
</template>

<style scoped>
.input-analiser {
	min-height: 120px;
}
</style>