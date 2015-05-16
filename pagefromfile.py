#!/usr/bin/python
#coding: utf-8
"""
This bot takes its input from a file that contains a number of
pages to be put on the wiki. The pages should all have the same
begin and end text (which may not overlap).

By default the text should have the intended title of the page
as the first text in bold (that is, between ''' and '''),
you can modify this behavior with command line options.

The default is not to include the begin and
end text in the page, if you want to include that text, use
the -include option.

Specific arguments:
-start:xxx      Specify the text that marks the beginning of a page
-end:xxx        Specify the text that marks the end of a page
-file:xxx       Give the filename we are getting our material from
-include        The beginning and end markers should be included
                in the page.
-titlestart:xxx Use xxx in place of ''' for identifying the
                beginning of page title
-titleend:xxx   Use xxx in place of ''' for identifying the
                end of page title
-notitle        do not include the title, including titlestart, and
                titleend, in the page
-nocontent      If page has this statment it dosen't append
                (example: -nocontents:"{{infobox")
-summary:xxx    Use xxx as the edit summary for the upload - if
                a page exists, standard messages are appended
                after xxx for appending, prepending, or replacement
-autosummary    Use MediaWikis autosummary when creating a new page,
                overrides -summary in this case
-minor          set minor edit flag on page edits

If the page to be uploaded already exists:
-safe           do nothing (default)
-appendtop      add the text to the top of it
-appendbottom   add the text to the bottom of it
-force          overwrite the existing page
"""
#
# (C) Andre Engels, 2004
# (C) Pywikibot team, 2005-2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import re
import codecs
import pywikibot
import config
from pywikibot import i18n


class NoTitle(Exception):
    """No title found"""
    def __init__(self, offset):
        self.offset = offset


class PageFromFileRobot:
    """
    Responsible for writing pages to the wiki, with the titles and contents
    given by a PageFromFileReader.

    """

    def __init__(self, reader, force, append, summary, minor, autosummary,
                 dry, nocontents):
        self.reader = reader
        self.force = force
        self.append = append
        self.summary = summary
        self.minor = minor
        self.autosummary = autosummary
        self.dry = dry
        self.nocontent = nocontents

    def run(self):
        for title, contents in self.reader.run():
            self.put(title, contents)

    def put(self, title, contents):
        mysite = pywikibot.getSite()

        page = pywikibot.Page(mysite, title)
        # Show the title of the page we're working on.
        # Highlight the title in purple.
        pywikibot.output(u">>> \03{lightpurple}%s\03{default} <<<"
                         % page.title())

        if self.summary:
            comment = self.summary
        else:
            comment = i18n.twtranslate(mysite, 'pagefromfile-msg')

        comment_top = comment + " - " + i18n.twtranslate(
            mysite, 'pagefromfile-msg_top')
        comment_bottom = comment + " - " + i18n.twtranslate(
            mysite, 'pagefromfile-msg_bottom')
        comment_force = "%s *** %s ***" % (
            comment, i18n.twtranslate(mysite, 'pagefromfile-msg_force'))

        # Remove trailing newlines (cause troubles when creating redirects)
        contents = re.sub('^[\r\n]*', '', contents)

        if page.exists():
            if self.nocontent != u'':
                pagecontents = page.get()
                if pagecontents.find(self.nocontent) != -1 or pagecontents.find(self.nocontent.lower()) != -1:
                    pywikibot.output(u'Page has %s so it is skipped' % (self.nocontent))
                    return
            if self.append == "Top":
                pywikibot.output(u"Page %s already exists, appending on top!"
                                     % title)
                contents = contents + page.get()
                comment = comment_top
            elif self.append == "Bottom":
                pywikibot.output(u"Page %s already exists, appending on bottom!"
                                     % title)
                contents = page.get() + contents
                comment = comment_bottom
            elif self.force:
                pywikibot.output(u"Page %s already exists, ***overwriting!"
                                 % title)
                comment = comment_force
            else:
                pywikibot.output(u"Page %s already exists, not adding!" % title)
                return
        else:
            if self.autosummary:
                comment = ''
                pywikibot.setAction('')

        if self.dry:
            pywikibot.output(
                u"*** Dry mode ***\n"
                u"\03{lightpurple}title\03{default}: " + title + "\n"
                u"\03{lightpurple}contents\03{default}:\n" + contents + "\n"
                u"\03{lightpurple}comment\03{default}: " + comment + "\n")
            return

        try:
            page.put(contents, comment=comment, minorEdit=self.minor)
        except pywikibot.LockedPage:
            pywikibot.output(u"Page %s is locked; skipping." % title)
        except pywikibot.EditConflict:
            pywikibot.output(u'Skipping %s because of edit conflict' % title)
        except pywikibot.SpamfilterError, error:
            pywikibot.output(
                u'Cannot change %s because of spam blacklist entry %s'
                % (title, error.url))


