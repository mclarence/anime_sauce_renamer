import requests
from bs4 import BeautifulSoup
import os
import logging
from Models.Results import Results
from Services.ServicesEnum import ServicesEnum as Service
from jikanpy import Jikan
from jikanpy import exceptions
from difflib import SequenceMatcher
import re


class IqdbService:
    def __init__(self, workingDirectory):
        self.workingDirectory = workingDirectory
        self.logger = logging.getLogger(__name__)
        self.startTime = 0
        self.requestCount = 0
        self.jikan = Jikan()

    def getSauce(self, filename: str) -> Results:
        searchResult = self.__query_iqdb(os.path.join(self.workingDirectory, filename))
        return self.__parse_results(searchResult)

    def __query_iqdb(self, filename):
        url = 'https://iqdb.org'
        files = {'file': (filename, open(filename, 'rb'))}
        res = requests.post(url, files=files)
        return res

    def __parse_results(self, result) -> Results:



        sauceData = Results(Service.IQDB, False)
        soup = BeautifulSoup(result.text, 'html.parser')
        try:
            tables = soup.find_all('table')
            search_result = tables[1].findChildren("th")[0].get_text()
        except:
            return ['server-error']
        tags = []
        if search_result == 'No relevant matches':
            sauceData.resultsFound = False
        else:
            print('Match Found')
            alt_string = tables[1].findChildren("img")[0]['alt']
            img_src_string = tables[1].findChildren("a")[0]['href']

            if img_src_string.startswith("//gelbooru.com"):
                sauceData.gelbooru_id = int(re.findall(r"(?<=id=).*", img_src_string)[0])
                sauceData.resultsFound = True
            elif img_src_string.startswith("//chan.sankakucomplex.com"):
                sauceData.sankakucomplex_id = int(re.findall(r"(?<=show/).*", img_src_string)[0])
                sauceData.resultsFound = True
            elif img_src_string.startswith("//danbooru.donmai.us.com"):
                sauceData.danbooru_id = int(re.findall(r"(?<=posts/).*", img_src_string)[0])
                sauceData.resultsFound = True
            elif img_src_string.startswith("//anime-pictures.net"):
                sauceData.anime_pictures_id = int(re.findall(r"(?<=view_post/).*(?=\?)", img_src_string)[0])
                sauceData.resultsFound = True
            elif img_src_string.startswith("//www.zerochan.net"):
                sauceData.zerochan_id = int(re.findall(r"(?<=net/).*", img_src_string)[0])
                sauceData.resultsFound = True
            elif img_src_string.startswith("//yande.re"):
                sauceData.yandere_id = int(re.findall(r"(?<=show/).*", img_src_string)[0])
                sauceData.resultsFound = True


            tag_string_index = alt_string.find('Tags:')
            if tag_string_index == -1:
                tags.append('undefined')
                sauceData.resultsFound = False
            else:
                tag_string = alt_string[tag_string_index + 6:]
                tag_string = tag_string.lower()
                tag_string_formatted = ''.join(c for c in tag_string if c not in ',')
                tags = list(set(tag_string_formatted.split(" ")))
                sauceData.resultsFound = True
        return sauceData
