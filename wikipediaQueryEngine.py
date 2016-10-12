from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import wikipedia

"""
Results of query are in the form of :

{
    'found': True,
    'description': "...",
    'info': {   
                'Famille': 'Aceraceae',
                'Sous-classe': 'Rosidae',
                'Division': 'Magnoliophyta',
                'Genre': 'Acer',
                'Sous-règne': 'Tracheobionta',
                'Ordre': 'Sapindales',
                'Règne': 'Plantae',
                'Classe': 'Magnoliopsida'
            },
    'url': 'https://fr.wikipedia.org/wiki/%C3%89rable_plane'
}
"""

class WikipediaQueryEngine:

    def __init__(self):
        wikipedia.set_lang("fr")

    def query_for(self, name):
        results = {}
        try:
            page = wikipedia.page(name)
            url = page.url
            self.scrape_page(url, results)
            results["url"] = url
            results["description"] = page.summary
            results["found"] = True
        except wikipedia.exceptions.PageError:
            results["found"] = False
        return results

    def scrape_page(self, url, results):
        raw = urlopen(url)
        soup = bs(raw, "html.parser")
        info = {}
        table = soup.find('table',{'class':'taxobox_classification'})
        for tr in table.find_all('tr') :
            th = tr.find('th')
            td = tr.find('td')
            info[th.text] = td.text
        results["info"] = info

wqe = WikipediaQueryEngine()
print(wqe.query_for("Erable plane"))
