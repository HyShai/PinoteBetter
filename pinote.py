import exceptions

import requests
from bs4 import BeautifulSoup

PINBOARD_API_ENDPOINT = 'https://api.pinboard.in/v1/'
PINBOARD_NOTES_ENDPOINT = 'https://notes.pinboard.in/'
HEADERS = {'User-Agent': 'Pinote-Better.py'}


class Pinote(object):
    _cached_session = None
    _delete_token = None

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.basic_auth = requests.auth.HTTPBasicAuth(username, password)
        self.post_auth = {'username': username, 'password': password}

    @property
    def __session(self):
        if not self._cached_session:
            self.__login()
        return self._cached_session

    def __login(self):
        self._cached_session = requests.Session()
        self._cached_session.post(
            'https://pinboard.in/auth/', data=self.post_auth, headers=HEADERS)

    def add_note(self, title, note, tags, use_markdown=False, public=False):
        visibility = 'public' if public else 'private'
        data = {
            'title': title,
            'note': note,
            'tags': tags,
            'use_markdown': '1' if use_markdown else '0',
            'submit': 'save ' + visibility,
            'action': 'save_' + visibility
        }

        self.__session.post('https://pinboard.in/note/add/',
                            data=data, headers=HEADERS)

    def get_all_notes(self):
        notes = requests.get('https://api.pinboard.in/v1/notes/list?format=json',
                             auth=self.basic_auth)
        return notes.json()

    def get_note_html(self, note_id):
        html = self.__session.get(
            'https://notes.pinboard.in/u:hyshai/notes/' + note_id).text
        soup = BeautifulSoup(html, "lxml")
        note_html = soup.find('blockquote', {'class': 'note'})
        return note_html

    def edit_note(self, title, note, note_id, use_markdown=False):
        data = {
            'slug': note_id,
            'action': 'update',
            'title': title,
            'note': note,
            'use_markdown': 'on' if use_markdown else 'off'
        }
        self.__session.post('https://notes.pinboard.in/u:hyshai/notes/' +
                            note_id + '/edit/', data=data, headers=HEADERS)

    def delete_note(self, note_id):
        if not self._delete_token:
            html = self.__session.get(
                'https://notes.pinboard.in', headers=HEADERS).text
            soup = BeautifulSoup(html, "lxml")
            self._delete_token = soup.find(
                'input', {'name': 'token'}).get('value')
        data = {
            'token': self._delete_token,
            'action': 'delete_note',
            'id': note_id
        }
        self.__session.post('https://notes.pinboard.in/',
                            data=data, headers=HEADERS)
