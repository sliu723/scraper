from bs4 import BeautifulSoup
import requests

links = []

def scrape_irrawaddy(query, keywords):
    query = query.lower()
    keywords = keywords.lower()
    html_text = requests.get('https://www.irrawaddy.com/?s=' + query).text
    soup = BeautifulSoup(html_text, 'lxml')
    articles = soup.find_all('article', class_='article')
    for article in articles:
        try:
            title = article.find('h2', class_='title').find('a').getText().strip().lower()
            href = article.find('h2', class_='title').find('a')['href']
            body = article.find('div', class_="entry").getText().strip().lower()
        except AttributeError:
            continue
        if(keywords in title or keywords in body):
            links.append(href)

def scrape_myanmar(query, keywords):
    query = query.lower()
    keywords = keywords.lower()
    html_text = requests.get('https://myanmar-now.org/en/search/node/all?mefibs-form-search-only-combine=' + query).text
    soup = BeautifulSoup(html_text, 'lxml')
    articles = soup.find_all('div', class_="search-text")
    for article in articles:
        title = article.find('a').getText().strip().lower()
        href = 'https://myanmar-now.org/' + article.find('a')['href']
        body = article.find('div', class_='search-body').getText().strip().lower()
        if(keywords in title or keywords in body):
            links.append(href)
    page = 1
    while(page < 5):
        html_text = requests.get('https://myanmar-now.org/en/search/node/all?mefibs-form-search-only-combine=' + query + '&page=' + str(page)).text
        soup = BeautifulSoup(html_text, 'lxml')
        articles = soup.find_all('div', class_="search-text")
        for article in articles:
            try:
                title = article.find('a').getText().strip().lower()
                href = 'https://myanmar-now.org/' + article.find('a')['href']
                body = article.find('div', class_='search-body').getText().strip().lower()
            except AttributeError:
                continue
            if(keywords in title or keywords in body):
                links.append(href)
        page += 1

def scrape_rfa(query, keywords):
    page = 0
    page_count = 30
    query = query.lower()
    keywords = keywords.lower()
    while(page < 3):
        html_text = requests.get('https://www.rfa.org/english/@@search?SearchableText=' + query + '&sort_on=Date&b_start:int=' + str(page * page_count)).text
        soup = BeautifulSoup(html_text, 'lxml')
        articles = soup.find_all('div', class_="searchresult")
        for article in articles:
            try:
                title = article.find('span', class_='result-title').find('a').getText().strip().lower()
                href = article.find('span', class_='result-title').find('a')['href']
                body = article.find('p', class_='croppedDescription').getText().strip().lower()
            except AttributeError:
                continue
            if(keywords in title or keywords in body):
                links.append(href)
        page += 1
def scrape_monitor(query, keywords):
    page = 1
    query = query.lower()
    keywords = keywords.lower()
    while(page < 5):
        html_text = requests.get('https://monitor.civicus.org/search/?page=' + str(page) + '&q=' + query).text
        soup = BeautifulSoup(html_text, 'lxml')
        articles = soup.find_all('div', class_="post")
        for article in articles:
            try:
                title = article.find('div', class_='details').find('h1', class_='post-title').find('a').getText().strip().lower()
                href = 'https://monitor.civicus.org/' + article.find('div', class_='details').find('h1', class_='post-title').find('a')['href']
                body = article.find('div', class_='details').find('p', class_='post-summary').getText().strip().lower()
            except AttributeError:
                continue
            if(keywords in title or keywords in body):
                links.append(href)
        page += 1

query = raw_input('Please specify your search word: \n')
keywords = raw_input('Please specify your in-text keywords: \n')

scrape_irrawaddy(query, keywords)
scrape_myanmar(query, keywords)
scrape_monitor(query, keywords)
scrape_rfa(query, keywords)
file = open('links.txt', 'w')
file.write('\n'.join(links))
file.close()

print('The results are exported to links.txt')











'''
https://www.irrawaddy.com/
https://myanmar-now.org/en
https://airtable.com/shr9w3z7dyIoqdUv4/tbl8hVtSci8VifbO9
rfa.org
https://monitor.civicus.org/search/?q=myanmar
'''