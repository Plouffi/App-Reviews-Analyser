import mock from "./mock"

/**
 * Module exporting Utils class
 */
export default class Utils {
	/**
	 * Get the mocked data corresponding to the key (app ID)
	 * 
	 * @param mockKey The mock key of the data wanted
	 * 
	 * @returns A dict of the mocked data
	 */
	static getMockDetail(mockKey: string): { [k: string]: any } {
		return mock.detail[mockKey]
	}
	/**
	 * Get the mocked data for the search app function
	 * 
	 * @param mockKey The mock key of the data wanted
	 * 
	 * @returns A dict of the mocked data
	 */
	static getMockSearch(mockKey: string): [{ [k: string]: any }] {
		return mock[mockKey]
	}
	/**
	 * Get the path of a mocked image
	 * 
	 * @param mockKey The mock key of the data wanted
	 * 
	 * @returns The path to the mocked image
	 */
	static getMockImage(mockKey: string): Blob {
		return mock.image[mockKey]
	}
}