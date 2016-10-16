from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import wikipedia
import utils
import sys

class WikipediaQueryEngine:
    '''
    This query and scraping class is only relevant for the html structure of wikipedia
    pages around 2016.
    '''

    def __init__(self):
        wikipedia.set_lang("fr")
        self.results_by_name = {}
        self.name_by_url = {}

    def correct_and_enrich_species(self, name_french, genus, species):
        """
        Returns a dictionary in the form of:
        {
            "page_title" : "..."
            "page_subtitle" : "..."
            "suggested_name_french" : "..."
            "genus" : "..."
            "species" : "..."
            "info_french" : { ... }
        }
        Use suggested_name_french, genus, species to override given name_french, genus, species in data
        """

        # This step is important : when names such as "Erable indéterminé" comes up,
        # Wikipedia API often gives strange results ("Erable indéterminé" ~> "Violon")
        words = name_french.split()
        name = ""
        for word in words:
            if(utils.normalize(word) == 'indetermine'):
                pass
            else:
                name += word+' '
        name = name.strip()

        results = {}

        # try to find query in already scraped elements
        if(name in self.results_by_name):
            return self.results_by_name[name]

        # query wikipedia API

        page_not_species = False
        page_not_found = False

        try:
            page = wikipedia.page(name)
            url = page.url

            results["page_title"] = page.title
            results["url"] = url
            results["description"] = page.summary

            # see if url matches already scraped elements
            if(url in self.name_by_url):
                if(self.name_by_url[url] in self.results_by_name):
                    return self.results_by_name[self.name_by_url[url]]

            # scrape given url
            self.scrape_page(url, results)
            if("Nom binominal" not in results["info_french"]):
                page_not_species = True

        except:
            page_not_found = True

        if(page_not_species or page_not_found):
            # then the page we found referes most likely to a genus and not a species.
            # thus we have to try to find a species' page using provided genus and species to infer the french name of the species
            infered_binominal_name = genus+' '+species
            # if we query for a hybrid (binominal such as Aesculus ×carnea), we have to delete space between the x and the species names to its right
            # for wikipedia api to find it
            infered_binominal_name = infered_binominal_name.replace(' x ', ' ×')

            try:
                page2 = wikipedia.page(infered_binominal_name)
                url = page2.url
                 # see if url matches already scraped elements
                if(url in self.name_by_url):
                    return self.results_by_name[self.name_by_url[url]]
                self.scrape_page(url, results)
                results["genus"] = genus
                results["species"] = species
                results["page_title"] = page2.title
                results["url"] = url
                results["description"] = page2.summary
                results["suggested_name_french"] = results["page_title"]
                if("page_subtitle" in results and results["page_subtitle"].strip()):
                    results["suggested_name_french"] += " / "+results["page_subtitle"]
            except:
                # could not find anything using binominal name as query
                return {}

        else:
            # we found a species, yay !
            results["suggested_name_french"] = name_french # this name seems OK since we found a matching species
            if "Genre" in results["info_french"]:
                results["genus"] = results["info_french"]["Genre"]
                binominal_name_words = results["info_french"]["Nom binominal"].split()
                normalized_genus = utils.normalize(results["genus"])
                species_words = []
                for binominal in binominal_name_words:
                    normalized_binominal = utils.normalize(binominal)
                    if normalized_binominal != normalized_genus:
                        species_words.append(normalized_binominal)
                species = ""
                for word in species_words:
                     species += word.lower() + ' '
                species = species.strip()
                results["species"] = species
            else:
                results["genus"] = genus
                results["species"] = species

        # save scraped element in memory
        self.results_by_name[name] = results
        self.name_by_url[url] = name

        return results

    def scrape_page(self, url, results):

        raw = urlopen(url)
        soup = bs(raw, "html.parser")
        info = {}
        try:
            tables = soup.find_all('table',{'class':'taxobox_classification'})
            for table in tables:
                for tr in table.find_all('tr') :
                    th = tr.find('th')
                    td = tr.find('td')
                    info[th.text] = td.text
            center_taxoboxes = soup.find_all('p',{'class':'center taxobox_classification'})
            for center_taxobox in center_taxoboxes:
                center_taxobox_title = center_taxobox.find_previous_sibling('p').get_text()

                if(center_taxobox_title == 'Nom binominal' or center_taxobox_title == 'Hybride'):
                    binominal = center_taxobox.select('span[lang=\"la\"]')[0].get_text().replace("×", "× ")#binominal
                    info["Nom binominal"] = binominal
            subtitle_spans = soup.select('span#sous_titre_h1')
            if subtitle_spans is not None:
                subtitle = ""
                if(len(subtitle_spans)>0):
                    subtitle = subtitle_spans[0].text
                for i in range(len(subtitle_spans)-1):
                    subtitle += ' / '+subtitle_spans[i+1].text
                results["page_subtitle"] = subtitle
            results["info_french"] = info
        except:
            results["info_french"] = {}

'''
w = WikipediaQueryEngine()
r = w.correct_and_enrich_species("Noisetier à fruits ronds", "CORYLUS", "vellana")
print(r)
print('\n')
w = WikipediaQueryEngine()
r = w.correct_and_enrich_species("Marronnier rouge", "Aesculus", "x carnea")
print(r)
print('\n')
w = WikipediaQueryEngine()
r = w.correct_and_enrich_species("Chêne chevelu", "lol", "lil")
print(r)
print('\n')
w = WikipediaQueryEngine()
r = w.correct_and_enrich_species("Platane à feuilles d'érable", "lol", "lil")
print(r)
print('\n')
r = w.correct_and_enrich_species("Savonnier", "KOELREUTERIA", "paniculata")
print(r)
print('\n')
r = w.correct_and_enrich_species("Buis", "Buxus", "Sempervirens")
print(r)
print('\n')
r = w.correct_and_enrich_species("Erable", "blabla", "zopzop")
print(r)
print('\n')
r = w.correct_and_enrich_species("Platane commun", "blabla", "zopzop")
print(r)
print('\n')

r = w.correct_and_enrich_species("Févier d'Amérique sans épines", "CORYLUS", "saccharinum")
'''
