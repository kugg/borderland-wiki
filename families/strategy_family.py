# -*- coding: utf-8  -*-
"""Family module for Wikimedia Strategy Wiki."""

__version__ = '$Id$'

import family


# The Wikimedia Strategy family
class Family(family.WikimediaFamily):

    """Family class for Wikimedia Strategy Wiki."""

    def __init__(self):
        """Constructor."""
        super(Family, self).__init__()
        self.name = 'strategy'
        self.langs = {
            'strategy': 'strategy.wikimedia.org',
        }

        self.namespaces[4] = {
            '_default': [u'Strategic Planning', 'Project'],
        }
        self.namespaces[5] = {
            '_default': [u'Strategic Planning talk', 'Project talk'],
        }
        self.namespaces[106] = {
            '_default': [u'Proposal'],
        }
        self.namespaces[107] = {
            '_default': [u'Proposal talk'],
        }

        self.interwiki_forward = 'wikipedia'

    def dbName(self, code):
        """Return the database name for this family."""
        return 'strategywiki_p'
