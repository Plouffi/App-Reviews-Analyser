import ServiceRestResource from './ServiceRestResource';
import { GpsApp } from '@/gpsApp';

export default class GPSRestResource extends ServiceRestResource {

	readonly _BASE_API = '/gpsApp'

	/**
	 * Fetch the search result from the backend API
	 *
	 * @param searchTerm Search terms
	 * 
	 * @returns The promise from the fetch API containing search result.
	 * If it fails, return a promise with mocked data.
	 */
	async searchApp(searchTerm: string): Promise<[{ [k: string]: any }]> {
		const endpoint = `${this._BASE_API}/search`
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
		const endpoint = `${this._BASE_API}/detail`
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
 * Trigger the scraping process on the backend API
 *
 * @param appId the app ID 
 * 
 * @returns The promise from the fetch API containing the success result
 */
	async scrapingApp(appId: string): Promise<GpsApp> {
		const endpoint = `${this._BASE_API}/scraping`
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
}