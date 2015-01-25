#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
With this tool you can add the template {{commonscat}} to categories.

The tool works by following the interwiki links. If the template is present on
another language page, the bot will use it.

You could probably use it at articles as well, but this isn't tested.

This bot uses pagegenerators to get a list of pages. The following options are
supported:

&params;

-always           Don't prompt you for each replacement. Warning message
                  has not to be confirmed. ATTENTION: Use this with care!

-summary:XYZ      Set the action summary message for the edit to XYZ,
                  otherwise it uses messages from add_text.py as default.

-checkcurrent     Work on all category pages that use the primary commonscat
                  template.

For example to go through all categories:
commonscat.py -start:Category:!
"""
"""
Commonscat bot:

Take a page. Follow the interwiki's and look for the commonscat template
*Found zero templates. Done.
*Found one template. Add this template
*Found more templates. Ask the user <- still have to implement this

TODO:
*Update interwiki's at commons
*Collect all possibilities also if local wiki already has link.
*Better support for other templates (translations) / redundant templates.
*Check mode, only check pages which already have the template
*More efficient like interwiki.py
*Possibility to update other languages in the same run

"""

#
# (C) Multichill, 2008-2009
# (C) Xqt, 2009-2015
# (C) Pywikibot team, 2008-2015
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import re

import add_text
import wikipedia as pywikibot
import pagegenerators
from pywikibot import i18n

docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}

# Primary template, list of alternatives
# No entry needed if it is like _default
commonscatTemplates = {
    '_default': (u'Commonscat', []),
    'af': (u'CommonsKategorie', [u'commonscat']),
    'an': (u'Commonscat', [u'Commons cat']),
    'ar': (u'تصنيف كومنز',
           [u'Commonscat', u'تصنيف كومونز', u'Commons cat', u'CommonsCat']),
    'arz': (u'Commons cat', [u'Commoncat']),
    'az': (u'CommonsKat', [u'Commonscat']),
    'bn': (u'কমন্সক্যাট', [u'Commonscat']),
    'ca': (u'Commonscat', [u'Commons cat', u'Commons category']),
    'crh': (u'CommonsKat', [u'Commonscat']),
    'cs': (u'Commonscat', [u'Commons cat']),
    'da': (u'Commonscat',
           [u'Commons cat', u'Commons category', u'Commonscat left',
            u'Commonscat2']),
    'en': (u'Commons category',
           [u'Commoncat', u'Commonscat', u'Commons cat', u'Commons+cat',
            u'Commonscategory', u'Commons and category', u'Commonscat-inline',
            u'Commons category-inline', u'Commons2', u'Commons category multi',
            u'Cms-catlist-up', u'Catlst commons', u'Commonscat show2',
            u'Sister project links']),
    'es': (u'Commonscat',
           [u'Ccat', u'Commons cat', u'Categoría Commons',
            u'Commonscat-inline']),
    'et': (u'Commonsi kategooria',
           [u'Commonscat', u'Commonskat', u'Commons cat', u'Commons category']),
    'eu': (u'Commonskat', [u'Commonscat']),
    'fa': (u'ویکی‌انبار-رده',
           [u'Commonscat', u'Commons cat', u'انبار رده', u'Commons category',
            u'انبار-رده', u'جعبه پیوند به پروژه‌های خواهر',
            u'در پروژه‌های خواهر', u'پروژه‌های خواهر']),
    'fr': (u'Commonscat', [u'CommonsCat', u'Commons cat', u'Commons category']),
    'frp': (u'Commonscat', [u'CommonsCat']),
    'ga': (u'Catcómhaoin', [u'Commonscat']),
    'he': (u'ויקישיתוף בשורה', []),
    'hi': (u'Commonscat', [u'Commons2', u'Commons cat', u'Commons category']),
    'hu': (u'Commonskat', [u'Közvagyonkat']),
    'hy': (u'Վիքիպահեստ կատեգորիա',
           [u'Commonscat', u'Commons cat', u'Commons category']),
    'id': (u'Commonscat',
           [u'Commons cat', u'Commons2', u'CommonsCat', u'Commons category']),
    'is': (u'CommonsCat', [u'Commonscat']),
    'ja': (u'Commonscat', [u'Commons cat', u'Commons category']),
    'jv': (u'Commonscat', [u'Commons cat']),
    'kaa': (u'Commons cat', [u'Commonscat']),
    'kk': (u'Commonscat', [u'Commons2']),
    'ko': (u'Commonscat', [u'Commons cat', u'공용분류']),
    'la': (u'CommuniaCat', []),
    'mk': (u'Ризница-врска',
           [u'Commonscat', u'Commons cat', u'CommonsCat', u'Commons2',
            u'Commons category']),
    'ml': (u'Commonscat', [u'Commons cat', u'Commons2']),
    'ms': (u'Kategori Commons', [u'Commonscat', u'Commons category']),
    'nn': (u'Commonscat', [u'Commons cat']),
    'os': (u'Commonscat', [u'Commons cat']),
    'pt': (u'Commonscat', [u'Commons cat']),
    'ro': (u'Commonscat', [u'Commons cat']),
    'ru': (u'Commonscat', [u'Викисклад-кат', u'Commons category']),
    'simple': (u'Commonscat',
               [u'Commons cat',  u'Commons cat multi', u'Commons category',
                u'Commons category multi', u'CommonsCompact',
                u'Commons-inline']),
    'sh': (u'Commonscat', [u'Commons cat']),
    'sl': (u'Kategorija v Zbirki',
           [u'Commonscat', u'Kategorija v zbirki', u'Commons cat',
            u'Katzbirke']),
    'sv': (u'Commonscat',
           [u'Commonscat-rad', u'Commonskat', u'Commons cat', u'Commonscatbox',
            u'Commonscat-box']),
    'sw': (u'Commonscat', [u'Commons2', u'Commons cat']),
    'te': (u'Commonscat', [u'Commons cat']),
    'tr': (u'Commons kategori',
           [u'CommonsKat', u'Commonscat', u'Commons cat']),
    'uk': (u'Commonscat', [u'Commons cat', u'Category', u'Commonscat-inline']),
    'vi': (u'Commonscat',
           [u'Commons2', u'Commons cat', u'Commons category', u'Commons+cat']),
    'zh': (u'Commonscat', [u'Commons cat', u'Commons category']),
    'zh-classical': (u'共享類', [u'Commonscat']),
    'zh-yue': (u'同享類',
               [u'Commonscat', u'共享類 ', u'Commons cat', u'Commons category']),
}

ignoreTemplates = {
    'af': [u'commons'],
    'ar': [u'تحويلة تصنيف', u'كومنز', u'كومونز', u'Commons'],
    'be-x-old': [u'Commons', u'Commons category'],
    'cs': [u'Commons', u'Sestřičky', u'Sisterlinks'],
    'da': [u'Commons', u'Commons left', u'Commons2', u'Commonsbilleder',
           u'Commonskat', u'Commonscat2', u'GalleriCommons', u'Søsterlinks'],
    'de': [u'Commons', u'ZhSZV', u'Bauwerk-stil-kategorien',
           u'Bauwerk-funktion-kategorien', u'KsPuB',
           u'Kategoriesystem Augsburg-Infoleiste',
           u'Kategorie Ge', u'Kategorie v. Chr. Ge',
           u'Kategorie Geboren nach Jh. v. Chr.', u'Kategorie Geboren nach Jh.',
           u'!Kategorie Gestorben nach Jh. v. Chr.',
           u'!Kategorie Gestorben nach Jh.',
           u'Kategorie Jahr', u'Kategorie Jahr v. Chr.',
           u'Kategorie Jahrzehnt', u'Kategorie Jahrzehnt v. Chr.',
           u'Kategorie Jahrhundert', u'Kategorie Jahrhundert v. Chr.',
           u'Kategorie Jahrtausend', u'Kategorie Jahrtausend v. Chr.'],
    'en': [u'Category redirect', u'Commons', u'Commonscat1A', u'Commoncats',
           u'Commonscat4Ra',
           u'Sisterlinks', u'Sisterlinkswp', u'Sister project links',
           u'Tracking category', u'Template category', u'Wikipedia category'],
    'eo': [u'Commons',
           (u'Projekto/box', 'commons='),
           (u'Projekto', 'commons='),
           (u'Projektoj', 'commons='),
           (u'Projektoj', 'commonscat=')],
    'es': [u'Commons', u'IprCommonscat'],
    'eu': [u'Commons'],
    'fa': [u'Commons', u'ویکی‌انبار', u'Category redirect', u'رده بهتر',
           u'جعبه پیوند به پروژه‌های خواهر', u'در پروژه‌های خواهر',
           u'پروژه‌های خواهر'],
    'fi': [u'Commonscat-rivi', u'Commons-rivi', u'Commons'],
    'fr': [u'Commons', u'Commons-inline', (u'Autres projets', 'commons=')],
    'fy': [u'Commons', u'CommonsLyts'],
    'he': [u'מיזמים'],
    'hr': [u'Commons', (u'WProjekti', 'commonscat=')],
    'is': [u'Systurverkefni', u'Commons'],
    'it': [(u'Ip', 'commons='), (u'Interprogetto', 'commons=')],
    'ja': [u'CommonscatS', u'SisterlinksN', u'Interwikicat'],
    'ms': [u'Commons', u'Sisterlinks', u'Commons cat show2'],
    'nds-nl': [u'Commons'],
    'nl': [u'Commons', u'Commonsklein', u'Commonscatklein', u'Catbeg',
           u'Catsjab', u'Catwiki'],
    'om': [u'Commons'],
    'pt': [u'Correlatos',
           u'Commons',
           u'Commons cat multi',
           u'Commons1',
           u'Commons2'],
    'simple': [u'Sisterlinks'],
    'ru': [u'Навигация', u'Навигация для категорий', u'КПР', u'КБР',
           u'Годы в России', u'commonscat-inline'],
    'tt': [u'Навигация'],
    'zh': [u'Category redirect', u'cr', u'Commons',
           u'Sisterlinks', u'Sisterlinkswp',
           u'Tracking category', u'Trackingcatu',
           u'Template category', u'Wikipedia category'
           u'分类重定向', u'追蹤分類', u'共享資源', u'追蹤分類'],
}


class CommonscatBot:

    """Commons categorisation bot."""

    def __init__(self, generator, always, summary=None):
        self.generator = generator
        self.always = always
        self.summary = summary
        self.site = pywikibot.getSite()

    def run(self):
        for page in self.generator:
            self.treat(page)

    def treat(self, page):
        """ Load the given page, do some changes, and save it. """
        if not page.exists():
            pywikibot.output(u'Page %s does not exist. Skipping.'
                             % page.title(asLink=True))
        elif page.isRedirectPage():
            pywikibot.output(u'Page %s is a redirect. Skipping.'
                             % page.title(asLink=True))
        elif page.isCategoryRedirect():
            pywikibot.output(u'Page %s is a category redirect. Skipping.'
                             % page.title(asLink=True))
        elif page.isDisambig():
            pywikibot.output(u'Page %s is a disambiguation. Skipping.'
                             % page.title(asLink=True))
        else:
            (status, always) = self.addCommonscat(page)
        return

    def save(self, text, page, comment, minorEdit=True, botflag=True):
        # only save if something was changed
        if text != page.get():
            # Show the title of the page we're working on.
            # Highlight the title in purple.
            pywikibot.output(u"\n\n>>> \03{lightpurple}%s\03{default} <<<"
                             % page.title())
            # show what was changed
            pywikibot.showDiff(page.get(), text)
            pywikibot.output(u'Comment: %s' % comment)
            if not self.always:
                choice = pywikibot.inputChoice(
                    u'Do you want to accept these changes?',
                    ['Yes', 'No', 'Always', 'Quit'],
                    ['y', 'N', 'a', 'q'], 'N')
                if choice == 'a':
                    self.always = True
                elif choice == 'q':
                    import sys
                    sys.exit()
            if self.always or choice == 'y':
                try:
                    # Save the page
                    page.put(text, comment=comment,
                             minorEdit=minorEdit, botflag=botflag)
                except pywikibot.LockedPage:
                    pywikibot.output(u"Page %s is locked; skipping."
                                     % page.title(asLink=True))
                except pywikibot.EditConflict:
                    pywikibot.output(
                        u'Skipping %s because of edit conflict'
                        % (page.title()))
                except pywikibot.SpamfilterError, error:
                    pywikibot.output(
                        u'Cannot change %s because of spam blacklist entry %s'
                        % (page.title(), error.url))
                else:
                    return True
        return False

    @classmethod
    def getCommonscatTemplate(cls, code=None):
        """Get the template name of a site. Expects the site code.

        Return as tuple containing the primary template and its alternatives.

        """
        if code in commonscatTemplates:
            return commonscatTemplates[code]
        else:
            return commonscatTemplates[u'_default']

    def skipPage(self, page):
        """Determine if the page should be skipped."""
        if page.site.code in ignoreTemplates:
            templatesInThePage = page.templates()
            templatesWithParams = page.templatesWithParams()
            for template in ignoreTemplates[page.site.code]:
                if not isinstance(template, tuple):
                    if template in templatesInThePage:
                        return True
                else:
                    for (inPageTemplate, param) in templatesWithParams:
                        if inPageTemplate == template[0] \
                           and template[1] in param[0].replace(' ', ''):
                            return True
        return False

    def updateInterwiki(self, wikipediaPage=None, commonsPage=None):
        """Update the interwiki's at commons from a wikipedia page. The bot just
        replaces the interwiki links at the commons page with the interwiki's
        from the wikipedia page. This should probably be more intelligent. We
        could use add all the interwiki's and remove duplicates. Or only remove
        language links if multiple language links to the same language exist.

        This function is disabled for the moment until i figure out what the
        best way is to update the interwiki's.

        """
        interwikis = {}
        comment = u''
        interwikilist = wikipediaPage.interwiki()
        interwikilist.append(wikipediaPage)

        for interwikiPage in interwikilist:
            interwikis[interwikiPage.site()] = interwikiPage
        oldtext = commonsPage.get()
        # The commonssite object doesnt work with interwiki's
        newtext = pywikibot.replaceLanguageLinks(oldtext, interwikis,
                                                 pywikibot.getSite(u'nl'))
        comment = u'Updating interwiki\'s from [[%s:%s]]' \
                  % (wikipediaPage.site.lang, wikipediaPage.title())

        if newtext != oldtext:
            #This doesnt seem to work. Newtext has some trailing whitespace
            pywikibot.showDiff(oldtext, newtext)
            commonsPage.put(newtext=newtext, comment=comment)

    def addCommonscat(self, page):
        """
        Add CommonsCat template to page.

        Take a page. Go to all the interwiki page looking for a commonscat
        template. When all the interwiki's links are checked and a proper
        category is found add it to the page.

        """
        pywikibot.output(u'Working on ' + page.title())
        # Get the right templates for this page
        primaryCommonscat, commonscatAlternatives = self.getCommonscatTemplate(
            page.site.code)
        commonscatLink = self.getCommonscatLink(page)
        if commonscatLink:
            pywikibot.output(u'Commonscat template is already on %s'
                             % page.title())
            (currentCommonscatTemplate,
             currentCommonscatTarget, LinkText, Note) = commonscatLink
            checkedCommonscatTarget = self.checkCommonscatLink(
                currentCommonscatTarget)
            if (currentCommonscatTarget == checkedCommonscatTarget):
                # The current commonscat link is good
                pywikibot.output(u'Commonscat link at %s to Category:%s is ok'
                                 % (page.title(), currentCommonscatTarget))
                return (True, self.always)
            elif checkedCommonscatTarget != u'':
                # We have a new Commonscat link, replace the old one
                self.changeCommonscat(page, currentCommonscatTemplate,
                                      currentCommonscatTarget,
                                      primaryCommonscat,
                                      checkedCommonscatTarget, LinkText, Note)
                return (True, self.always)
            else:
                # Commonscat link is wrong
                commonscatLink = self.findCommonscatLink(page)
                if (commonscatLink != u''):
                    self.changeCommonscat(page, currentCommonscatTemplate,
                                          currentCommonscatTarget,
                                          primaryCommonscat, commonscatLink)
                # TODO: if the commonsLink == u'', should it be removed?

        elif self.skipPage(page):
            pywikibot.output("Found a template in the skip list. Skipping %s"
                             % page.title())
        else:
            commonscatLink = self.findCommonscatLink(page)
            if (commonscatLink != u''):
                if commonscatLink == page.title():
                    textToAdd = u'{{%s}}' % primaryCommonscat
                else:
                    textToAdd = u'{{%s|%s}}' % (primaryCommonscat,
                                                commonscatLink)
                (success, status, self.always) = add_text.add_text(page,
                                                                   textToAdd,
                                                                   self.summary,
                                                                   None, None,
                                                                   self.always)
                return (True, self.always)
        return (True, self.always)

    def changeCommonscat(self, page=None, oldtemplate=u'', oldcat=u'',
                         newtemplate=u'', newcat=u'', linktitle=u'',
                         description=u''):
        """ Change the current commonscat template and target. """
        if oldcat == '3=S' or linktitle == '3=S':
            return  # TODO: handle additional param on de-wiki
        if not linktitle and (page.title().lower() in oldcat.lower() or
                              oldcat.lower() in page.title().lower()):
            linktitle = oldcat
        if linktitle and newcat != page.title(withNamespace=False):
            newtext = re.sub(u'(?i)\{\{%s\|?[^{}]*(?:\{\{.*\}\})?\}\}'
                             % oldtemplate,
                             u'{{%s|%s|%s}}' % (newtemplate, newcat, linktitle),
                             page.get())
        elif newcat == page.title(withNamespace=False):
            newtext = re.sub(u'(?i)\{\{%s\|?[^{}]*(?:\{\{.*\}\})?\}\}'
                             % oldtemplate,
                             u'{{%s}}' % newtemplate,
                             page.get())
        elif oldcat.strip() != newcat:  # strip trailing white space
            newtext = re.sub(u'(?i)\{\{%s\|?[^{}]*(?:\{\{.*\}\})?\}\}'
                             % oldtemplate,
                             u'{{%s|%s}}' % (newtemplate, newcat),
                             page.get())
        else:  # nothing left to do
            return
        if self.summary:
            comment = self.summary
        else:
            comment = i18n.twtranslate(page.site.code,
                                       'commonscat-msg_change',
                                       {'oldcat': oldcat, 'newcat': newcat})
        self.save(newtext, page, comment)

    def findCommonscatLink(self, page=None):
        """Find CommonsCat template on interwiki pages."""
        for ipage in page.interwiki():
            try:
                if(not ipage.exists() or ipage.isRedirectPage()
                   or ipage.isDisambig()):
                    continue
                commonscatLink = self.getCommonscatLink(ipage)
                if not commonscatLink:
                    continue
                (currentTemplate,
                 possibleCommonscat, linkText, Note) = commonscatLink
                checkedCommonscat = self.checkCommonscatLink(possibleCommonscat)
                if (checkedCommonscat != u''):
                    pywikibot.output(
                        u"Found link for %s at [[%s:%s]] to %s."
                        % (page.title(), ipage.site.code,
                           ipage.title(), checkedCommonscat))
                    return checkedCommonscat
            except pywikibot.BadTitle:
                # The interwiki was incorrect
                return u''
        return u''

    def getCommonscatLink(self, wikipediaPage=None):
        """Find CommonsCat template on page.

        @rtype: tuple of (<templatename>, <target>, <linktext>, <note>)
        """
        primaryCommonscat, commonscatAlternatives = self.getCommonscatTemplate(
            wikipediaPage.site.code)
        commonscatTemplate = u''
        commonscatTarget = u''
        commonscatLinktext = u''
        commonscatNote = u''
        # See if commonscat is present
        for template in wikipediaPage.templatesWithParams():
            if template[0] == primaryCommonscat \
               or template[0] in commonscatAlternatives:
                commonscatTemplate = template[0]
                if (len(template[1]) > 0):
                    commonscatTarget = template[1][0]
                    if len(template[1]) > 1:
                        commonscatLinktext = template[1][1]
                    if len(template[1]) > 2:
                        commonscatNote = template[1][2]
                else:
                    commonscatTarget = wikipediaPage.title(withNamespace=False)
                return (commonscatTemplate, commonscatTarget,
                        commonscatLinktext, commonscatNote)
        return None

    def checkCommonscatLink(self, name=""):
        """ Return the name of a valid commons category.

        If the page is a redirect this function tries to follow it.
        If the page doesn't exists the function will return an empty string

        """
        if pywikibot.verbose:
            pywikibot.output("getCommonscat: " + name)
        try:
            commonsSite = self.site.image_repository()
            # This can throw a pywikibot.BadTitle
            commonsPage = pywikibot.Page(commonsSite, "Category:" + name)

            if not commonsPage.exists():
                logpages = commonsSite.logpages(mode='delete',
                                                title=commonsPage.title())
                try:
                    logitem = logpages.next()
                    (logpage, loguser, logtimestamp, logcomment) = logitem
                    # Some logic to extract the target page.
                    regex = u'moved to \[\[\:?Category:(?P<newcat1>[^\|\}]+)(\|[^\}]+)?\]\]|Robot: Changing Category:(.+) to Category:(?P<newcat2>.+)'
                    m = re.search(regex, logcomment, flags=re.I)
                    if m:
                        if m.group('newcat1'):
                            return self.checkCommonscatLink(m.group('newcat1'))
                        elif m.group('newcat2'):
                            return self.checkCommonscatLink(m.group('newcat2'))
                    else:
                        pywikibot.output(
                            u'getCommonscat: %s deleted by %s. Couldn\'t find '
                            u'move target in "%s"'
                            % (commonsPage, loguser, logcomment))
                        return u''
                except StopIteration:
                    if pywikibot.verbose:
                        pywikibot.output(
                            u"getCommonscat: The category doesnt exist and "
                            u"nothing found in the deletion log.")
                    return u''
            elif commonsPage.isRedirectPage():
                if pywikibot.verbose:
                    pywikibot.output(
                        u"getCommonscat: The category is a redirect")
                return self.checkCommonscatLink(
                    commonsPage.getRedirectTarget().title(withNamespace=False))
            elif "Category redirect" in commonsPage.templates():
                if pywikibot.verbose:
                    pywikibot.output(
                        u"getCommonscat: The category is a category redirect")
                for template in commonsPage.templatesWithParams():
                    if (template[0] == "Category redirect" and
                            len(template[1]) > 0):
                        return self.checkCommonscatLink(template[1][0])
            elif commonsPage.isDisambig():
                if pywikibot.verbose:
                    pywikibot.output(
                        u"getCommonscat: The category is disambiguation")
                return u''
            else:
                return commonsPage.title(withNamespace=False)
        except pywikibot.BadTitle:
            # Funky title so not correct
            return u''
        except pywikibot.PageNotFound:
            return u''


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    summary = None
    generator = None
    always = False
    ns = []
    ns.append(14)

    # Process global args and prepare generator args parser

    genFactory = pagegenerators.GeneratorFactory()

    for arg in pywikibot.handleArgs(*args):
        if arg.startswith('-summary'):
            if len(arg) == 8:
                summary = pywikibot.input(u'What summary do you want to use?')
            else:
                summary = arg[9:]
        elif arg.startswith('-checkcurrent'):
            primaryCommonscat, commonscatAlternatives = \
                CommonscatBot.getCommonscatTemplate(
                    pywikibot.getSite().language())
            generator = pagegenerators.NamespaceFilterPageGenerator(
                pagegenerators.ReferringPageGenerator(
                    pywikibot.Page(pywikibot.getSite(),
                                   u'Template:' + primaryCommonscat),
                    onlyTemplateInclusion=True), ns)

        elif arg == '-always':
            always = True
        else:
            genFactory.handleArg(arg)

    if not generator:
        generator = genFactory.getCombinedGenerator()

    if generator:
        pregenerator = pagegenerators.PreloadingGenerator(generator)
        bot = CommonscatBot(pregenerator, always, summary)
        bot.run()
    else:
        pywikibot.showHelp()


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
