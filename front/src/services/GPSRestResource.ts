import { GpsApp } from '@/gpsApp';
import Utils from '@/utils';

export default class GPSRestResource {

	/**
	 * Fetch the search result from the backend API
	 *
	 * @returns The promise from the fetch API containing search result.
	 * If it fails, return a promise with mocked data.
	 */
	async searchApp(searchTerm: string): Promise<[{ [k: string]: any }]> {
		try {
			const params: { [k: string]: any } = {}
			if (searchTerm.length) {
				params.search = searchTerm
				const query = new URLSearchParams(params)
				const res = await fetch(`http://localhost:5173/api/searchApp?${query}`, {
					method: 'GET',
				})
				if (!res.ok) throw res.statusText
				return res.json()
			}
			throw 'Error params'
		} catch (e) {
			console.error(`Error while requesting /searchApp :${e}`)
			return new Promise<[{ [k: string]: any }]>(function (resolve) {
				resolve(Utils.getMockSearch('search'))
			})
		}
	}

	/**
	 * Fetch the detail app from the backend API
	 *
	 * @returns The promise from the fetch API containing the app detail.
	 * If it fails, return a promise with mocked data.
	 */
	async getAppDetail(appId: string): Promise<GpsApp> {
		try {
			const params: { [k: string]: any } = {}
			params.id = appId
			const query = new URLSearchParams(params)
			const res = await fetch(`http://localhost:5173/api/appDetail?${query}`, {
				method: 'GET',
			})
			if (!res.ok) throw res.statusText
			return res.json()
		} catch (e) {
			console.error(`Error while requesting /appDetail :${e}`)
			return new Promise<GpsApp>(function (resolve) {
				const app = new GpsApp()
				app.init(Utils.getMockDetail(appId))
				resolve(app)
			})
		}
	}

	/**
	 * Fetch the score distribution graph from the backend API
	 *
	 * @returns The promise from the fetch API containing the score distribution graph.
	 * If it fails, return a promise with mocked data.
	 */
	async getScoreDistribution(date: Date): Promise<any> {
		try {
			const res = await fetch('http://localhost:5173/api/compute/scoreDistribution', {
				method: 'POST',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(date ? { 'date': date.toLocaleString() } : {})
			})
			if (!res.ok) throw `${res.statusText} - ${res.status}`
			return res.blob()
		} catch (e) {
			let msg = `Error while requesting /compute/scoreDistribution : ${e}`
			console.error(msg)
			throw msg
		}
	}
}