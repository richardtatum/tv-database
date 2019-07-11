# tv_database
Hooks into email via IMAP, scrapes links from a newsletter based on a subject line search, then formats that data into an excel spreadsheet which is uploaded to Dropbox.

## Prerequisites
### IMAP Access
* The host for your IMAP connection. If you are using gmail this is `imap.gmail.com`. 

This will be saved in the `.env` file under `IMAP_HOST`.

<br>

* The username for your IMAP connection. Usually this is just your email address.

This will be saved in the `.env` file under `IMAP_USER`.

### Gmail App Password
If you use 2FA to secure your email, you will be required to assign an App password to get access with IMAPClient. Head to https://myaccount.google.com/apppasswords to create a 16 letter code. This code will be saved in the `.env` file under `APP_PASS`.

*Take note, the spaces are important and required!*
![](https://i.imgur.com/lKSoClR.png)

### Dropbox Developer Access
We are using dropbox to store the file once we are finished, so it can be accessed by the client wherever it is required. To use the dropbox API we need a key. Head to https://www.dropbox.com/developers/apps/create to one, then scroll down to 'Generate Access Token'. This will be saved in the `.env` file under `DBX_TOKEN`.

![](https://i.imgur.com/oK97sSo.png)

## Code Prerequisites

This script requires Python 3.6 or above.

### Packages

Install all the packages in `requirements.txt`:

```
pip3 install -r /path/to/requirements.txt
```

