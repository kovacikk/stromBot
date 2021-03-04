#drive.py

import pickle
import os
import io
from apiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tabulate import tabulate
from apiclient.http import MediaFileUpload
import google_auth_oauthlib.flow
import shutil
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./drive/token.pickle'):
        with open('./drive/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './drive/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./drive/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)




# Looks for and downloads memes from the google drive not in the local folders
# Updates Folder found in PATH, using the folder with the NAME in the google drive
#
async def update(path, name, messageStart, message, post):
    #Update Classic Memes
    service = get_gdrive_service()

    # Get Folder ID for Classic Memes folder
    """
    results = service.files().list(q='name="Kek"').execute().get('files', [])
    for result in results:
        print(result.get('id'))
    results = service.files().list(q='name="Cringe"').execute().get('files', [])
    for result in results:
        print(result.get('id'))      
    """ 

    driveMeme = []
    driveDict = {} 

    page_token = None
    counter = 0
    responses = {}
    while True:
        if (name == "Classic Memes"):
            responses = service.files().list(q='"1MCpKK8qwbzpzFRu0rybwqisnreoa6k7B" in parents', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        elif (name == "Warrior Cats"):
            responses = service.files().list(q='"1FRGzx9qPRdFifo-jZliFz8gx-70qZZ_G" in parents', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        elif (name == "Bulborbs"):
            responses = service.files().list(q='"1VjkqcKJFxvXQp1yLpqtiVpcYXfZIFSFS" in parents', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        elif (name == "Good Rates"):
            responses = service.files().list(q='"1HdvYwYDiwmQb_IZNRh8QV6n7IYyC0a6-" in parents', fields='nextPageToken, files(id, name)', pageToken=page_token).execute() 
        elif (name == "Bad Rates"):
            responses = service.files().list(q='"1q-HBINKngi-gPmA2DFYoFGpvdxmBLz6O" in parents', fields='nextPageToken, files(id, name)', pageToken=page_token).execute() 
        elif (name == "Other Rates"):
            responses = service.files().list(q='"195zBIPW4gzksNVWlWGitGfjIrX5tmOHq" in parents', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        elif (name == "Kek"):
            responses = service.files().list(q='"1KDflBiAeRAlMS6wM3-8vDbp0XSBMdwee" in parents', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        elif (name == "Cringe"):
            responses = service.files().list(q='"1K8o0r-LtNTt0A-zIZh_juqmMUVjNLZ64" in parents', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        else:
            return

        for response in responses.get('files', []):
            counter = counter + 1
            #print(response.get('name'))
            file_id = response.get('id')
            file_name = response.get('name')
            driveMeme.append(response.get('name'))

            driveDict[file_name] = file_id

        page_token = responses.get('nextPageToken', None)
        
        if page_token is None:
            break

    driveMeme.sort()

    # Get Memes currently in bot
    localMeme = os.listdir(path)
    localMeme.sort()

    driveMeme = set(driveMeme)
    difference = driveMeme.symmetric_difference(set(localMeme))
    
    yes = 0
    no = 0

    #print("Adding Classic Memes")
    #ctx.send("Adding Classic Memes")
    
    count = 0
    for meme in difference:
        if meme in driveMeme:
            count = count + 1

    first_added = ""

    if (count > 0):
        bar = '|'
        for square in range(20):
            bar = bar + '□'
        bar = bar + '|\n'
        await post.edit(content = messageStart + bar + '-----------------------------------\n' + message)

    for meme in difference:
        #if yes == 2:
        #    break
        # Memes not yet added to local
        if meme in driveMeme:
            if yes == 0:
                first_added = meme

            yes = yes + 1

            #Download Meme to Drive

            request = service.files().get_media(fileId=driveDict[meme])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

            fh.seek(0)
            with open(path + meme, 'wb') as f:
                shutil.copyfileobj(fh, f, length=131072)
            
            percent = int((float(yes) / float(count)) * 20)
            bar = '|'
            for square in range(percent):
                bar = bar + '■'

            for square in range(20 - percent):
                bar = bar + '□'

            bar = bar + '|\n'

            await post.edit(content = messageStart + bar + '-----------------------------------\n' + message)

        # Memes not yet added to drive
        else:
            no = no + 1

    #print(yes, no)

    if (yes == 0):
        message = "No " + name + " added\n"
    else:
        message = "Added: " + name + ": " + str(yes) + "\n-------- including: " + first_added + "\n"

    if name == "Good Rates" or name == "Bad Rates" or name == "Other Rates" or name == "Kek" or name == "Cringe":
        message = str(yes)

    return message


    """
    #Download Files From Drive
    #file_id = '0BwwA4oUTeiV1UVNwOHItT0xfa2M'
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download", (int(status.progress() * 100)))

    fh.seek(0)
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(fh, f, length=131072)

    
    file_metadata = {
        'name': 'makoto.png'#,
        #'parents': 
    }

    media = MediaFileUpload('./makoto.png', mimetype='image/png', resumable=True)
   
    

    #Upload Files to Drive
    new = service.files().create(body = file_metadata, media_body = media).execute()
    
    print(new.get('id'))
    """

def list_files(items):
    """given items returned by Google Drive API, prints them in a tabular way"""
    if not items:
        # empty drive
        print('No files found.')
    else:
        rows = []
        for item in items:
            # get the File ID
            id = item["id"]
            # get the name of file
            name = item["name"]
            try:
                # parent directory ID
                parents = item["parents"]
            except:
                # has no parrents
                parents = "N/A"
            try:
                # get the size in nice bytes format (KB, MB, etc.)
                size = get_size_format(int(item["size"]))
            except:
                # not a file, may be a folder
                size = "N/A"
            # get the Google Drive type of file
            mime_type = item["mimeType"]
            # get last modified date time
            modified_time = item["modifiedTime"]
            # append everything to the list
            rows.append((id, name, parents, size, mime_type, modified_time))
        print("Files:")
        # convert to a human readable table
        table = tabulate(rows, headers=["ID", "Name", "Parents", "Size", "Type", "Modified Time"])
        # print the table
        print(table)


