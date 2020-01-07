from Services.ServicesEnum import ServicesEnum as Services
class Results:
    def __init__(self, service: Services, resultsFound: bool):
        self.service = service
        self.resultsFound = resultsFound
        self.material = None
        self.characters = None
        self.pixiv_id = None
        self.nijie_id = None
        self.seiga_id = None
        self.anidb_aid = None
        self.pawoo_id = None
        self.bcy_id = None
        self.da_id = None
        self.gelbooru_id = None
        self.danbooru_id = None
        self.sankakucomplex_id = None
        self.anime_pictures_id = None
        self.e_shuushuu_id = None
        self.zerochan_id = None
        self.konachan_id = None
        self.yandere_id = None