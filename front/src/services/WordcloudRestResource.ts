import ServiceRestResource from './ServiceRestResource'

export default class WordcloudRestResource extends ServiceRestResource  {

	readonly _BASE_API = '/wordcloud'

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
		const endpoint = `${this._BASE_API}/words`
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
		const endpoint = `${this._BASE_API}/image`
		try {
			const res = await fetch(this.buildURL(endpoint), {
				method: 'POST',
				headers: this._HEADERS,
				body: JSON.stringify({ 'words': words })
			})
			if (!res.ok) throw `${res.statusText} - ${res.status}`
			return res.blob()
		} catch (err) {
			throw this.handleError(endpoint, err)
		}
	}
}