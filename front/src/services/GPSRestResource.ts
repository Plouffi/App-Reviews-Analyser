import { GpsApp } from '@/gpsApp';
import Utils from '@/utils';

export default class GPSRestResource {

	readonly _BASE_URL = import.meta.env.VITE_BASE_URL
	readonly _HEADERS = {
		'Accept': 'application/json',
		'Content-Type': 'application/json'
	}

	/**
	 * Fetch the search result from the backend API
	 *
	 * @param searchTerm Search terms
	 * 
	 * @returns The promise from the fetch API containing search result.
	 * If it fails, return a promise with mocked data.
	 */
	async searchApp(searchTerm: string): Promise<[{ [k: string]: any }]> {
		const endpoint = '/searchApp'
		try {
			const params: { [k: string]: any } = {}
			if (searchTerm.length) {
				params.search = searchTerm
				const query = new URLSearchParams(params)
				const res = await fetch(`${this.buildURL(endpoint)}?${query}`, {
					method: 'GET'
				})
				if (!res.ok) throw `${res.statusText} - ${res.status}`
				return res.json()
			}
			throw 'Error params'
		} catch (err) {
			throw this.handleError(endpoint, err)
		}
	}

	/**
	 * Fetch the detail app from the backend API
	 *
	 * @param appId the app ID 
	 * 
	 * @returns The promise from the fetch API containing the app detail.
	 * If it fails, return a promise with mocked data.
	 */
	async getAppDetail(appId: string): Promise<GpsApp> {
		const endpoint = '/appDetail'
		try {
			const params: { [k: string]: any } = {}
			params.id = appId
			const query = new URLSearchParams(params)
			const res = await fetch(`${this.buildURL(endpoint)}?${query}`, {
				method: 'GET',
			})
			if (!res.ok) throw `${res.statusText} - ${res.status}`
			return res.json()
		} catch (err) {
			throw this.handleError(endpoint, err)
		}
	}

	/**
	 * Fetch the score distribution graph from the backend API
	 *
	 * @param date the date to separate the 2 period to compare
	 * 
	 * @returns The promise from the fetch API containing the score distribution graph.
	 * If it fails, return a promise with mocked data.
	 */
	async getScoreDistribution(date: Date): Promise<any> {
		const endpoint = '/compute/scoreDistribution'
		try {
			const res = await fetch(this.buildURL(endpoint), {
				method: 'POST',
				headers: this._HEADERS,
				body: JSON.stringify(date ? { 'date': date.toLocaleString() } : {})
			})
			if (!res.ok) throw `${res.statusText} - ${res.status}`
			return res.blob()
		} catch (err) {
			throw this.handleError(endpoint, err)
		}
	}

	/**
	 * Fetch the means graph from the backend API
	 *
	 * @param timeDelta Define the duration in days on which it computes cumulatives results
	 * @param ignore The number of first reviews to ignore
	 * 
	 * @returns The promise from the fetch API containing the means graph.
	 * If it fails, return a promise with mocked data.
	 */
	async getMeans(timeDelta: number, ignore: number): Promise<any> {
		const endpoint = '/compute/means'
		try {
			const params: { [k: string]: any } = {}
			if (!isNaN(timeDelta)) {
				params.timeDelta = timeDelta
			}
			if (!isNaN(ignore)) {
				params.ignore = ignore
			}
			const res = await fetch(this.buildURL(endpoint), {
				method: 'POST',
				headers: this._HEADERS,
				body: JSON.stringify(params)
			})
			if (!res.ok) throw `${res.statusText} - ${res.status}`
			return res.blob()
		} catch (err) {
			throw this.handleError(endpoint, err)
		}
	}

	/**
	 * Fetch the words and their frequencies from the backend API
	 *
	 * @param alpha Reduces noises in data
	 * @param nToken Define the number of word per token vocabulary
	 * @param lang Reviews and vocabulary language
	 * @param score Filter reviews on score (take all if 0)
	 * @param start1 First periode start date to compare
	 * @param end1 First periode end date to compare
	 * @param start2 Second periode start date to compare
	 * @param end2 Second periode end date to compare
	 * 
	 * @returns The promise from the fetch API containing the words and their frequencies.
	 */
	async getWords(alpha: number, nToken: number, lang: string, score: number, start1: Date, end1: Date, start2: Date, end2: Date): Promise<any> {
		const endpoint = '/wordcloud/computeWords'
		try {
			const params: { [k: string]: any } = {}
			params.alpha = alpha
			params.n = nToken
			params.lang = lang
			if (!isNaN(score)) {
				params.score = score
			}
			params.start1 = start1.toLocaleString()
			params.end1 = end1.toLocaleString()
			params.start2 = start2.toLocaleString()
			params.end2 = end2.toLocaleString()
			const res = await fetch(this.buildURL(endpoint), {
				method: 'POST',
				headers: this._HEADERS,
				body: JSON.stringify(params)
			})
			if (!res.ok) throw `${res.statusText} - ${res.status}`
			return res.json()
		} catch (err) {
			throw this.handleError(endpoint, err)
		}
	}

	/**
	 * Fetch the wordcloud image from the backend API
	 *
	 * @param words the words and their frequencies
	 * 
	 * @returns The promise from the fetch API containing the wordcloud image.
	 * If it fails, return a promise with mocked data.
	 */
	async getImageWordcloud(words: [[string, Float32Array]]) {
		const endpoint = '/wordcloud/generateImage'
		const res = await fetch(this.buildURL(endpoint), {
			method: 'POST',
			headers: this._HEADERS,
			body: JSON.stringify({ 'words': words })
		})
		return res.blob()
	}

	/**
	 * Build the URL request
	 *
	 * @param endpoint the requested endpoint
	 * 
	 * @returns the url
	 */
	private buildURL(endpoint: string): string {
		return `${this._BASE_URL}/api${endpoint}`
	}

	/**
	 * Log and send the error message
	 *
	 * @param endpoint the requested endpoint
	 * @param err the error
	 * 
	 * @returns A error message 
	 */
	private handleError(endpoint: string, err: unknown): string {
		const msg = `Error while requesting ${endpoint} : ${err}`
		console.error(msg)
		return msg
	}
}