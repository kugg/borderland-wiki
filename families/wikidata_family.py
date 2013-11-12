# -*- coding: utf-8  -*-

__version__ = '$Id$'

import family

# The wikidata family


class Family(family.WikimediaFamily):
    def __init__(self):
        super(Family, self).__init__()
        self.name = 'wikidata'
        self.langs = {
            'wikidata': 'www.wikidata.org',
            'test': 'test.wikidata.org',
        }

        # Override defaults

        # Most namespaces are inherited from family.Family.
        # Translation used on all wikis for the different namespaces.
        # (Please sort languages alphabetically)
        # You only need to enter translations that differ from _default.
        self.namespaces[4] = {
            '_default': [u'Wikidata', u'WD', 'Project'],
        }

        self.namespaces[5] = {
            '_default': [u'Wikidata talk', u'WT', 'Project talk'],
        }

        self.namespaces[120] = {
            '_default':[u'Property', u'P'],
        }

        self.namespaces[121] = {
            '_default': u'Property talk',
        }

        self.namespaces[122] = {
            '_default': u'Query',
        }

        self.namespaces[123] = {
            '_default': u'Query talk',
        }

        self.namespaces[1198] = {
            '_default': u'Translations',
        }

        self.namespaces[1199] = {
            '_default': u'Translations talk',
        }

    def shared_data_repository(self, code, transcluded=False):
        """Always return a repository tupe. This enables testing whether
        the site opject is the repository itself, see Site.is_data_repository()

        """
        if transcluded:
            return (None, None)
        else:
            return (code, self.name)
