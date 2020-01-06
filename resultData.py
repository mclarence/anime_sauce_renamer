class ResultData:
    def __init__(self, resultsFound: bool, material: str = None, characters: str = None, pixiv_id: int = None, nijie_id: int = None, seiga_id: int = None, anidb_aid: int = None, pawoo_id: int = None, bcy_id: int = None, da_id: int = None, gelbooru_id: int = None, danbooru_id: int = None):
        self.resultsFound = resultsFound
        self.material = material
        self.characters = characters
        self.pixiv_id = pixiv_id
        self.nijie_id = nijie_id
        self.seiga_id = seiga_id
        self.anidb_aid = anidb_aid
        self.pawoo_id = pawoo_id
        self.bcy_id = bcy_id
        self.da_id = da_id
        self.gelbooru_id = gelbooru_id
        self.danbooru_id = danbooru_id