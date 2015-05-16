#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
\03{lightyellow}This bot renders statistics provided by [[Special:Statistics]] in a table on a wiki page.\03{default}
Thus it creates and updates a Statistics wikitable.

The following parameters are supported:

\03{lightred}-screen\03{default}     If True, doesn't do any changes, but only shows the statistics.

\03{lightgreen}-page\03{default}    On what page statistics are rendered.
        If not existing yet, it is created.
        If existing, it is updated.
"""
#
#
# (C) Pywikibot team, 2009-2013
#
# Distributed under the terms of the MIT license.
__version__ = '$Id$'
#

import time
import pywikibot
import query

# This is the title of the wikipage where to render stats.
your_page = "Logstats"

summary_update = {
    'en': u'Bot: Updating some statistics.',
}

summary_creation = {
    'en': u'Bot: Creating statistics log page.',
}


class StatisticsBot:

    def __init__(self, screen, your_page):
        """
        Constructor. Parameter:
            * screen    - If True, doesn't do any real changes, but only shows
                          some stats.
        """
        self.screen = screen
        self.your_page = your_page
        self.site = pywikibot.getSite()
        self.dict = self.getdata()  # Try to get data.

    def run(self):
        if self.screen:
            pywikibot.output("Bot is running to output stats.")
            self.idle(1)  # Run a function to idle
            self.outputall()
        if not self.screen:
            self.outputall()  # Output all datas on screen.
            pywikibot.output("\nBot is running. Going to treat "
                             "\03{lightpurple}%s\03{default}..."
                             % self.your_page)
            self.idle(2)
            self.treat()

    def getdata(self):
        # getdata() returns a dictionnary of the query to
        # api.php?action=query&meta=siteinfo&siprop=statistics
        # This method return data in a dictionnary format.
        # View data with:
        # api.php?action=query&meta=siteinfo&siprop=statistics&format=jsonfm
        params = {
        'action': 'query',
        'meta': 'siteinfo',
        'siprop': 'statistics',
        }
        pywikibot.output("\nQuerying api for json-formatted data...")
        data = None
        try:
            data = query.GetData(params, self.site)
        except:
            url = (self.site.protocol() + '://' + self.site.hostname() +
                   self.site.api_address())
            pywikibot.output("The query has failed. Have you check the API? "
                             "Cookies are working?")
            pywikibot.output(u"\n>> \03{lightpurple}%s\03{default} <<" % url)
        if data:
            pywikibot.output("Extracting statistics...")
            return data['query']['statistics']

    def treat(self):
            page = pywikibot.Page(self.site, self.your_page)
            if page.exists():
                pywikibot.output(
                    u'\nWikitable on \03{lightpurple}%s\03{default} will be '
                    u'completed with:\n' % self.your_page)
                text = page.get()
                newtext = self.newraw()
                pywikibot.output(newtext)
                choice = pywikibot.inputChoice(
                    u'Do you want to add these on wikitable?',
                    ['Yes', 'No'], ['y', 'N'], 'N')
                text = text[:-3] + newtext
                summ = pywikibot.translate(self.site, summary_update)
                if choice == 'y':
                    try:
                        page.put(u''.join(text), summ)
                    except:
                        pywikibot.output(u'Impossible to edit. It may be an '
                                         u'edit conflict. Skipping...')
            else:
                pywikibot.output(
                    u'\nWikitable on \03{lightpurple}%s\03{default} will be '
                    u'created with:\n' % self.your_page)
                newtext = self.newtable()+self.newraw()
                pywikibot.output(newtext)
                summ = pywikibot.translate(self.site, summary_creation)
                choice = pywikibot.inputChoice(
                    u'Do you want to accept this page creation?',
                    ['Yes', 'No'], ['y', 'N'], 'N')
                if choice == 'y':
                    try:
                        page.put(newtext, summ)
                    except pywikibot.LockedPage:
                        pywikibot.output(u"Page %s is locked; skipping."
                                         % title)
                    except pywikibot.EditConflict:
                        pywikibot.output(u'Skipping %s because of edit conflict'
                                         % title)
                    except pywikibot.SpamfilterError, error:
                        pywikibot.output(u'Cannot change %s because of spam '
                                         u'blacklist entry %s'
                                         % (title, error.url))

    def newraw(self):
        # new raw for date and stats
        newtext = ("\n|----\n!''" + self.date() + "''")
        for name in self.dict:
            newtext += '\n|' + str(abs(self.dict[name]))
        newtext += '\n|----\n|}'
        return newtext

    def newtable(self):
        # create table
        newtext = ('\n{| class=wikitable style=text-align:center\n!' + "date")
        for name in self.dict:
            newtext += '\n|'+name
        return newtext

    def date(self):
        return time.strftime('%Y/%m/%d', time.localtime(time.time()))

    def outputall(self):
        list = self.dict.keys()
        list.sort()
        for name in self.dict:
            pywikibot.output("There are " + str(self.dict[name]) + " " + name)

    def idle(self, retry_idle_time):
        time.sleep(retry_idle_time)
        pywikibot.output(u"Starting in %i second..." % retry_idle_time)
        time.sleep(retry_idle_time)


def main(your_page):
    screen = False  # If True do not edit the wiki, only output statistics
    _page = None

    pywikibot.output("\nBuilding the bot...")
    for arg in pywikibot.handleArgs():  # Parse command line arguments
        if arg.startswith('-page'):
            if len(arg) == 5:
                _page = pywikibot.input(
                    u'On what page do you want to add statistics?')
            else:
                _page = arg[6:]
        if arg.startswith("-screen"):
            screen = True
    if not _page:
        _page = your_page
        if not screen:
            pywikibot.output("The bot will add statistics on %s.\n" % _page)
    bot = StatisticsBot(screen, _page)  # Launch the instance of a StatisticsBot
    bot.run()  # Execute the 'run' method


if __name__ == "__main__":
    try:
        main(your_page)
    finally:
        pywikibot.stopme()
