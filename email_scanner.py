from imapclient import IMAPClient
from dotenv import load_dotenv
import os
import email
load_dotenv()


class EmailConnect:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.login()

    def login(self):
        print(f'Logging in as {self.username.')
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
