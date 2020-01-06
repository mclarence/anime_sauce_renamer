from saucenao import SauceNao
from saucenao import exceptions
from proxybroker import errors
from resultData import ResultData
import time
import logging
class Sauce:
    def __init__(self, workingDirectory, apiKey, similarity):
        self.workingDirectory = workingDirectory
        self.apiKey = apiKey
        self.logger = logging.getLogger(__name__)
        self.saucenao = SauceNao(directory=workingDirectory, output_type=SauceNao.API_JSON_TYPE,
                        api_key=apiKey)
        self.startTime = 0
        self.requestCount = 0
        self.similarity = similarity

    def getSauce(self, filename: str) -> ResultData:
        self.isRequestLimitReached()
        sauceResult = ResultData(False)
        while True:
            try:
                self.startTime = time.time()
                self.requestCount += 1
                searchResults = self.saucenao.check_file(filename)
                if not searchResults:
                    self.logger.warning("No results returned for file " + filename)
                    sauceResult.resultsFound = False
                    self.isRequestLimitReached()
                    return sauceResult
                else:
                    break
            except exceptions.DailyLimitReachedException as error:
                    self.logger.critical("Saucenao daily limit reached.")
                    raise error
            except exceptions.UnknownStatusCodeException:
                continue

        for result in searchResults:
            if float(result['header']['similarity']) >= self.similarity:
                resultData = result['data'].keys()
                if 'material' in resultData:
                    sauceResult.material = result['data']['material']
                if 'characters' in resultData:
                    sauceResult.characters = result['data']['characters'].split(",")
                if 'pixiv_id' in resultData:
                    sauceResult.pixiv_id = result['data']['pixiv_id']
                if 'nijie_id' in resultData:
                    sauceResult.nijie_id = result['data']['nijie_id']
                if 'seiga_id' in resultData:
                    sauceResult.seiga_id = result['data']['seiga_id']
                if 'anidb_aid' in resultData:
                    sauceResult.anidb_aid = result['data']['anidb_aid']
                if 'pawoo_id' in resultData:
                    sauceResult.pawoo_id = result['data']['pawoo_id']
                if 'bcy_id' in resultData:
                    sauceResult.bcy_id = result['data']['bcy_id']
                if 'da_id' in resultData:
                    sauceResult.da_id = result['data']['da_id']
                if 'gelbooru_id' in resultData:
                    sauceResult.gelbooru_id = result['data']['gelbooru_id']
                if 'danbooru_id' in resultData:
                    sauceResult.danbooru_id = result['data']['danbooru_id']
                if 'yandere_id' in resultData:
                    sauceResult.yandere_id = result['data']['yandere_id']
        self.logger.info("Results found for " + filename)
        sauceResult.resultsFound = True
        return sauceResult

    def isRequestLimitReached(self):
        end_time = time.time()
        elapsedTime = end_time - self.startTime
        if self.requestCount >= 5:
            if elapsedTime >= 29:
                self.logger.warning("30s request limited reached. Waiting 30 seconds...")
                time.sleep(30)
                self.requestCount = 0




















