from urllib.request import urlopen
import urllib.request
import json

class CustomSearchEngine:

    
    def get_results(self, query, start=1):
        key = 'AIzaSyB5G3zlUEBWyL18hv7ZSPjJvDH7mcwPHpo'
        cx = '007910554110679342100%3Anj4qfuidjj4'
        url = 'https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q="%s"&start=%d' %(key, cx, query, start)
        results = []
        try:
            response = urlopen(url).read().decode('utf8')
            json_content = json.loads(response)
            comments = json_content['items']
            for comment in comments:
                print('Link: %s' %(comment['link']))
                print('---Comment: --------')
                print(comment['snippet'])
                results.append({'url': comment['link'], 'description': comment['snippet']})

                print('---Meta info ------')
                pagemap = json_content.get('pagemap')
            
                if pagemap:
                    # check if the site it's a question site
                    questionsite = pagemap.get('qapage')
                    if questionsite:
                        print('--- Question --')
                        print(questionsite['description'])
                        results.append({'url': comment['link'], 'description': questionsite['description']})

                    # check for twitter descriptions
                    metatags = pagemap.get('metatags')
                    if metatags:
                        twitter_desc = metatags.get('twitter:description')
                        if twitter_desc:
                            print('--Twitter description --')
                            print(twitter_desc)
                            results.append({'url': comment['link'], 'description': twitter_desc})
        except Exception as e:
            print("# Error: ", e)
        return results
            

    def iterate_pages(self, query, page_num):
        start = 1
        comments = []
        for i in range(1, page_num+1):
            comments += self.get_results(query, start=start)
            start += 10
        return comments

if __name__ == "__main__":
    crawler = CustomSearchEngine()
    print("Comments:")
    print(crawler.iterate_pages("rethinkdb+performance+is", 4))

