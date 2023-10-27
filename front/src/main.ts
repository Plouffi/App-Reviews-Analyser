import App from './App.vue'
import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import 'vuetify/styles'
import './assets'
import '@mdi/font/css/materialdesignicons.css'

/* 
 * Main file, initialise vuetify dependance and vue app
 */
const vuetify = createVuetify({
	icons: {
		defaultSet: 'mdi',
		aliases,
		sets: {
			mdi,
		},
	},
})
const app = createApp(App)
app.use(vuetify)
app.mount('#app')
