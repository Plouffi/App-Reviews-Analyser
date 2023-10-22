# App-Reviews-Analyser

A small tool to analyse reviews on playstore.

# Prerequisites
- Python 3.10+
- NodeJS 18+

# Project Setup
## Flask API
- Got to `/api` directory
- Install python requirements listed in `requirements.txt` with `py -m pip install -r ./requirements.txt`
- Run the following command `py -m flask run -h localhost -p 8080` to launch Flask server

API description can be find [here](https://github.com/Plouffi/App-Reviews-Analyser/blob/master/src/openapi.yaml)

## VueJS front
- Got to `/front` directory
- Install node requirements listed in `package.json` with `npm install`
- Run the following command `npm run dev` to launch vue.js server (running on port 5173)

# Powered by:
- facundoolano: https://github.com/facundoolano/google-play-scraper
- WordCloud: https://github.com/amueller/word_cloud
- Inspirateur: https://github.com/Inspirateur