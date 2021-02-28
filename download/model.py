class DownloadModel:
    def __init__(self,):
        self.title = ''
        self.artist = ''
        self.tags = []
        self.page_count = ''
        self.image_path = None

    def setTitle(self, title):
        self.title = title

    def setArtist(self, artist):
        self.artist = artist

    def setTags(self, tags):
        self.tags = tags

    def setPageCount(self, page_count):
        self.page_count = page_count

    def setImagePath(self, image_path):
        self.image_path = image_path
