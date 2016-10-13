from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import wikipedia

"""
Results of query are in the form of :

{
   'info': 
         {'Ordre': 'Lamiales',
          'Nom binomial': 'Fraxinus ornus',
          'Division': 'Magnoliophyta',
          'Règne': 'Plantae',
          'Classe': 'Magnoliopsida',
          'Famille': 'Oleaceae',
          'Genre': 'Fraxinus'
         },
   'found': True,
   'name': 'Fraxinus ornus',
   'description': "Le Frêne à fleurs ou Orne (Fraxinus ornus L.,1753), parfois appelé Frêne à manne, ou Frêne orne, plus rarement Orne d'Europe, est un arbre de la famille des Oléacées.\nAutres noms communs : frêne à manne, orne à manne, frêne orne, orne d'Europe.\n\n",
   'url': 'https://fr.wikipedia.org/wiki/Fraxinus_ornus'
}

"""

class WikipediaQueryEngine:
    '''
    Warning : this query and scraping class is only relevant for the html structure of wikipedia
    pages around 2016.
    '''

    def __init__(self):
        wikipedia.set_lang("fr")
        self.results_by_name = {}
        self.name_by_url = {}

    def query_for(self, name):
        results = {}
        try:
            # try to find query in already scraped elements
            if(name in self.results_by_name):
                return self.results_by_name[name]

            # query wikipedia API
            page = wikipedia.page(name)
            url = page.url

            # see if url matches already scraped elements
            if(url in self.name_by_url):
                return self.results_by_name[self.name_by_url[url]]

            # scrape given url
            self.scrape_page(url, results)
            if("Genre" not in results["info"]):
                return {"found":False}
            results["name"] = page.title
            results["url"] = url
            results["description"] = page.summary
            results["found"] = True
            
            # save scraped element in memory
            self.results_by_name[name] = results
            self.name_by_url[url] = name

        except wikipedia.exceptions.PageError:
            return {"found":False}

        return results

    def scrape_page(self, url, results):
        raw = urlopen(url)
        soup = bs(raw, "html.parser")
        info = {}
        tables = soup.find_all('table',{'class':'taxobox_classification'})
        for table in tables:
            for tr in table.find_all('tr') :
                th = tr.find('th')
                td = tr.find('td')
                info[th.text] = td.text
        center_taxobox = soup.find('p',{'class':'center taxobox_classification'})
        i = center_taxobox.find('i')
        info["Nom binomial"] = i.text
        results["info"] = info
        

wqe = WikipediaQueryEngine()
print(wqe.query_for("frene à fleurs"))
