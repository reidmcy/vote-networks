import os
import os.path
import requests
import json
import urllib

apiURL = 'https://api.github.com'

tokenPath = os.path.normpath(os.path.join(os.path.dirname(__file__) + '/..' , 'token.txt'))

class Github_Session(object):
    def __init__(self, auth = None):
        if auth is None:
            try:
                with open(tokenPath) as f:
                    username, token = f.readline().strip().split()
                    self.auth = (username, token)
            except FileNotFoundError:
                self.auth = None

        self.remaining = 0
        self.reset = 0
        self.lastResponse = None
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({'Accept' : 'application/vnd.github.squirrel-girl-preview'})
        self.checkRate()

    def __repr__(self):
        return "<Github_Session {} remaining>".format(self.remaining)

    def checkRate(self):
        rateLimiting = self.get('{}/rate_limit'.format(apiURL))
        self.remaining = rateLimiting['rate']['remaining']
        self.reset = rateLimiting['rate']['reset']
        return rateLimiting['rate']['remaining']

    def get(self, target):
        if target.startswith('http'):
            url = target
        else:
            url = urllib.parse.urljoin(apiURL, target)
        r = self.session.get(url)
        self.lastResponse = r
        if not r.ok:
            raise RuntimeError('Invalid request: {}\n{}'.format(url, r.text))
        try:
            if len(r.links) > 0 and 'next' in r.links:
                return json.loads(r.text) + self.get(r.links['next']['url'])
            else:
                return json.loads(r.text)
        except json.JSONDecodeError:
            return []