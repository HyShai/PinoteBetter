from functools import wraps
import atexit
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Pinote-Better.py'}


class PinoteError(Exception):

    @staticmethod
    def error_handler(msg=''):
        def error_handler_decorator(func):
            @wraps(func)
            def func_wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    raise PinoteError("Error while executing '{}' -- {}\n{}"
                                      .format(func.func_name, repr(e), msg))
            return func_wrapper
        return error_handler_decorator


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
        r = self._cached_session.post(
            'https://pinboard.in/auth/', data=self.post_auth,
            headers=HEADERS, allow_redirects=False)
        r.raise_for_status()
        if 'error' in r.headers.get('location'):
            self._cached_session = None
            raise Exception('Invalid login')

    @atexit.register
    def __del__(self):
        try:
            self._cached_session.get('https://pinboard.in/logout/', allow_redirects=False)
        except Exception:
            pass

    @PinoteError.error_handler()
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

        r = self.__session.post('https://pinboard.in/note/add/',
                                data=data, headers=HEADERS,
                                allow_redirects=False)
        r.raise_for_status()

    @PinoteError.error_handler()
    def get_all_notes(self):
        r = requests.get('https://api.pinboard.in/v1/notes/list?format=json',
                         auth=self.basic_auth)
        r.raise_for_status()
        return r.json()

    @PinoteError.error_handler()
    def get_note_html(self, note_id):
        r = self.__session.get(
            'https://notes.pinboard.in/u:{}/notes/{}'.format(self.username, note_id))
        r.raise_for_status()
        html = r.text
        soup = BeautifulSoup(html, "lxml")
        note_html = soup.find('blockquote', {'class': 'note'})
        return note_html

    @PinoteError.error_handler()
    def edit_note(self, title, note, note_id, use_markdown=False):
        data = {
            'slug': note_id,
            'action': 'update',
            'title': title,
            'note': note,
            'use_markdown': 'on' if use_markdown else 'off'
        }
        r = self.__session.post('https://notes.pinboard.in/u:{}/notes/{}/edit/'
                                .format(self.username, note_id), data=data, headers=HEADERS)
        r.raise_for_status()

    @PinoteError.error_handler()
    def delete_note(self, note_id):
        if not self._delete_token:
            r = self.__session.get(
                'https://notes.pinboard.in', headers=HEADERS)
            r.raise_for_status()
            html = r.text
            soup = BeautifulSoup(html, "lxml")
            self._delete_token = soup.find(
                'input', {'name': 'token'}).get('value')
        data = {
            'token': self._delete_token,
            'action': 'delete_note',
            'id': note_id
        }
        r = self.__session.post('https://notes.pinboard.in/',
                                data=data, headers=HEADERS)
        r.raise_for_status()
