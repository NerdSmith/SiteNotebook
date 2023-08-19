from typing import Dict

import opengraph_py3


class OGPInfoExtractor:
    def __init__(self, url) -> None:
        self.target_url = url
        self.site_data = None

    def extract(self) -> None:
        self.site_data = opengraph_py3.OpenGraph(url=self.target_url, scrape=True)

    def info(self) -> Dict[str, str]:
        if self.site_data is None:
            raise Exception("Execute .extract() first!")
        return self.site_data
