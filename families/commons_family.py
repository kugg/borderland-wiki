# -*- coding: utf-8  -*-
"""Family module for Wikimedia Commons."""

__version__ = '$Id$'

import family


# The Wikimedia Commons family
class Family(family.WikimediaFamily):

    """Family class for Wikimedia Commons."""

    def __init__(self):
        """Constructor."""
        super(Family, self).__init__()
        self.name = 'commons'
        self.langs = {
            'commons': 'commons.wikimedia.org',
        }

        self.namespaces[4] = {
            '_default': [u'Commons', 'Project'],
            'commons': [u'Commons', u'COM'],
        }
        self.namespaces[5] = {
            '_default': [u'Commons talk', 'Project talk'],
        }
        self.namespaces[100] = {
            '_default': u'Creator',
        }
        self.namespaces[101] = {
            '_default': u'Creator talk',
        }
        self.namespaces[102] = {
            '_default': u'TimedText',
        }
        self.namespaces[103] = {
            '_default': u'TimedText talk',
        }
        self.namespaces[104] = {
            '_default': u'Sequence',
        }
        self.namespaces[105] = {
            '_default': u'Sequence talk',
        }
        self.namespaces[106] = {
            '_default': [u'Institution', u'Museum'],
        }
        self.namespaces[107] = {
            '_default': [u'Institution talk', u'Museum talk'],
        }
        self.namespaces[460] = {
            '_default': [u'Campaign'],
        }
        self.namespaces[461] = {
            '_default': [u'Campaign talk'],
        }
        self.namespaces[490] = {
            '_default': [u'GWToolset'],
        }
        self.namespaces[491] = {
            '_default': [u'GWToolset talk'],
        }
        self.namespaces[1198] = {
            '_default': u'Translations',
        }
        self.namespaces[1199] = {
            '_default': u'Translations talk',
        }

        self.interwiki_forward = 'wikipedia'

        self.category_redirect_templates = {
            'commons': (
                u'Category redirect',
                u'Categoryredirect',
                u'Catredirect',
                u'Cat redirect',
                u'Catredir',
                u'Cat-red',
                u'See cat',
                u'Seecat',
                u'See category',
                u'Redirect category',
                u'Redirect cat',
                u'Redir cat',
                u'Synonym taxon category redirect',
                u'Invalid taxon category redirect',
                u'Monotypic taxon category redirect',
            ),
        }

        self.disambcatname = {
            'commons':  u'Disambiguation'
        }

    def dbName(self, code):
        return 'commonswiki_p'

    def shared_data_repository(self, code, transcluded=False):
        """Return the shared data repository for this site."""
        return ('wikidata', 'wikidata')
