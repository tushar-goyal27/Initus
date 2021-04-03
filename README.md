# Initus_bot
This repository contains the codes for the bot.

## Bot description
The prefix of the bot is '_'

### Commands
- hi command: Says hi
- imdb command: gets the details of movie or tv series from the imdb website
- slang command: gets the meaning of a slang from urbandictionary 
- news command: gets the news of a topic entered

### Requirements
- discord.py
- python-dotenv
- bs4 and requests for web scraping
- lxml parser for parsing websites html code
- standard python libraries

### Technical Details
- the news command gets the data from newsapi.org which requires api key of newsapi.org 
- the urbandictionary and imdb are scraped via the bot and don't require any api key
