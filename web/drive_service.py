from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload
from .models import Drive


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive']

def signInAndDownloadDB():
    creds = None
    file_id = ""
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        #Get the newest version
        for item in items:
            if item['name'] == "TrackHistory.db":
                print("Hei")
                file_id = item['id']
                print(file_id)
                break
    if(file_id):
        file_id = file_id
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO("TrackHistory.db", 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        print("done")
        return "Downloaded the newest database version."
    
    return "The google drive does not contain TrackHistory.db. Please upload data from the mobile app."

def signOut():
    if os.path.exists('token.json'):
        os.remove('token.json')
        return "You have been signed out"
    else:
        return "Already signed out"

def getSignInStatus():
    if os.path.exists('token.json'):
        return True
    return False



#signInAndDownloadDB()
#signOut()
#testDBDrive()