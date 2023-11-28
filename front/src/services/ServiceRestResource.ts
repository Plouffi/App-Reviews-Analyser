export default class ServiceRestResource {

	readonly _BASE_URL = import.meta.env.VITE_BASE_URL
	readonly _HEADERS = {
		'Accept': 'application/json',
		'Content-Type': 'application/json'
	}

	/**
	 * Build the URL request
	 *
	 * @param endpoint the requested endpoint
	 * 
	 * @returns the url
	 */
	protected buildURL(endpoint: string): string {
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
	protected handleError(endpoint: string, err: unknown): string {
		const msg = `Error while requesting ${endpoint} : ${err}`
		console.error(msg)
		return msg
	}
}