class PageFromFileReader:
    """
    Responsible for reading the file.

    The run() method yields a (title, contents) tuple for each found page.
    """
    def __init__(self, filename, pageStartMarker, pageEndMarker,
                 titleStartMarker, titleEndMarker, include, notitle):
        self.filename = filename
        self.pageStartMarker = pageStartMarker
        self.pageEndMarker = pageEndMarker
        self.titleStartMarker = titleStartMarker
        self.titleEndMarker = titleEndMarker
        self.include = include
        self.notitle = notitle

    def run(self):
        pywikibot.output('Reading \'%s\'...' % self.filename)
        try:
            f = codecs.open(self.filename, 'r',
                            encoding=config.textfile_encoding)
        except IOError, err:
            print err
            return

        text = f.read()
        position = 0
        length = 0
        while True:
            try:
                length, title, contents = self.findpage(text[position:])
            except AttributeError:
                if not length:
                    pywikibot.output(u'\nStart or end marker not found.')
                else:
                    pywikibot.output(u'End of file.')
                break
            except NoTitle, err:
                pywikibot.output(u'\nNo title found - skipping a page.')
                position += err.offset
                continue

            position += length
            yield title, contents

    def findpage(self, text):
        pageR = re.compile(self.pageStartMarker + "(.*?)" + self.pageEndMarker,
                           re.DOTALL)
        titleR = re.compile(self.titleStartMarker + "(.*?)" +
                            self.titleEndMarker)

        location = pageR.search(text)
        if self.include:
            contents = location.group()
        else:
            contents = location.group(1)
        try:
            title = titleR.search(contents).group(1)
            if self.notitle:
                #Remove title (to allow creation of redirects)
                contents = titleR.sub('', contents, count=1)
        except AttributeError:
            raise NoTitle(location.end())
        else:
            return location.end(), title, contents


def main():
    # Adapt these to the file you are using. 'pageStartMarker' and
    # 'pageEndMarker' are the beginning and end of each entry. Take text that
    # should be included and does not occur elsewhere in the text.

    # TODO: make config variables for these.
    filename = "dict.txt"
    pageStartMarker = "{{-start-}}"
    pageEndMarker = "{{-stop-}}"
    titleStartMarker = u"'''"
    titleEndMarker = u"'''"
    nocontents = u""
    include = False
    force = False
    append = None
    notitle = False
    summary = None
    minor = False
    autosummary = False

    for arg in pywikibot.handleArgs():
        if arg.startswith("-start:"):
            pageStartMarker = arg[7:]
        elif arg.startswith("-end:"):
            pageEndMarker = arg[5:]
        elif arg.startswith("-file:"):
            filename = arg[6:]
        elif arg == "-include":
            include = True
        elif arg == "-appendtop":
            append = "Top"
        elif arg == "-appendbottom":
            append = "Bottom"
        elif arg == "-force":
            force = True
        elif arg == "-safe":
            force = False
            append = None
        elif arg == '-notitle':
            notitle = True
        elif arg == '-minor':
            minor = True
        elif arg.startswith('-nocontent:'):
            nocontents = arg[11:]
        elif arg.startswith("-titlestart:"):
            titleStartMarker = arg[12:]
        elif arg.startswith("-titleend:"):
            titleEndMarker = arg[10:]
        elif arg.startswith("-summary:"):
            summary = arg[9:]
        elif arg == '-autosummary':
            autosummary = True
        else:
            pywikibot.output(u"Disregarding unknown argument %s." % arg)

    reader = PageFromFileReader(filename, pageStartMarker, pageEndMarker,
                                titleStartMarker, titleEndMarker, include,
                                notitle)
    bot = PageFromFileRobot(reader, force, append, summary, minor, autosummary,
                            pywikibot.simulate, nocontents)
    bot.run()


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
