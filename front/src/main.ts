import App from './App.vue'
import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import { createVueI18nAdapter } from 'vuetify/locale/adapters/vue-i18n'
import { createI18n, useI18n } from 'vue-i18n'
import type { ThemeDefinition } from 'vuetify/dist/vuetify-labs.js'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import './assets/main.css'
import en from './locales/en.json'
import fr from './locales/fr.json'

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

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
	globalInjection: true,
  messages: {
		en,
		fr
	},
})

const vuetify = createVuetify({
	theme: {
		defaultTheme: 'myDarkTheme',
		themes: {
			myDarkTheme,
			myLightTheme
		}
	},
	locale: {
    adapter: createVueI18nAdapter({ i18n, useI18n }),
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
app.use(i18n)
app.mount('#app')
