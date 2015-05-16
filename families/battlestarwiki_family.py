# -*- coding: utf-8  -*-
"""Family module for Battlestar Wiki."""

__version__ = '$Id$'

import family


# The Battlestar Wiki family, a set of Battlestar wikis.
# http://battlestarwiki.org/
class Family(family.Family):

    """Family class for Battlestar Wiki."""

    def __init__(self):
        """Constructor."""
        family.Family.__init__(self)
        self.name = 'battlestarwiki'

        self.languages_by_size = ['en', 'de', 'fr', 'zh', 'es', 'ms', 'tr', 'simple']

        for lang in self.languages_by_size:
            self.langs[lang] = '%s.battlestarwiki.org' % lang

        # Most namespaces are inherited from family.

        self.namespaces[4] = {
            '_default': u'Battlestar Wiki',
        }
        self.namespaces[5] = {
            '_default': u'Battlestar Wiki talk',
            'de': u'Battlestar Wiki Diskussion',
            'es': u'Battlestar Wiki Discusión',
            'fr': u'Discussion Battlestar Wiki',
            'ms': u'Perbincangan Battlestar Wiki',
            'tr': u'Battlestar Wiki tartışma',
        }

        # Custom namespaces that a needed

        self.namespaces[100] = {
            '_default': u'Portal',
        }
        self.namespaces[101] = {
            '_default': u'Portal talk',
        }
        self.namespaces[102] = {
            '_default': u'Sources',
        }
        self.namespaces[103] = {
            '_default': u'Sources talk',
        }
        self.namespaces[104] = {
            '_default': u'Quotes',
        }
        self.namespaces[105] = {
            '_default': u'Quotes talk',
        }
        self.namespaces[106] = {
            '_default': u'Podcast',
        }
        self.namespaces[107] = {
            '_default': u'Podcast talk',
        }

    def hostname(self, code):
        """Return the hostname for a site in this family."""
        return '%s.battlestarwiki.org' % code

    def version(self, code):
        """Return the version for this family."""
        return "1.16.4"
