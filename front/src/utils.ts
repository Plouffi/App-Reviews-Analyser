import mock from "./mock"

export default class Utils {
	static debounce<Params extends any[]>(
		func: (...args: Params) => any,
		timeout: number,
	): (...args: Params) => void {
		let timer: NodeJS.Timeout
		return (...args: Params) => {
			clearTimeout(timer)
			timer = setTimeout(() => {
				func(...args)
			}, timeout)
		}
	}
	static getMockDetail(mockKey: string): { [k: string]: any } {
		return mock.detail[mockKey]
	}
	static getMockSearch(mockKey: string): [{ [k: string]: any }] {
		return mock[mockKey]
	}
	static getMockImage(mockKey: string): Blob {
		return mock.image[mockKey]
	}
}