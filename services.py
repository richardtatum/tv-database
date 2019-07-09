from imapclient import IMAPClient
from dotenv import load_dotenv
import dropbox
import email
import logging

logger = logging.getLogger(__name__)
load_dotenv()


class EmailConnect:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.login()

    def login(self):
        client = IMAPClient(self.host, use_uid=True, ssl=True)
        client.login(self.username, self.password)
        self.client = client

    def get_id_by_subject(self, subject, folder='INBOX'):
        logger.info(f'Searching for emails with subject <{subject}>')
        self.client.select_folder(folder)
        self.search = ['SUBJECT', subject]
        return self.client.search(self.search)

    def get_html(self, email_id):
        logger.info('Retrieving HTML of selected emails')
        data = []
        for uid, message_data in self.client.fetch(email_id, 'RFC822').items():
            email_message = email.message_from_bytes(message_data[b'RFC822'])

            for part in email_message.walk():
                if part.get_content_type() == 'text/html':
                    data.append(part.get_payload(decode=True))
        return data

    def move(self, email_id, folder):
        logger.info(f'Moving {len(email_id)} message/s to {folder}')
        self.client.move(email_id, folder)

    def delete(self, ids):
        logger.info(f'Deleting {len(email_id)} message/s')
        self.client.delete_messages(ids)

    def logout(self):
        self.client.logout()


class Dropbox:
    def __init__(self, token):
        self.token = token
        self.login()

    def login(self):
        logger.info(f'Logging into Dropbox...')
        client = dropbox.Dropbox(self.token)
        self.client = client

    def upload(self, local, remote):
        with open(local, 'rb') as f:
            self.client.files_upload(f.read(), remote, mode=dropbox.files.WriteMode.overwrite)
        logger.info(f'File <{local}> uploaded to <{remote}>.')

    def download(self, local, remote):
        try:
            self.client.files_download_to_file(local, remote)
            logger.info(f'File <{remote}> downloaded to <{local}>.')
        except dropbox.exceptions.ApiError as err:
            logger.info(f'Lookup error: {err}')
            logger.info('Skipping...')
            pass
