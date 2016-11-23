from urllib.request import urlopen
from bs4 import BeautifulSoup

class StackoverflowScrapper:

    def __init__(self, name):
        main_url = "http://stackoverflow.com/tags/%s/info" %(name)
        html = urlopen(main_url)
        self.bsObj = BeautifulSoup(html, "lxml")

    def check_wiki_extract_same_paragraph(self, tagInfo):
        wiki_extract = tagInfo.find('div', {'id': 'wiki-excerpt'})
        children = tagInfo.children
        childs = []
        for child in children:
            if child.name == 'p':
                childs.append(child.get_text())
        if childs[0] == wiki_extract.get_text().strip(): return True

    def get_tag_description(self):
        try:
            tagInfo = self.bsObj.find('div', {'class': 'post-text'})
            paragraphs = tagInfo.findAll("p")
            description = ""
            idx = 0
            if self.check_wiki_extract_same_paragraph(tagInfo): idx = 1
            for paragraph in paragraphs[idx:]:
                link = paragraph.find("a")
                if link is not None:
                    if link.get_text() != paragraph.get_text():
                        description += paragraph.get_text().strip(" ")
                else:
                    description += paragraph.get_text().strip(" ")
            for tag in self.bsObj.findAll("li"):
                if tag.find("a") is None:
                    description += tag.get_text()
            return description
        except Exception as e:
            print(str(e))
            return None

    def get_links(self):
        result_links = []
        try:
            tag_info = self.bsObj.find('div', {'class': 'post-text'})
            links = tag_info.findAll("a")
            for link in links:
                url = link.attrs['href']
                if '/questions/tagged' not in url:
                    title = link.get_text()
                    result_links.append({'title': title, 'url': url})
            return result_links
        except Exception as e:
            print(str(e))
            return None

    def get_stats(self):
        try:
            table = self.bsObj.find("table", {"id": "qinfo"})
            rows = table.findAll("tr")
            stats = ""
            for row in rows:
                for cell in row.findAll(['td']):
                    stats += cell.find("p").get_text().strip() + ' '
                stats += '\n'
            return stats
        except:
            return None


def get_followers(name):
    import selenium
    from selenium import webdriver
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.keys import Keys
    import time
    driver = webdriver.PhantomJS()
    driver.get('http://stackoverflow.com/tags')
    search_input = driver.find_element_by_id('tagfilter')
    search_input.send_keys(name)
    search_input.send_keys(Keys.RETURN)
    time.sleep(20)
    element = driver.find_element_by_link_text(name)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()
    time.sleep(10)
    info = driver.find_element_by_class_name('tm-sub-info')
    text = info.text
    print("Original: %s" %(text))
    followers, questions = text.split(',')
    followers = followers.replace('followers', '')
    followers = followers.replace('follower', '')

    if 'k' in followers:
        followers = followers.replace('k', '')
        followers = float(followers.strip(' '))
        followers = followers * 1000
    else:
        followers = int(followers.strip())


    questions = questions.replace('questions', '')
    questions = questions.replace('\nrss', '')
    if 'k' in questions:
        index = questions.index('k')
        questions = questions[:index]
        questions = questions.replace('k', '')
        questions = float(questions.strip(' '))
        questions = questions * 1000
    else:
        questions = int(questions)
    return followers, questions
