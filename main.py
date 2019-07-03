from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.cell.cell import Cell


# Applies formatting to the data to match the sheet
def apply_formatting(data, ws):
    for d in data:
        d = Cell(ws, column='A', row=1, value=d)
        d.font = Font(name='Calibri', size=9)
        d.alignment = Alignment(horizontal='center',
                                vertical='center',
                                wrap_text=True)
        yield d


def insert_data(data):
    wb = load_workbook('data/database.xlsx')
    ws = wb.active
    ws.append(apply_formatting(data, ws))
    wb.save('data/database.xlsx')


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


# Removes duplicates whilst maintaining order
def remove_duplicates(list_w_duplicates):
    return list(dict.fromkeys(list_w_duplicates))


# Picks out the correct content links from the email
def acquire_links():
    email = open('data/email.htm', encoding='utf16')
    e_soup = bs(email.read(), 'html.parser')

    l = []
    for link in e_soup.find_all('a'):
        if 'tvbizz.net/newsitemsocial' in link.get('href'):
            l.append(link.get('href'))

    return remove_duplicates(l)


for url in acquire_links():
    print(f'Added data from: {url}')
    parse_content(url)