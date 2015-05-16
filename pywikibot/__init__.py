# -*- coding: utf-8  -*-
"""
The initialization file for the Pywikibot framework.

wikipedia.py will monkey-patch this module to look completely
alike wikipedia itself...
"""
#
# (C) Pywikipedia bot team, 2010-2013
#
# Distributed under the terms of the MIT license.
#
__release__ = '1.0b1'
__version__ = '$Id$'

try:
    import wikipedia
except Exception, e:
    print e
    print u'Serious import error; pywikibot not available - was it configured?'
