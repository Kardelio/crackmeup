import urllib
import random
import re
from random import randint

from bs4 import BeautifulSoup

def jokesDotCCDotcom():

	'''to get random jokes from jokes.cc.com, we're going to use the API I dug up from their site (#sweg).
	-Send a request to http://jokes.cc.com/feeds/random/(any number between 1-6811)
	-Data recieved is in JSON
	-Extract this link, send a urllib request there and scrape out the joke from the HTML recieved
	'''
	randomLinkToGoToAPI = 'http://jokes.cc.com/feeds/random/' + str(randint(1, 6779))
	JSONData = urllib.urlopen(randomLinkToGoToAPI).read()
	#parse data
	parsedJokeLink = JSONData[JSONData.index('http') : JSONData.index('","queryString')].replace('\\',"")
	#Now send a request to parse this random joke link
	handle = urllib.urlopen(parsedJokeLink)
	htmlGunk =  handle.read()
	soup = BeautifulSoup(htmlGunk, "html.parser")
	jokeData = soup.findAll('div', {'class':'content_wrap'})[0].get_text()
	if 'Next' in jokeData:
		jokeData = jokeData[jokeData.index('Next')+5:]
	return jokeData
	

def randomjokesDotcom():
	categories = {'Random':'haha', 'One Liners':'oneliners', 'True Stories':'news',
	'Signs of Our Times':'signs', 'Nerdy Jokes':'nerd','Quotes':'quotes',
	'Professional':'professional', 'Light Bulb':'lightbulb', 
	'Gender Battles':'couples', 'Riddles':'riddles', 'Religion':'religion',
	'Gross':'gross', 'Blondes':'blonde', 'Politics':'politics', 'Just do it':'doit',
	'Laws':'laws', 'PG 13':'dirty', 'Racist':'ethnic'}

	category = categories[random.choice(categories.keys())]

	urlToRead = "http://www.randomjoke.com/topic/" + (category) + (".php")
	handle = urllib.urlopen(urlToRead)
	htmlGunk =  handle.read()
	soup = BeautifulSoup(htmlGunk, "html.parser")
	#print soup.prettify().encode('utf-8')
	# Find out the exact position of the joke in the page
	jokeSectionText = soup.body.findAll('tr')[1].findAll('td')[2].findAll('p')[1].get_text() # magic
	# The joke ends at the keyword 'Over'
	joke = jokeSectionText[:jokeSectionText.index('Over')].strip()
	return joke

def jokesYouDotcom():
	urlToRead = "http://www.jokesyou.com/"
	handle = urllib.urlopen(urlToRead)
	htmlGunk =  handle.read()
	soup = BeautifulSoup(htmlGunk, "html.parser")
	joke = soup.findAll('div', {'class':'right'})[0].findAll('p')[0]
	joke = str(joke)
	#Regex replace
	joke = re.sub(r'<p>', r'', joke)
	joke = re.sub(r'</p>|<br/>', r'\n', joke)
	return joke

def randomJokesPointDotcom():
	randomJokeId = str(randint(1, 1000))
	#Apprently on their site they have 1000 jokes, but this is not true
	#there are MANY jokes missing when their random number is selected
	#so I also implemented a recursive function so that if no joke is
	#found on the page then it re runs this function with hopefully a
	#different random number, however I will make a ticket to store the failed
	#numbers so that in future runs of this function those numbers can be
	#avoided. That is a TODO
	urlToRead = "http://www.jokespoint.com/joke.php?id=" + randomJokeId
	handle = urllib.urlopen(urlToRead)
	htmlOutput =  handle.read()
	soupedHtml = BeautifulSoup(htmlOutput, "html.parser")
	possJokes = soupedHtml.findAll('div', {'class':'joke'})
	numberOfAvailableJokes = len(possJokes)

	if numberOfAvailableJokes > 0:
	   joke = soup.findAll('div', {'class':'joke'})[0].findAll('p')[0]
	   joke = str(joke)
	   joke = re.sub(r'<p>', r'', joke)
	   joke = re.sub(r'</p>|<br/>', r'\n', joke)
	   return joke
	else:
	   return randomJokesPointDotcom()

whichSite = randint(1,3)
if whichSite == 1:
	print jokesDotCCDotcom()
	print "\nSource - jokes.cc.com"

elif whichSite == 2:
	print jokesYouDotcom()
	print "\nSource - jokesyou.com"

elif whichSite == 3:
	print randomJokesPointDotcom()
	print "\nSource - jokespoint.com"

else:
	#Also this will currently never get hit the random int
	#generator only handles 1, 2 and (now) 3? Is there a reason for this?
	print randomjokesDotcom()
	print "\nSource - randomjoke.com"