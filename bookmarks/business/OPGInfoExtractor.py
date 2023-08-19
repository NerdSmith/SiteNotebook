import opengraph_py3


class OPGInfoExtractor:
    def __init__(self, url):
        self.target_url = url
        self.site_data = None

    def extract(self):
        self.site_data = opengraph_py3.OpenGraph(url=self.target_url, scrape=True)

    def info(self):
        if self.site_data is None:
            raise Exception("Execute .extract() first!")
        return self.site_data
