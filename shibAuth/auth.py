__author__ = 'vladg'

import requests
from BeautifulSoup import BeautifulSoup
import shibAuth.config

class ShibAuth(requests.auth.AuthBase):
    """Attaches HTTP Digest Authentication to the given Request object."""
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def handle_302(self, r):
        """Takes the given response and tries digest-auth, if needed."""
        if r.url == shibAuth.config.auth_url:
            _r = requests.post(r.url,
                    {'j_username': self.username,
                     'j_password': self.password},
                    allow_redirects=True, cookies=r.cookies)
            if _r.status_code == 200:
                soup = BeautifulSoup(_r.content)
                form = soup.body.form
                if form is None:
                    print _r.content
                url = form['action']
                args = [x for x in form.findAll('input') if x['type'] == "hidden"]
                vars = [x['name'] for x in args]
                vals = [x['value'] for x in args]
                params = dict(zip(vars, vals))
                _r = requests.post(url, params, cookies=r.cookies,
                                   allow_redirects=True)
                r.request.cookies = _r.cookies
                r.request.send(anyway=True)
                _r = r.request.response
                _r.history.append(r)

                return _r

        return r

    def __call__(self, r):
        try:
            r.hooks['response'] = self.handle_302
        except TypeError:
            pass
        return r

