class Dataset:
    def __init__(self, catalog):
        self.url = catalog["url"]
        self.more = catalog["more"]
        self.next_page = catalog["next"]
        self.detail_pages = catalog["detail_pages"]
        self.details = catalog["details"]