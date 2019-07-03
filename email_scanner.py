from imapclient import IMAPClient
from dotenv import load_dotenv
import os
import email
load_dotenv()


def acquire_email(subject):
    with IMAPClient(host=os.getenv('IMAP_HOST'), use_uid=True, ssl=True) as client:
        client.login(os.getenv('IMAP_USER'), os.getenv('APP_PASS'))
        inbox = client.select_folder('INBOX')
        search = client.search(['SUBJECT', subject])
        for uid, message_data in client.fetch(search, 'RFC822').items():
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            
            # print(email_message.get_payload()[1])
            return email_message.get_payload()[1]
