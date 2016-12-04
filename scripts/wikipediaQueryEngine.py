from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import wikipedia
import utils
import sys
import json

class WikipediaQueryEngine:
    '''
    This query and scraping class is only relevant for the html structure of wikipedia
    pages around 2016.
    '''
    scraped_pages_by_url = {}
    results_by_tuple = {}

    def __init__(self):
        wikipedia.set_lang("fr")

    def build_binominal_name_for_query(self, genus, species):
        infered_binominal_name = genus+' '+species
        infered_binominal_name = infered_binominal_name.replace(' x ', ' ×')
        return infered_binominal_name

    def build_species_name_from_binominal_name(self, binominal_name, genus):
        binominal_name_words = binominal_name.split()
        normalized_genus = utils.normalize(genus)
        species_words = []
        for binominal in binominal_name_words:
            normalized_binominal = utils.normalize(binominal)
            if normalized_binominal != normalized_genus:
                species_words.append(normalized_binominal)
        species = ""
        for word in species_words:
             species += word.lower() + ' '
        return species.strip()

    def enrich_data(self, name_french, genus, species):        
        """
        Returns a dictionary in the form of:
        {
            "genus" : "..."
            "species" : "..."
            "genus_page" : {
                                "url" : "..."
                                "page_title" : "..."
                                "page_subtitle" : "..."
                                "description" : "..."
                           }
            "species_page" : {
                                "url" : "..."
                                "page_title" : "..."
                                "page_subtitle" : "..."
                                "description" : "..."
                             }
            "info_french" : {
                                ...
                            }   
        }
        """    

        if (name_french, genus, species) in WikipediaQueryEngine.results_by_tuple:
            return WikipediaQueryEngine.results_by_tuple[(name_french, genus, species)]

        undefined_species = False

        # This step is important : when names such as "Erable indéterminé" come up,
        # Wikipedia API often gives strange results ("Erable indéterminé" ~> "Violon")
        words = name_french.split()
        name = ""
        for word in words:
            if(utils.normalize(word) == 'indetermine'):
                undefined_species = True
            else:
                name += word+' '
        name = name.strip()

        result = { 'genus':'', 'genus_page':{}, 'species':'', 'species_page':{}, 'info_french':{} }

        if(undefined_species):
            # We only have to find a genus page
            queries_for_genus = set()
            queries_for_genus.add(genus)
            queries_for_genus.add(name.split()[0])
            queries_for_genus.add(name)    

            for query_for_genus in queries_for_genus:
                genus_page = self.find_genus_page_for(query_for_genus)
                if genus_page:
                    result["genus_page"] = genus_page.copy()
                    result["genus"] = genus_page["info_french"]["Genre"]
                    break
        else:
            # We have to find a genus page AND a species page
            species_page = self.find_species_page_for(name)
            if not species_page :
                # plant name did not return a species page, use binominal name build from genus and species names
                species_page = self.find_species_page_for(self.build_binominal_name_for_query(genus, species))
            if species_page: 
                # we finaly found a species page 
                result["species_page"] = species_page.copy()
                result["species"] = self.build_species_name_from_binominal_name(species_page["info_french"]["Nom binominal"], species_page["info_french"]["Genre"])

            # And also the corresponding genus page
            genus_page = self.find_genus_page_for(name)
            queries_for_genus = set()
            if species_page:
                queries_for_genus.add(species_page["info_french"]["Genre"])
            if name.strip():
                queries_for_genus.add(name.split()[0])
            queries_for_genus.add(genus)
            for query_for_genus in queries_for_genus:
                genus_page = self.find_genus_page_for(query_for_genus)
                if genus_page:
                    result["genus_page"] = genus_page.copy()
                    result["genus"] = genus_page["info_french"]["Genre"]
                    break

        max_page_info = {}
        if "genus_page" in result and result["genus_page"]:
            max_page_info = result["genus_page"]["info_french"].copy()
            del result["genus_page"]["info_french"] 

        species_page_info = {}
        if "species_page" in result and result["species_page"]:
            species_page_info = result["species_page"]["info_french"].copy()
            del result["species_page"]["info_french"]

        max_page_info.update(species_page_info)

        if max_page_info:
            result["info_french"] = max_page_info

        WikipediaQueryEngine.results_by_tuple[(name_french, genus, species)] = result.copy()

        return result

    def find_genus_page_for(self, query):
        return self.find_page_for(query, species=False)

    def find_species_page_for(self, query):
        return self.find_page_for(query, species=True)

    def find_page_for(self, query, species=True):
        """
        Returns a dictionary in the form of:
        {
            "url" : "..."
            "page_title" : "..."
            "page_subtitle" : "..."
            "description" : "..."
            "info_french" : "..."
        }
        """
        results = {}

        # query wikipedia API
        try:
            page = wikipedia.page(wikipedia.search(query)[0])
            url = page.url

            page_results = {}

            # scrape given url
            if url in WikipediaQueryEngine.scraped_pages_by_url:
                page_results = WikipediaQueryEngine.scraped_pages_by_url[url]
            else:                            
                page_results = self.scrape_page(url)
                WikipediaQueryEngine.scraped_pages_by_url[url] = page_results

            # check if page is relevant (must refer to a plantae)
            if "Règne" not in page_results["info_french"] or utils.normalize(page_results["info_french"]["Règne"]) != "plantae":
                raise Exception

            if species:
                # Check if page is species
                if("Nom binominal" not in page_results["info_french"]):
                    # Page is not a species
                    raise Exception
                else:
                    results["info_french"] = page_results["info_french"].copy()
                    results["url"] = page.url
                    results["page_title"] = page.title
                    if("page_subtitle" in page_results):
                        results["page_subtitle"] = page_results["page_subtitle"]
                    results["description"] = page.summary
            else :
                # Check if page is genus
                if("Genre" not in page_results["info_french"] or "Nom binominal" in page_results["info_french"]):
                    # Not a genus
                    raise Exception
                else:
                    results["info_french"] = page_results["info_french"].copy()
                    results["url"] = page.url
                    results["page_title"] = page.title
                    if("page_subtitle" in page_results):
                        results["page_subtitle"] = page_results["page_subtitle"]
                    results["description"] = page.summary
        except:
            results = {}

        return results

    def scrape_page(self, url):

        results = {}

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
                elif(center_taxobox_title == 'Genre'):
                     info["Genre"] = center_taxobox.select('span[lang=\"la\"]')[0].get_text()

            subtitle_spans = soup.select('span#sous_titre_h1')
            if subtitle_spans is not None:
                subtitle = ""
                if(len(subtitle_spans)>0):
                    subtitle = subtitle_spans[0].text
                for i in range(len(subtitle_spans)-1):
                    subtitle += ' / '+subtitle_spans[i+1].text
                if(subtitle.strip()):
                    results["page_subtitle"] = subtitle
            results["info_french"] = info
        except:
            results["info_french"] = {}

        return results
