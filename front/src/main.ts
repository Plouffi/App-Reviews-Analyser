import App from './App.vue'
import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import type { ThemeDefinition } from 'vuetify/dist/vuetify-labs.js'
import 'vuetify/styles'
import './assets/main.css'
import '@mdi/font/css/materialdesignicons.css'

/* 
 * Main file, initialise vuetify dependance, vue app and themes
 */
const myDarkTheme: ThemeDefinition = {
	dark: true,
	colors: {
		'background': "#212121",
		'surface': "#424242",
		'header': "#424242"
	}
}

const myLightTheme: ThemeDefinition = {
	dark: false,
	colors: {
		'header': "#FFFFFF"
	}
}

const vuetify = createVuetify({
	theme: {
		defaultTheme: 'myDarkTheme',
		themes: {
			myDarkTheme,
			myLightTheme
		}
	},
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
