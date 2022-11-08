from __future__ import print_function

import io

import httplib2
import os
from apiclient import discovery
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class GoogleLoader:
    def __init__(self):

        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/drive-python-quickstart.json
        SCOPES = 'https://www.googleapis.com/auth/drive'
        CLIENT_SECRET_FILE = 'client_secret.json'  # Ваш client_secret.json, полученный в console.cloud.google.com/apis
        APPLICATION_NAME = 'google-drive'

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v3', http=http)  # Подготовленный авторизованный объект для запроса

    def download_file(self, real_file_id):
        """Downloads a file
        Args:
            real_file_id: ID of the file to download
        Returns : IO object with location.

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """

        try:
            file_id = real_file_id

            # pylint: disable=maybe-no-member
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f'Download {int(status.progress() * 100)}.')

        except HttpError as error:
            print(f'An error occurred: {error}')
            file = None

        return file.getvalue()


if __name__ == '__main__':
    # Создание авторизованного объекта для запросов к google drive
    google_loader = GoogleLoader()
    # Для загрузки файла с google drive нужен id файла
    # id файла берём из адресной строки при открытом файле в браузере
    # Например, https://docs.google.com/spreadsheets/d/1pOuPTSQUUOCVbNOG7kSDQhwUpYJF0vsh/edit#gid=593977617
    # 1pOuPTSQUUOCVbNOG7kSDQhwUpYJF0vsh - это id файла для скачивания
    # Ниже вписать id своего файла
    file_value = google_loader.download_file(real_file_id='1pOuPTSQUUOCVbNOG7kSDQhwUpYJF0vsh')
    # print(file_value)