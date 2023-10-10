# Feh-Pass-Reviews

A small tool to analyse reviews on playstore about FEH pass.

Fire Emblem Heroes is a free-to-play tactical role-playing game developed by Intelligent Systems and published by 
Nintendo for Android and iOS.
To celebrate its third anniversary, the game introduce a premium pass to unlock different features (cosmetic, boost, QoL).
The goal of this tool is to visualize how much this pass has impacting the PlayStore's reviews and the application's score.

# How to run it
1. Clone the project wherever you want
2. Install the requirements listed in `requirements.txt` with `pip`
3. Run the following commands with Python 3.10+
   - `python -m flask run -h localhost -p 8080` to launch Flask server

# Flask API

- **GET** `/getReviews`
  - Fetch reviews from Fire Emblem Heroes app and save them in resources/out.csv ***(need to be done first)***

- **GET** `/compute/scoreDistribution`
  - Return an image of a bar chart representing the score distribution before and after FEH Pass

- **GET** `/compute/means`
  - Return an image of a graph of the cumulative means of score reviews

- **GET** `/compute/stats`
  - Return a string JSON with differents stats

- **GET** `/wordcloud`
  - Return a HTML page with 2 wordclouds from reviews data

# Powered by:

- facundoolano: https://github.com/facundoolano/google-play-scraper
- WordCloud: https://github.com/amueller/word_cloud
- Inspirateur: https://github.com/Inspirateur