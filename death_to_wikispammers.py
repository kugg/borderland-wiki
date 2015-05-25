#!/usr/bin/env python
# -*- coding: utf-8  -*-
##
# death_to_wikispammers.py - helps quickly delete spam in
# spuriously created userpages
###
"""death_to_wikispammers

Usage: death_to_wikispammers [username]
 Downloads a list of recently created users, starting at the username given.
 One by one, shows their user page via STDOUT.
 Delete user page and block for spam? it asks, [y/n]
 If yes, deletes user page, blocks user for spamming
 If no, goes onto next

"""

__version__ = "0.1"
__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

from pywikipediabot import wikipedia
from userlistpage import user_list_since_user

whitelist = ["Borderwiki", "Guff", "DanielH", "Mulvany", \
	     "Andreas", "Good News", "Blackbird", "Timorybak", \
	     "Maria", "Hest", "Tingfinder", "Secretary", \
	     "Fannyofdoom", "Mathias Gazze", "Mama Rabbit", \
	     "Nikolajmartini", u'Zak rlig', "Animalpaul", \
	     "KraFs", "Juliebm", "Gfgfs", "Mermaid"]
white_pages = ["Dreams", "Camps", \
	       "Survival Guide", "The Ten Principles", "The essentials", \
	       "Arriving The area", "The Clown Police", "The area", \
	       "Photography", "Leave No Trace", "Getting There", \
	       "Shopping 2", "Shopping", "Trixeldome", \
	       "Kakophonium", "Evil Mutant Overlord Cheap Wine Tasting", \
	       "DREAM_RADIO", u'Jrmungandr', "The_Borderland Sauna", \
	       "The center of information and misinformstion", "Earth", \
	       "The Shadowland", "HighBearNation", \
	       "The Rabbithole", "Queer Qlux Qlan", \
               "Frequently Asked Questions", \
               "Complete List of Important Things", "Danish Law", \
               "Use of Images", "Electricity", "Logo", "Getting There", \
               "Event Participation Agreement", "FAQ", "Mermaid camp"]
def main(args):
    noisebridge = wikipedia.Site('en')
    if len(args) > 0:
        lastUser = args[0]
    else:
        try:
            f = open("/tmp/death_to_wikispammers_last_spammer","r")
            lastUser = f.readline().strip()
            f.close()
        except IOError:
            lastUser = '3upiotr'

    users = user_list_since_user(noisebridge, lastUser).getUsers()
    
    for i in users:
	try:
            input_name = i.name()
	    ascii_name = input_name.encode('ascii', 'ignore')
        except:
	    print input_name
	    print type(input_name)
            print ascii_name
	    print type(ascii_name)
            raise

	if ascii_name in whitelist:
            print("Protected by whitelist: {}".format(ascii_name))
	    continue
	else:
            print("Not in whitelist: {}".format(ascii_name))

        hasContributions = False
        if i.isBlocked():
            continue
        try:
            m = i.contributions(limit=1).next()
            print "Last edit:", m
            hasContributions = True
        except StopIteration:
            pass
        #if hasContributions:
            #decision = raw_input("Spam? [y/N]")
            #if decision.upper() != "Y":
            #    continue
        print "Despamming"
        userpage_deleted = False
        for each_page in i.contributions():
            print each_page
            print each_page[0].title()
            title = each_page[0].title().encode('ascii', 'ignore')
            if each_page[0].title() in white_pages:
                print "Page is protected by whitepage filter."
                continue
            """Page [[en:User:Cynthia8890]] could not be deleted - it doesn't exist"""
            if title == "User:{}".format(ascii_name):
                if userpage_deleted:
                    continue
                else:
                    userpage_deleted = True
            each_page[0].delete("Spam (deleted by [Secretaribot] )",
                    prompt=False)
        i.block(reason="Spam: deleted by [Secretaribot]",
                expiry="infinite", onAutoblock=True,
                allowUsertalk=False, anon=False)
        f = open("/tmp/death_to_wikispammers_last_spammer","w")
        f.write(i.name())
        f.close()


import sys
import getopt


class Main():
    """ Encapsulates option handling. Subclass to add new options,
        add 'handle_x' method for an -x option,
        add 'handle_xlong' method for an --xlong option
        help (-h, --help) should be automatically created from module
        docstring and handler docstrings.
        test (-t, --test) will run all docstring and unittests it finds
        """
    class Usage(Exception):
        """ Use this to generate a Usage message """
        def __init__(self, msg):
            self.msg = msg

    def __init__(self):
        handlers = [i[7:] for i in dir(self) if i.startswith('handle_')]
        self.shortopts = ''.join([i for i in handlers if len(i) == 1])
        self.longopts = [i for i in handlers if (len(i) > 1)]

    def handler(self, option):
        i = 'handle_%s' % option.lstrip('-')
        if hasattr(self, i):
            return getattr(self, i)

    def default_main(self, args):
        print sys.argv[0], " called with ", args

    def handle_help(self, v):
        """ Shows this message """
        print sys.modules.get(__name__).__doc__
        descriptions = {}
        for i in list(self.shortopts) + self.longopts:
            d = self.handler(i).__doc__
            if d in descriptions:
                descriptions[d].append(i)
            else:
                descriptions[d] = [i]
        for d, opts in descriptions.iteritems():
            for i in opts:
                if len(i) == 1:
                    print '-%s' % i,
                else:
                    print '--%s' % i,
            print
            print d
        sys.exit(0)
    handle_h = handle_help

    def handle_test(self, v):
        """ Runs test suite for file """
        import doctest
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromModule(
                sys.modules.get(__name__))
        suite.addTest(doctest.DocTestSuite())
        runner = unittest.TextTestRunner()
        runner.run(suite)
        sys.exit(0)
    handle_t = handle_test

    def run(self, main=None, argv=None):
        """ Execute main function, having stripped out options and called the
        responsible handler functions within the class. Main defaults to
        listing the remaining arguments.
        """
        if not callable(main):
            main = self.default_main
        if argv is None:
            argv = sys.argv
        try:
            try:
                opts, args = getopt.getopt(argv[1:],
                                 self.shortopts, self.longopts)
            except getopt.error, msg:
                raise self.Usage(msg)
            for o, a in opts:
                (self.handler(o))(a)
            return main(args)
        except self.Usage, err:
            print >>sys.stderr, err.msg
            self.handle_help(None)
            return 2

if __name__ == "__main__":
    sys.exit(Main().run(main) or 0)
