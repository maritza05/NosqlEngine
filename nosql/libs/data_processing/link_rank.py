from ..webcrawlers.mozscape_crawler.mozscape import Mozscape

class UrlRank:

    def __init__(self):
        self.client = Mozscape(
                    'mozscape-156a394681',
                        'f8572c1748959f150d4c2b0b8a0a814d')

    def get_rank_of_links(self, links):
        metrics = self.client.urlMetrics(links, Mozscape.UMCols.domainAuthority)
        return metrics

    def get_rank_of_link(self, link):
        metrics = self.client.urlMetrics(link, Mozscape.UMCols.domainAuthority)
        return metrics['pda']
