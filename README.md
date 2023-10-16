# App-Reviews-Analyser

A small tool to analyse reviews on playstore.

# How to run it
1. Clone the project wherever you want
2. Install the requirements listed in `requirements.txt` with `pip`
3. Run the following commands with Python 3.10+
   - `python -m flask run -h localhost -p 8080` in `/src` to launch Flask server
   - `npm run dev` in `/front` to launch vue.js server (running on port 5173)

# Flask API

- **GET** `/getReviews` (*not fully working yet*)
  - Fetch reviews from app and save them in resources/out.csv ***(need to be done first)***

- **GET** `/compute/scoreDistribution?date=str`
  - Return an image of a bar chart representing the score distribution before and after FEH Pass
  - URL parameters:
    - date: datetime in string format - Date to compare score distribution (if empty, no comparaison)

- **GET** `/compute/means?timeDelta=int&ignore=int`
  - Return an image of a graph of the cumulative means of score reviews
  - URL parameters:
    - timeDelta: strictly positive int - Define the duration on which it computes cumulative results (default = 30)
    - ignore: positive int - Indicates the number of first reviews to skip (default = 0)

- **GET** `/compute/stats`
  - Return a string JSON with differents stats

- **GET** `/wordcloud?alpha=int&n=int&lang=str&score=int&start1=str&end1=str&start2=str&end2=str`
  - Return a HTML page with 2 wordclouds from reviews data
  - URL parameters:
    - alpha: positive int - Parameters to reduce noises in data
    - n: strictly positive int - Define the number of word per token vocabulary (group of consecutive word)
    - lang: str - Language of analysed reviews from the following list []
    - score: int between 0 and 5 - Filter reviews on score (take all if empty or 0)
    - start1: str - First period start date to compare
    - end1: str - First period end date to compare
    - start2: str - Second period start date to compare
    - end2: str - Second period end date to compare

# Powered by:

- facundoolano: https://github.com/facundoolano/google-play-scraper
- WordCloud: https://github.com/amueller/word_cloud
- Inspirateur: https://github.com/Inspirateur