import mock from "./mock"

/**
 * Module exporting Utils class
 */
export default class Utils {
	private static readonly _languages = [
		{
			value: 'en',
			title: 'English',
			country: 'us',
			props: {
				prependAvatar: 'https://cdn.vuetifyjs.com/images/flags/us.png'
			}
		},
		{
			value: 'fr',
			title: 'Français',
			country: 'fr',
			props: {
				prependAvatar: 'https://cdn.vuetifyjs.com/images/flags/fr.png'
			}
		}
	]

	/**
	 * Get the list of available languages 
	 * 
	 * @returns A list of the languages
	 */
	static getLanguagesApp(): any[] {
		return this._languages
	}

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
	static getMockImage(mockKey: string): string {
		return mock.image[mockKey]
	}
}