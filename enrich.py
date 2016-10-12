from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url = "https://fr.wikipedia.org/wiki/%C3%89rable_plane"

#TODO : Build toolbox to validate and enrich raw data using wikipedia

def infobox() :
	raw = urlopen(url)
	soup = bs(raw, "html.parser")
	table = soup.find('table',{'class':'taxobox_classification'})
	for tr in table.find_all('tr') :
    		print(tr.text)

infobox()
