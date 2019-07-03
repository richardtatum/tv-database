from bs4 import BeautifulSoup as bs
import requests

def parse_content(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    data = []

    # Section that holds the date and country
    link_data = soup.find('div', class_='profile_tweet_date_country').get_text().split()

    # Format the date to requested style
    time = datetime.strptime(link_data[0], '%d/%m/%Y').strftime('%d.%m.%y')

    # Appending data to a list (required for openpyxl.append())
    data.append(time)
    data.append(' '.join(link_data[2:]))
    data.append(soup.find('div', class_='profile_tweet_content').get_text())

    # Pass data to worksheet
    insert_data(data)


urls = ['http://tvbizz.net/newsitemsocial?newsId=128888','http://tvbizz.net/newsitemsocial?newsId=128937',
        'http://tvbizz.net/newsitemsocial?newsId=128936', 'http://tvbizz.net/newsitemsocial?newsId=128931']
for url in urls:
    parse_content(url)
