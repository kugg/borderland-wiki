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
            'client': 'wikidata-test-client.wikimedia.de',
            'test': 'test.wikidata.org',
        }

        # Override defaults

        # Most namespaces are inherited from family.Family.
        # Translation used on all wikis for the different namespaces.
        # (Please sort languages alphabetically)
        # You only need to enter translations that differ from _default.
        self.namespaces[4] = {
            '_default': [u'Wikidata', u'WD', 'Project'],
            'client': u'Test Wikipedia',
        }
        self.namespaces[5] = {
            '_default': [u'Wikidata talk', u'WT', 'Project talk'],
            'client': u'Test Wikipedia talk',
        }
        self.namespaces[120] = {
            'test': u'Property',
            'wikidata': u'Property',
        }
        self.namespaces[121] = {
            'test': u'Property talk',
            'wikidata': u'Property talk',
        }
        self.namespaces[122] = {
            'test': u'Query',
            'wikidata': u'Query',
        }
        self.namespaces[123] = {
            'test': u'Query talk',
            'wikidata': u'Query talk',
        }
        self.namespaces[1198] = {
            'test': u'Translations',
            'wikidata': u'Translations',
        }
        self.namespaces[1199] = {
            'test': u'Translations talk',
            'wikidata': u'Translations talk',
        }

    def scriptpath(self, code):
        if code == 'client':
            return ''
        return super(Family, self).scriptpath(code)

    def shared_data_repository(self, code, transcluded=False):
        """Always return a repository tupe. This enables testing whether
        the site opject is the repository itself, see Site.is_data_repository()

        """
        if transcluded:
            return (None, None)
        else:
            if code == 'wikidata':
                return ('wikidata', 'wikidata')
            elif code == 'test':
                return ('test', 'wikidata')
            else:
                return (None, None)
        
    def protocol(self, code):
        if code == 'client':
            return 'http'
        return super(Family, self).protocol(code)
