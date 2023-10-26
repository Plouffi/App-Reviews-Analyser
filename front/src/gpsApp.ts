/***
 * Class representing a GooglePlayStore app retrieve from the backend api
***/
export class GpsApp {
	id: string = ''
	title: string = ''
	icon: string = ''
	headerImage: string = ''
	video: string = ''
	videoImage: string = ''
	screenshots: [string] = ['']
	score: number = 0
	genre: string = ''
	categories: [string] = ['']
	price: number = 0
	currency: string = ''
	free: boolean = true
	summary: string = ''
	description: string = ''
	descriptionHTML: string = ''
	version: string = ''
	developer: string = ''
	developerWebsite: string = ''
	installs: string = ''
	realInstalls: number = 0
	reviews: number = 0
	url: string = ''

	// Initialiser from dict
	init(json: any) {
		this.id = json['id']
		this.title = json['title']
		this.icon = json['icon']
		this.headerImage = json['headerImage']
		this.video = json['video']
		this.videoImage = json['videoImage']
		this.screenshots = json['screenshots']
		this.score = json['score']
		this.genre = json['genre']
		this.categories = json['categories']
		this.price = json['price']
		this.currency = json['currency']
		this.free = json['free']
		this.summary = json['summary']
		this.description = json['description']
		this.descriptionHTML = json['descriptionHTML']
		this.version = json['version']
		this.developer = json['developer']
		this.developerWebsite = json['developerWebsite']
		this.installs = json['installs']
		this.realInstalls = json['realInstalls']
		this.reviews = json['reviews']
		this.url = json['url']
	}
}