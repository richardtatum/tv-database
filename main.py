from bs4 import BeautifulSoup as bs
from datetime import datetime, date
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.cell.cell import Cell
from services import EmailConnect, Dropbox
import requests
import os


# Applies formatting to the data to match the sheet
def apply_formatting(data, ws):
    for d in data:
        d = Cell(ws, column='A', row=1, value=d)
        d.font = Font(name='Calibri', size=9)
        d.alignment = Alignment(
            horizontal='center',
            vertical='center',
            wrap_text=True
        )
        yield d


def parse_content(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    data = []

    # Section that holds the date and country
    link_data = soup.find('div', class_='profile_tweet_date_country').get_text().split()

    # Format the date to requested style
    try:
        datetime.strptime(link_data[0], '%d/%m/%Y').strftime('%d/%m/%y')
    except ValueError:
        time = date.today().strftime('%d/%m/%y')

    # Appending data to a list (required for openpyxl.append())
    data.append(time)
    data.append(' '.join(link_data[2:]))
    data.append(soup.find('div', class_='profile_tweet_content').get_text())

    # Pass data to worksheet
    ws.append(apply_formatting(data, ws))


# Removes duplicates whilst maintaining order
def remove_duplicates(list_w_duplicates):
    return list(dict.fromkeys(list_w_duplicates))


# Picks out the correct content links from the email
def acquire_links(subject):
    # Acquire the ID of the email
    ids = gmail.get_id_by_subject(subject)

    # If no ID's are returned, logout and exit
    if len(ids) < 1:
        print(f'No emails found matching the requested subject <{subject}>.')
        print('Exiting...')
        gmail.logout()
        exit()

    # If there are links, pull the raw HTML
    html = gmail.get_html(ids)
    e_soup = bs(html, 'html.parser')

    # Adds correct links to a masterlist
    links = []
    for link in e_soup.find_all('a'):
        if 'tvbizz.net/newsitemsocial' in link.get('href'):
            links.append(link.get('href'))

    # Delete the email once we have finished
    # gmail.delete(ids)

    return remove_duplicates(links)


if __name__ == '__main__':
    # Load the document and worksheet
    wb = load_workbook('data/International Format Tracker.xlsx')
    ws = wb['TV BIZZ']
    print('Loading worksheet.')

    # Create a gmail instance and login
    gmail = EmailConnect(
        os.getenv('IMAP_HOST'),
        os.getenv('IMAP_USER'),
        os.getenv('APP_PASS'),
    )

    # Same for Dropbox
    # box = Dropbox(os.getenv('DBX_TOKEN'))
    # box.download('data/database.xlsx', '/database.xlsx')

    # Aquire all the data from each link and add it to the file
    link_list = acquire_links('Latest headlines on TVBIZZ')
    for url in link_list:
        parse_content(url)
    print(f'Added data from {len(link_list)} links.')

    # Save the new file
    wb.save('data/International Format Tracker.xlsx')

    # Upload to dropbox
    # box.upload('data/database.xlsx', '/database.xlsx')
