# -*- coding: utf-8  -*-
"""Family module for Wikitech."""
__version__ = '$Id$'

import family


# The Wikitech family
class Family(family.Family):

    """Family class for Wikitech."""

    def __init__(self):
        """Constructor."""
        super(Family, self).__init__()
        self.name = 'wikitech'
        self.langs = {
            'en': 'wikitech.wikimedia.org',
        }

        self.namespaces[4] = {
            '_default': [u'Wikitech', self.namespaces[4]['_default']],
        }
        self.namespaces[5] = {
            '_default': [u'Wikitech talk', self.namespaces[5]['_default']],
        }

    def version(self, code):
        """Return the version for this family."""
        return '1.21wmf8'

    def scriptpath(self, code):
        return ''
