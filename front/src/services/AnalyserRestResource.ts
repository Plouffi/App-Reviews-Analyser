import ServiceRestResource from './ServiceRestResource'

export default class AnalyserRestResource extends ServiceRestResource  {

	readonly _BASE_API = '/analyser'

	/**
	 * Fetch the score distribution graph from the backend API
	 *
	 * @param date the date to separate the 2 period to compare
	 * 
	 * @returns The promise from the fetch API containing the score distribution graph.
	 * If it fails, return a promise with mocked data.
	 */
	async getScoreDistribution(appId: string, date: Date): Promise<any> {
		const endpoint = `${this._BASE_API}/scoreDistribution`
		try {
			const params: { [k: string]: any } = {}
			if (appId) {
				params.appId = appId
			}
			if (date) {
				params.date = date.toLocaleString()
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
	 * Fetch the means graph from the backend API
	 *
	 * @param timeDelta Define the duration in days on which it computes cumulatives results
	 * @param ignore The number of first reviews to ignore
	 * 
	 * @returns The promise from the fetch API containing the means graph.
	 * If it fails, return a promise with mocked data.
	 */
	async getMeans(appId: string, timeDelta: number, ignore: number): Promise<any> {
		const endpoint = `${this._BASE_API}/means`
		try {
			const params: { [k: string]: any } = {}
			if (appId) {
				params.appId = appId
			}
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
}