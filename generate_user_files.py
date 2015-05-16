# -*- coding: utf-8  -*-
"""Script to create user files (user-config.py, user-fixes.py)."""
#
# (C) Pywikibot team, 2008-2015
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import codecs
import os
import re
import sys

console_encoding = sys.stdout.encoding

if console_encoding is None or sys.platform == 'cygwin':
    console_encoding = "iso-8859-1"


def listchoice(clist=[], message=None, default=None):

    if not message:
        message = "Select"

    if default:
        message += " (default: %s)" % default

    message += ": "

    for n, i in enumerate(clist):
        print ("%d: %s" % (n + 1, i))

    while True:
        choice = raw_input(message)
        if choice == '' and default:
            return default
        try:
            choice = int(choice)
        except ValueError:
            pass
        if isinstance(choice, basestring):
            if choice not in clist:
                print("Invalid response")
            else:
                return choice
        try:
            return clist[int(choice) - 1]
        except:
            if not isinstance(choice, basestring):
                print("Invalid response")
    return response


def file_exists(filename):
    """Return whether the file exists and print a message if it exists."""
    if os.path.exists(filename):
        print("'%s' already exists." % filename)
        return True
    return False


def create_user_config(base_dir):
    _fnc = os.path.join(base_dir, "user-config.py")
    if not file_exists(_fnc):
        known_families = re.findall(r'(.+)_family.py\b',
                                    '\n'.join(os.listdir(
                                        os.path.join(base_dir, "families"))))
        fam = listchoice(known_families,
                         "Select family of sites we are working on, " \
                         "just enter the number not name",
                         default='wikipedia')
        codesds = codecs.open("families/%s_family.py"
                              % fam, "r", "utf-8").read()
        rre = re.compile("self\.languages\_by\_size *\= *(.+?)\]", re.DOTALL)
        known_langs = []
        if not rre.findall(codesds):
            rre = re.compile("self\.langs *\= *(.+?)\}", re.DOTALL)
            if rre.findall(codesds):
                import ast
                known_langs = ast.literal_eval(
                    rre.findall(codesds)[0] + u"}").keys()
        else:
            known_langs = eval(rre.findall(codesds)[0] + u"]")
        print "This is the list of known language(s):"
        print " ".join(sorted(known_langs))
        mylang = raw_input(
            "The language code of the site we're working on (default: 'en'): "
        ) or 'en'
        username = raw_input("Username (%s %s): "
                             % (mylang, fam)) or 'UnnamedBot'
        username = unicode(username, console_encoding)
        while True:
            choice = raw_input(
                "Which variant of user_config.py:\n"
                "[S]mall or [E]xtended (with further information)? ").upper()
            if choice in "SE":
                break

        #
        # I don't like this solution. Temporary for me.
        #
        f = codecs.open(os.path.join(base_dir, "config.py"), "r", "utf-8")
        cpy = f.read()
        f.close()

        res = re.findall("^(############## (?:LOGFILE|"
                                            "INTERWIKI|"
                                            "SOLVE_DISAMBIGUATION|"
                                            "IMAGE RELATED|"
                                            "TABLE CONVERSION BOT|"
                                            "WEBLINK CHECKER|"
                                            "DATABASE|"
                                            "SEARCH ENGINE|"
                                            "COPYRIGHT|"
                                            "FURTHER) SETTINGS .*?)^(?=#####|# =====)",
                         cpy, re.MULTILINE | re.DOTALL)
        config_text = '\n'.join(res)

        f = codecs.open(_fnc, "w", "utf-8")
        if choice == 'E':
            f.write("""# -*- coding: utf-8  -*-

# This is an automatically generated file. You can find more configuration
# parameters in 'config.py' file.

# The family of sites we are working on. wikipedia.py will import
# families/xxx_family.py so if you want to change this variable,
# you need to write such a file.
family = '%s'

# The language code of the site we're working on.
mylang = '%s'

# The dictionary usernames should contain a username for each site where you
# have a bot account.
usernames['%s']['%s'] = u'%s'


%s""" % (fam, mylang, fam, mylang, username, config_text))
        else:
            f.write("""# -*- coding: utf-8  -*-
family = '%s'
mylang = '%s'
usernames['%s']['%s'] = u'%s'
""" % (fam, mylang, fam, mylang, username))
        f.close()
        print("'%s' written." % _fnc)


def create_user_fixes(base_dir):
    """Create a basic user-fixes.py in base_dir."""
    _fnf = os.path.join(base_dir, "user-fixes.py")
    if not file_exists(_fnf):
        with codecs.open(_fnf, "w", "utf-8") as f:
            f.write(r"""# -*- coding: utf-8  -*-

#
# This is only an example. Don't use it.
#

fixes['example'] = {
    'regex': True,
    'msg': {
        '_default': u'no summary specified',
    },
    'replacements': [
        (ur'\bword\b', u'two words'),
    ]
}

""")
        print("'%s' written." % _fnf)


if __name__ == "__main__":
    print("1: Create user_config.py file (required)")
    print("2: Create user_fixes.py file (optional, for advanced usage)")
    print("3: The two files")
    choice = raw_input("What do you do? Just enter the number: ")
    if choice == "1":
        create_user_config('')
    if choice == "2":
        create_user_fixes('')
    if choice == "3":
        create_user_config('')
        create_user_fixes('')
    if choice not in "123":
        print("Nothing to do")
