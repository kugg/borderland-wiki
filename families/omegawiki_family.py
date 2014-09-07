# -*- coding: utf-8  -*-
"""Family module for Omega Wiki."""
__version__ = '$Id$'

import family


# Omegawiki, the Ultimate online dictionary
class Family(family.Family):

    """Family class for Omega Wiki."""

    def __init__(self):
        """Constructor."""
        family.Family.__init__(self)
        self.name = 'omegawiki'
        self.langs['omegawiki'] = 'www.omegawiki.org'

        self.namespaces[4] = {
            '_default': [u'Meta'],
        }
        self.namespaces[5] = {
            '_default': [u'Meta talk'],
        }
        self.namespaces[6] = {
            '_default': [u'File'],
        }
        self.namespaces[7] = {
            '_default': [u'File talk'],
        }
        self.namespaces[16] = {
            '_default': [u'Expression'],
        }
        self.namespaces[17] = {
            '_default': [u'Expression talk'],
        }
        self.namespaces[22] = {
            '_default': [u'Portal'],
        }
        self.namespaces[23] = {
            '_default': [u'Portal talk'],
        }
        self.namespaces[24] = {
            '_default': [u'DefinedMeaning'],
        }
        self.namespaces[25] = {
            '_default': [u'DefinedMeaning talk'],
        }
        self.namespaces[26] = {
            '_default': [u'Search'],
        }
        self.namespaces[27] = {
            '_default': [u'Search talk'],
        }
        self.namespaces[28] = {
            '_default': [u'NeedsTranslationTo'],
        }
        self.namespaces[29] = {
            '_default': [u'NeedsTranslationTo talk'],
        }
        self.namespaces[30] = {
            '_default': [u'Partner'],
        }
        self.namespaces[31] = {
            '_default': [u'Partner talk'],
        }

        # On most Wikipedias page names must start with a capital letter, but some
        # languages don't use this.

        self.nocapitalize = self.langs.keys()

    def hostname(self, code):
        """Return the hostname for this family."""
        return 'www.omegawiki.org'

    def version(self, code):
        """Return the version for this family."""
        return "1.22.6"

    def scriptpath(self, code):
        """Return the script path for this family."""
        return ''

    def nicepath(self, code):
        return '/'
