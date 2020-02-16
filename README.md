# Feh-Pass-Reviews

A small tool to analyse reviews on playstore about FEH pass.

Fire Emblem Heroes is a free-to-play tactical role-playing game developed by Intelligent Systems and published by 
Nintendo for Android and iOS.
To celebrate its third anniversary, the game introduce a premium pass to unlock different features (cosmetic, boost, QoL).
The goal of this tool is to visualize how much this pass has impacting the PlayStore's reviews and the application's score.

# How to run it
1. Clone the project wherever you want
2. Install the requirements listed in `requirements.txt` with `pip`
3. Run the following commands with Python 3.5+
   - `main.py get_reviews` to fetch reviews from the Playstore (**need to be done first**)
   - `main.py compute_data` to computing statistics and plot graphs
   - `main.py word_cloud` to create word_cloud based on reviews' content

# Powered by:

- facundoolano: https://github.com/facundoolano/google-play-scraper
- WordCloud: https://github.com/amueller/word_cloud
- Inspirateur: https://github.com/Inspirateur