from bs4 import BeautifulSoup as bs
import requests

def parse_content(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')

    link_data = soup.find('div', class_='profile_tweet_date_country').get_text().split()

    data = {}
    data['date'] = link_data[0]
    data['country'] = ' '.join(link_data[2:])
    data['title'] = soup.find('div', class_='profile_tweet_title').get_text()
    data['content'] = soup.find('div', class_='profile_tweet_content').get_text()

    print(data)


url = 'http://tvbizz.net/newsitemsocial?newsId=128888'
# url = 'http://tvbizz.net/newsitemsocial?newsId=128909'
parse_content(url)
