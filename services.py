from imapclient import IMAPClient
from dotenv import load_dotenv
import dropbox
import email
import os

load_dotenv()


class EmailConnect:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.login()

    def login(self):
        print(f'Logging in as {self.username}.')
        client = IMAPClient(self.host, use_uid=True, ssl=True)
        client.login(self.username, self.password)
        self.client = client

    def get_id_by_subject(self, subject, folder='INBOX'):
        self.client.select_folder(folder)
        self.search = ['SUBJECT', subject]
        return self.client.search(self.search)

    def get_html(self, email_id):
        for uid, message_data in self.client.fetch(email_id, 'RFC822').items():
            email_message = email.message_from_bytes(message_data[b'RFC822'])

            for part in email_message.walk():
                if part.get_content_type() == 'text/html':
                    return part.get_payload(decode=True)


class Dropbox:
    def __init__(self, token):
        self.token = token
        self.login()

    def login(self):
        print(f'Logging into Dropbox...')
        client = dropbox.Dropbox(self.token)
        self.client = client

    def upload(self, local, remote):
        with open(local, 'rb') as f:
            self.client.files_upload(f.read(), remote, mode=dropbox.files.WriteMode.overwrite)
        print(f'File {local} uploaded to {remote}.')

    def download(self, local, remote):
        try:
            self.client.files_download_to_file(local, remote)
            print(f'File {remote} downloaded to {local}.')
        except dropbox.exceptions.ApiError as err:
            print(f'Lookup error: {err}')
            print('Skipping...')
            pass

