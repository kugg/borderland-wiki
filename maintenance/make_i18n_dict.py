# -*- coding: utf-8  -*-
"""
Generate a i18n file from a given script

usage:

run IDLE
>>> from make_i18n_dict import i18nBot
>>> bot = i18nBot('<scriptname>', '<msg dict>')
>>> bot.run()

If you have more than one message dictionary, give all these names to the bot:
>>> bot = i18nBot('<scriptname>', '<msg dict1>', '<msg dict2>', '<msg dict3>')

If you have the messages as instance constants you may call the bot as follows:
>>> bot = i18nBot('<scriptname>.<class instance>', '<msg dict1>', '<msg dict2>')

It's also possible to make json files too by using to_json method:
>>> from make_i18n_dict import i18nBot
>>> bot = i18nBot('disambredir', 'msg')
>>> bot.to_json()
"""
#
# (C) xqt 2013
# (C) Pywikipedia bot team, 2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#
import os
import json
import codecs
import sys
sys.path.insert(1, '..')

from pywikibot import config


class i18nBot(object):

    def __init__(self, script, *args):
        modules = script.split('.')
        self.scriptname = modules[0]

        self.script = __import__(self.scriptname, modules[1:])
        if len(modules) == 2 and hasattr(self.script, modules[1]):
            self.script = getattr(self.script, modules[1])
        self.messages = list()
        for msg in args:
            if hasattr(self.script, msg):
                self.messages.append(msg)
        self.messages.sort()
        self.dict = dict()

    def print_all(self):
        keys = self.dict.keys()
        keys.sort()
        print "msg = {"
        for code in keys:
            print " " * 8 + "'%s': {" % code
            for msg in self.messages:
                label = "%s-%s" % (self.scriptname, msg)
                if label in self.dict[code]:
                    print " " * 16 + "'%s': u'%s'," \
                          % (label, self.dict[code][label])
            print " " * 8 + "},"
        print "}"

    def read(self, item):
        msg = getattr(self.script, item)
        self.keys = msg.keys()
        self.keys.append('qqq')
        self.keys.sort()
        for code in self.keys:
            label = "%s-%s" % (self.scriptname, item)
            if code == 'qqq':
                if code not in self.dict:
                    self.dict[code] = {}
                self.dict[code][label] = \
                    u'Edit summary for %s report' % self.scriptname
            elif code != 'commons':
                if code not in self.dict:
                    self.dict[code] = {}
                self.dict[code][label] = msg[code]

    def run(self):
        for msg in self.messages:
            self.read(msg)
        self.print_all()

    def to_json(self):
        if not self.dict:
            self.run()
        json_dir = os.path.join(
            config.base_dir, 'i18n', self.scriptname)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        for lang in self.dict:
            file_name = os.path.join(json_dir, '%s.json' % lang)
            if os.path.isfile(file_name):
                with codecs.open(file_name, 'r', 'utf-8') as json_file:
                    new_dict = json.loads(json_file.read())
            else:
                new_dict = {}
            new_dict['@metadata'] = new_dict.get('@metadata', {'authors': []})
            with codecs.open(file_name, 'w', 'utf-8') as json_file:
                new_dict.update(self.dict[lang])
                json.dump(new_dict, json_file, ensure_ascii=False,
                          sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    print __doc__
