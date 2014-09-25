# -*- coding: utf-8  -*-
"""Family module for Wikia."""

__version__ = '$Id$'

import family


# The Wikia Search family
# user-config.py: usernames['wikia']['wikia'] = 'User name'
class Family(family.Family):

    """Family class for Wikia."""

    def __init__(self):
        """Constructor."""
        family.Family.__init__(self)
        self.name = u'wikia'

        self.langs = {
            u'wikia': None,
        }

        self.namespaces[4] = {
            '_default': [u'search', self.namespaces[4]['_default']],
        }
        self.namespaces[5] = {
            '_default': [u'search talk', self.namespaces[5]['_default']],
        }
        self.namespaces[100] = {
            '_default': u'Forum',
        }
        self.namespaces[101] = {
            '_default': u'Forum talk',
        }
        self.namespaces[112] = {
            '_default': u'Mini',
        }
        self.namespaces[113] = {
            '_default': u'Mini talk',
        }

    def hostname(self, code):
        """Return the hostname for every site in this family."""
        return u'www.wikia.com'

    def version(self, code):
        """Return the version for this family."""
        return "1.19.20"

    def scriptpath(self, code):
        """Return the script path for this family."""
        return ''
