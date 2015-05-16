# -*- coding: utf-8  -*-
"""Family module for Wikimedia species wiki."""

__version__ = '$Id$'

import family


# The wikispecies family
class Family(family.WikimediaFamily):

    """Family class for Wikimedia species wiki."""

    def __init__(self):
        """Constructor."""
        super(Family, self).__init__()
        self.name = 'species'
        self.langs = {
            'species': 'species.wikimedia.org',
        }

        self.namespaces[4] = {
            '_default': [u'Wikispecies', self.namespaces[4]['_default']],
        }
        self.namespaces[5] = {
            '_default': [u'Wikispecies talk', self.namespaces[5]['_default']],
        }

        self.interwiki_forward = 'wikipedia'
