from bs4 import BeautifulSoup as bs
import requests
import os
from datetime import datetime, date
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.cell.cell import Cell
from email_scanner import EmailConnect


# Applies formatting to the data to match the sheet
def apply_formatting(data, ws):
    for d in data:
        d = Cell(ws, column='A', row=1, value=d)
        d.font = Font(name='Calibri', size=9)
        d.alignment = Alignment(horizontal='center',
                                vertical='center',
                                wrap_text=True)
        yield d

    d[2].alignment = Alignment(horizontal='justify')

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
    try:
        time = datetime.strptime(link_data[0], '%d/%m/%Y').strftime('%d.%m.%y')
    except ValueError:
        time = date.today().strftime('%d.%m.%y')

    # Appending data to a list (required for openpyxl.append())
    data.append(time)
    data.append(' '.join(link_data[2:]))
    data.append('\n' + soup.find('div', class_='profile_tweet_content').get_text() + '\n')

    # Pass data to worksheet
    insert_data(data)


# Removes duplicates whilst maintaining order
def remove_duplicates(list_w_duplicates):
    return list(dict.fromkeys(list_w_duplicates))


# Picks out the correct content links from the email
def acquire_links(subject):
    ids = gmail.get_id_by_subject(subject)
    html = gmail.get_html(ids)

    e_soup = bs(html, 'html.parser')

    links = []
    for link in e_soup.find_all('a'):
        if 'tvbizz.net/newsitemsocial' in link.get('href'):
            links.append(link.get('href'))

    return remove_duplicates(links)


if __name__ == '__main__':
    gmail = EmailConnect(os.getenv('IMAP_HOST'), os.getenv('IMAP_USER'), os.getenv('APP_PASS'))
    link_list = acquire_links('TVBIZZ')
    for url in link_list:
        parse_content(url)
    print(f'Added data from {len(link_list)} links.')