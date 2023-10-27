<script setup lang="ts">
defineOptions({
  name: 'ara-error'
})
const props = defineProps({
	msg: String //Error message
})
</script>

<template>
	<v-card class="ara-alert d-flex justify-center align-center pa-2" variant="flat" color="red-lighten-2">
		<v-icon icon="mdi-alert" size="large"></v-icon>
		<v-card-text>{{ msg }}</v-card-text>
	</v-card>
</template>

<style scoped>
.ara-alert>.v-card-text {
	font-weight: bold;
}
</style>