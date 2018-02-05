from .github_session import Github_Session

import urllib
import collections.abc

emojiMapping = {
    '+1' : '👍',
    '-1' : '👎',
    'heart' : '❤️',
    'hooray' : '🎉',
    'laugh' : '😄',
    'confused' : '😕',
}

class Organization(object):
    def __init__(self, orgName, session = None):
        self.name = orgName
        self.url = 'orgs/{}'.format(orgName)
        if session is None:
            self.session = Github_Session()
        else:
            self.session = session
        self.info = self.session.get('orgs/{}'.format(self.name))
        self._repos = None

    @property
    def repos(self):
        if self._repos is None:
            self._repos = [Repo(r, session = self.session) for r in self.session.get(self.info['repos_url'])]
        return self._repos

class GH_Mapping_Object(collections.abc.Mapping):
    def __init__(self, data, session = None):
        self.data = data
        if session is None:
            self.session = Github_Session()
        else:
            self.session = session

        self._issues = None

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        for v in self.data:
            yield v

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return "<{} {} {}>".format(self.__class__.__name__, self.name, self.htmlURL)

    @property
    def htmlURL(self):
        return self['html_url']

    @property
    def apiURL(self):
        return self['url']

    @property
    def name(self):
        try:
            return self['name']
        except KeyError:
            return self['title']

    @property
    def actor(self):
        try:
            return self['user']['login']
        except KeyError:
            return self['owner']['login']

class Repo(GH_Mapping_Object):
    def __init__(self, data, session = None):
        super().__init__(data, session = session)
        self._issues = None

    @property
    def issues(self):
        if self._issues is None:
            self._issues = [Issue(i, session = self.session) for i in self.session.get(self['issues_url'].split('{')[0])]
        return self._issues

class Issue(GH_Mapping_Object):
    def __init__(self, data, session = None):
        super().__init__(data, session = session)

        self._reactions = None

    @property
    def reactions(self):
        if self._reactions is None:
            self._reactions = [Reaction(i, self, session = self.session) for i in self.session.get(self['reactions']['url'])]
        return self._reactions

class Reaction(GH_Mapping_Object):
    def __init__(self, data, issue, session = None):
        super().__init__(data, session = session)

        self.issue = issue

    @property
    def name(self):
        return emojiMapping[self['content']]

    @property
    def htmlURL(self):
        return self.issue.htmlURL

    def __repr__(self):
        return "<{} {} {}>".format(self.__class__.__name__, self.name, self.actor)