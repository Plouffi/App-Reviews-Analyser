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
	static getMock(mockKey: string): { [k: string]: any } {
		return mock[mockKey]
	}
	static getListMock(mockKey: string): [{ [k: string]: any }] {
		return mock[mockKey]
	}
}