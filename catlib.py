#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Library to work with category pages on Wikipedia
"""
#
# (C) Rob W.W. Hooft, Andre Engels, 2004-2007
# (C) Daniel Herding, 2004-2007
# (C) Russell Blau, 2005
# (C) Cyde Weys, 2005-2007
# (C) Leonardo Gregianin, 2005-2007
# (C) Pywikipedia bot team, 2007-2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#
import re
import urllib
import wikipedia as pywikibot
import query

msg_created_for_renaming = {
    'ar': u'روبوت: نقل من %s. المؤلفون: %s',
    'da': u'Bot: flytter fra %s. Bidragsydere: %s',
    'de': u'Bot: Verschoben von %s. Autoren: %s',
    'en': u'Robot: Moved from %s. Authors: %s',
    'es': u'Bot: Traslado desde %s. Autores: %s',
    'fa': u'ربات: انتقال از %s. نویسندگان: %s',
    'fi': u'Botti siirsi luokan %s. Muokkaajat: %s',
    'fr': u'Robot : déplacé depuis %s. Auteurs: %s',
    'he': u'בוט: הועבר מהשם %s. כותבים: %s',
    'hu': u'Bottal áthelyezve innen: %s. Eredeti szerzők: %s',
    'ia': u'Robot: Transferite de %s. Autores: %s',
    'id': u'Bot: Memindahkan dari %s. Kontributor: %s',
    'it': u'Bot: Voce spostata da %s. Autori: %s',
    'ja': u'ロボットによる: %s から移動しました。原作者は %s',
    'ksh': u'Bot: hääjeholldt von %s. Schriiver: %s',
    'nds': u'Kat-Bot: herschaven von %s. Schriever: %s',
    'nl': u'Bot: hernoemd van %s. Auteurs: %s',
    'nn': u'robot: flytta frå %s. Bidragsytarar: %s',
    'no': u'Bot: Flytta fra %s. Bidragsytere: %s',
    'pl': u'Robot przenosi z %s. Autorzy: %s',
    'pt': u'Bot: Movido de %s. Autor: %s',
    'zh': u'機器人: 已從 %s 移動。原作者是 %s',
}

# some constants that are used internally
ARTICLE = 0
SUBCATEGORY = 1


def isCatTitle(title, site):
    return ':' in title and title[:title.index(':')
                                  ] in site.category_namespaces()


def unique(l):
    """Given a list of hashable object, return an alphabetized unique list."""
    l = dict.fromkeys(l).keys()
    l.sort()
    return l


class Category(pywikibot.Page):
    """Subclass of Page that has some special tricks that only work for
    category: pages

    """

    def __init__(self, site, title=None, insite=None, sortKey=None,
                 sortKeyPrefix=None):
        pywikibot.Page.__init__(self, site=site, title=title, insite=insite,
                                defaultNamespace=14)
        self.sortKey = sortKey
        self.sortKeyPrefix = sortKeyPrefix
        if self.namespace() != 14:
            pywikibot.Page.__init__(self, site=site, title="Category:" + title, insite=insite,
                                    defaultNamespace=14)
        self.completelyCached = False
        self.articleCache = []
        self.subcatCache = []

    def aslink(self, forceInterwiki=False, textlink=False, noInterwiki=False):
        """A string representation in the form of a link.

        This method is different from Page.aslink() as the sortkey may have
        to be included.

        """
        if self.sortKey:
            titleWithSortKey = '%s|%s' % (self.title(savetitle=True),
                                          self.sortKey)
        else:
            titleWithSortKey = self.title(savetitle=True)
        if not noInterwiki and (forceInterwiki
                                or self.site() != pywikibot.getSite()):
            if self.site().family != pywikibot.getSite().family \
                    and self.site().family.name != self.site().lang:
                return '[[%s:%s:%s]]' % (self.site().family.name,
                                         self.site().lang,
                                         self.title(savetitle=True))
            else:
                return '[[%s:%s]]' % (self.site().lang,
                                      self.title(savetitle=True))
        elif textlink:
            return '[[:%s]]' % self.title(savetitle=True)
        else:
            return '[[%s]]' % titleWithSortKey

    def _getAndCacheContents(self, recurse=False, purge=False, startFrom=None,
                             cache=None, sortby=None, sortdir=None,
                             endsort=None):
        """Cache results of _parseCategory for a second call.

        If recurse is a bool, and value is True, then recursively retrieves
        contents of all subcategories without limit. If recurse is an int,
        recursively retrieves contents of subcategories to that depth only.

        Other parameters are analogous to _parseCategory(). If purge is True,
        cached results will be discarded. If startFrom is used, nothing
        will be cached.

        This should not be used outside of this module.

        """
        if cache is None:
            cache = []
        if purge:
            self.completelyCached = False
        if recurse:
            if type(recurse) is int:
                newrecurse = recurse - 1
            else:
                newrecurse = recurse
        if self.completelyCached:
            for article in self.articleCache:
                if article not in cache:
                    cache.append(article)
                    yield ARTICLE, article
            for subcat in self.subcatCache:
                if subcat not in cache:
                    cache.append(subcat)
                    yield SUBCATEGORY, subcat
                    if recurse:
                        # contents of subcategory are cached by calling
                        # this method recursively; therefore, do not cache
                        # them again
                        for item in subcat._getAndCacheContents(
                                newrecurse, purge, cache=cache, sortby=sortby,
                                sortdir=sortdir, endsort=endsort):
                            yield item
        else:
            for tag, page in self._parseCategory(purge, startFrom, sortby,
                                                 sortdir, endsort):
                if tag == ARTICLE:
                    self.articleCache.append(page)
                    if page not in cache:
                        cache.append(page)
                        yield ARTICLE, page
                elif tag == SUBCATEGORY:
                    self.subcatCache.append(page)
                    if page not in cache:
                        cache.append(page)
                        yield SUBCATEGORY, page
                        if recurse:
                            # contents of subcategory are cached by calling
                            # this method recursively; therefore, do not cache
                            # them again
                            for item in page._getAndCacheContents(
                                    newrecurse, purge, cache=cache,
                                    sortby=sortby, sortdir=sortdir):
                                yield item
            if not startFrom:
                self.completelyCached = True

    def _getContentsNaive(self, recurse=False, startFrom=None, sortby=None,
                          sortdir=None, endsort=None):
        """Simple category content yielder. Naive, do not attempts to
        cache anything

        """
        for tag, page in self._parseCategory(startFrom=startFrom,
                                             sortby=sortby, sortdir=sortdir,
                                             endsort=endsort):
            yield tag, page
            if tag == SUBCATEGORY and recurse:
                for item in page._getContentsNaive(recurse=True,
                                                   sortby=sortby,
                                                   sortdir=sortdir,
                                                   endsort=endsort):
                    yield item

    def _parseCategory(self, purge=False, startFrom=None, sortby=None,
                       sortdir=None, endsort=None):
        """
        Yields all articles and subcategories that are in this category by API.

        Set startFrom to a string which is the title of the page to start from.

        Yielded results are tuples in the form (tag, page) where tag is one
        of the constants ARTICLE and SUBCATEGORY, and title is the Page or
        Category object.

        Note that results of this method need not be unique.

        This should not be used outside of this module.

        """
        if not self.site().has_api() or self.site().versionnumber() < 11:
            for tag, page in self._oldParseCategory(purge, startFrom):
                yield tag, page
            return

        currentPageOffset = None
        params = {
            'action': 'query',
            'list': 'categorymembers',
            'cmtitle': self.title(),
            'cmprop': ['title', 'ids', 'sortkey', 'timestamp'],
            #'': '',
        }
        if self.site().versionnumber() > 16:
            params['cmprop'].append('sortkeyprefix')
        if sortby:
            params['cmsort'] = sortby
        if sortdir:
            params['cmdir'] = sortdir
        while True:
            if pywikibot.config.special_page_limit > 500:
                params['cmlimit'] = 500
            else:
                params['cmlimit'] = pywikibot.config.special_page_limit

            if currentPageOffset:
                params.update(currentPageOffset)
                pywikibot.output('Getting [[%s]] list from %s...'
                                 % (self.title(),
                                    "%s=%s" % currentPageOffset.popitem()))
            else:
                msg = 'Getting [[%s]] list' % self.title()
                # category sort keys are uppercase
                if startFrom:
                    startFrom = startFrom.upper()
                    params['cmstartsortkey'] = startFrom
                    msg += ' starting at %s' % startFrom
                if endsort:
                    endsort = endsort.upper()
                    params['cmendsortkey'] = endsort
                    msg += ' ending at %s' % endsort
                pywikibot.output(msg + u'...')

            pywikibot.get_throttle()
            data = query.GetData(params, self.site())
            if 'error' in data:
                raise RuntimeError("%s" % data['error'])
            count = 0

            for memb in data['query']['categorymembers']:
                count += 1
                # For MediaWiki versions where subcats look like articles
                if memb['ns'] == 14:
                    if 'sortkeyprefix' in memb:
                        sortKeyPrefix = memb['sortkeyprefix']
                    else:
                        sortKeyPrefix = None
                    yield SUBCATEGORY, Category(self.site(), memb['title'],
                                                sortKey=memb['sortkey'],
                                                sortKeyPrefix=sortKeyPrefix)
                elif memb['ns'] == 6:
                    yield ARTICLE, pywikibot.ImagePage(self.site(),
                                                       memb['title'])
                else:
                    page = pywikibot.Page(self.site(), memb['title'],
                                          defaultNamespace=memb['ns'])
                    if 'sortkeyprefix' in memb:
                        page.sortkeyprefix = memb['sortkeyprefix']
                    else:
                        page.sortkeyprefix = None
                    yield ARTICLE, page
                if count >= params['cmlimit']:
                    break
            # try to find a link to the next list page
            if 'query-continue' in data and count < params['cmlimit']:
                currentPageOffset = data['query-continue']['categorymembers']
            else:
                break

    def _oldParseCategory(self, purge=False, startFrom=None):
        """Yields all articles and subcategories that are in this category.

        Set purge to True to instruct MediaWiki not to serve a cached version.

        Set startFrom to a string which is the title of the page to start from.

        Yielded results are tuples in the form (tag, page) where tag is one
        of the constants ARTICLE and SUBCATEGORY, and title is the Page or
        Category object.

        Note that results of this method need not be unique.

        This should not be used outside of this module.

        """
        if self.site().versionnumber() < 4:
            Rtitle = re.compile('title\s?=\s?\"([^\"]*)\"')
        elif self.site().versionnumber() < 8:
            # FIXME seems to parse all links
            Rtitle = re.compile('/\S*(?: title\s?=\s?)?\"([^\"]*)\"')
        else:
            Rtitle = re.compile(
                '<li>(?:<span.*?>)?<a href=\".*?\"\s?title\s?=\s?\"'
                '([^\"]*)\"\>\+?[^\<\+]')
        if self.site().versionnumber() < 8:
            Rsubcat = None
            Rimage = None
        else:
            Rsubcat = re.compile(
                'CategoryTreeLabelCategory\"\s?href=\".+?\">(.+?)</a>')
            Rimage = re.compile(
                '<div class\s?=\s?\"thumb\"\sstyle=\"[^\"]*\">'
                '(?:<div style=\"[^\"]*\">)?<a href=\".*?\"'
                '(?:\sclass="image")?\stitle\s?=\s?\"([^\"]*)\"')
        # regular expression matching the "(next 200)" link
        RLinkToNextPage = re.compile('&amp;from=(.*?)" title="')

        if startFrom:
            currentPageOffset = urllib.quote(
                startFrom.encode(self.site().encoding()))
        else:
            currentPageOffset = None
        while True:
            path = self.site().get_address(self.urlname())
            if purge:
                path += '&action=purge'
            if currentPageOffset:
                path += '&from=' + currentPageOffset
                pywikibot.output('Getting [[%s]] starting at %s...'
                                 % (self.title(),
                                    pywikibot.url2link(currentPageOffset,
                                                       self.site(),
                                                       self.site())))
            else:
                pywikibot.output('Getting [[%s]]...' % self.title())
            pywikibot.get_throttle()
            txt = self.site().getUrl(path)
            # index where subcategory listing begins
            if self.site().versionnumber() >= 9:
                # These IDs were introduced in 1.9
                if '<div id="mw-subcategories">' in txt:
                    ibegin = txt.index('<div id="mw-subcategories">')
                elif '<div id="mw-pages">' in txt:
                    ibegin = txt.index('<div id="mw-pages">')
                elif '<div id="mw-category-media">' in txt:
                    ibegin = txt.index('<div id="mw-category-media">')
                else:
                    # No pages
                    return
            else:
                # does not work for cats without text
                ibegin = txt.index('<!-- start content -->')
                # TODO: This parses category text and may think they are
                # pages in category! Check for versions before 1.9

            # index where article listing ends
            if '<div class="printfooter">' in txt:
                iend = txt.index('<div class="printfooter">')
            elif '<div class="catlinks">' in txt:
                iend = txt.index('<div class="catlinks">')
            else:
                iend = txt.index('<!-- end content -->')
            txt = txt[ibegin:iend]
            for title in Rtitle.findall(txt):
                if title == self.title():
                    # This is only a link to "previous 200" or "next 200".
                    # Ignore it.
                    pass
                # For MediaWiki versions where subcats look like articles
                elif isCatTitle(title, self.site()):
                    yield SUBCATEGORY, Category(self.site(), title)
                else:
                    yield ARTICLE, pywikibot.Page(self.site(), title)
            if Rsubcat:
                # For MediaWiki versions where subcats look differently
                for titleWithoutNamespace in Rsubcat.findall(txt):
                    title = 'Category:%s' % titleWithoutNamespace
                    yield SUBCATEGORY, Category(self.site(), title)
            if Rimage:
                # For MediaWiki versions where images work through galleries
                for title in Rimage.findall(txt):
                    # In some MediaWiki versions, the titles contain the
                    # namespace, but they don't in other (newer) versions. Use
                    # the ImagePage's defaultNamespace feature to get everything
                    # correctly.
                    yield ARTICLE, pywikibot.ImagePage(self.site(), title)
            # try to find a link to the next list page
            matchObj = RLinkToNextPage.search(txt)
            if matchObj:
                currentPageOffset = matchObj.group(1)
            else:
                break

    def subcategories(self, recurse=False, startFrom=None, cacheResults=False,
                      sortby=None, sortdir=None):
        """Yields all subcategories of the current category.

        If recurse is True, also yields subcategories of the subcategories.
        If recurse is a number, also yields subcategories of subcategories,
        but only at most that number of levels deep (that is, recurse = 0 is
        equivalent to recurse = False, recurse = 1 gives first-level
        subcategories of subcategories but no deeper, etcetera).

        cacheResults - cache the category contents: useful if you need to
        do several passes on the category members list. The simple cache
        system is *not* meant to be memory or cpu efficient for large
        categories

        Results a sorted (as sorted by MediaWiki), but need not be unique.

        """
        if cacheResults:
            gen = self._getAndCacheContents
        else:
            gen = self._getContentsNaive
        for tag, subcat in gen(recurse=recurse, startFrom=startFrom,
                               sortby=sortby, sortdir=sortdir):
            if tag == SUBCATEGORY:
                yield subcat

    def subcategoriesList(self, recurse=False, sortby=None, sortdir=None):
        """Creates a list of all subcategories of the current category.

        If recurse is True, also return subcategories of the subcategories.
        Recurse can also be a number, as explained above.

        The elements of the returned list are sorted and unique.

        """
        subcats = []
        for cat in self.subcategories(recurse, sortby=sortby, sortdir=sortdir):
            subcats.append(cat)
        return unique(subcats)

    def articles(self, recurse=False, startFrom=None, cacheResults=False,
                 sortby=None, sortdir=None, endsort=None):
        """Yields all articles of the current category.

        If recurse is True, also yields articles of the subcategories.
        Recurse can be a number to restrict the depth at which subcategories
        are included.

        cacheResults - cache the category contents: useful if you need to
        do several passes on the category members list. The simple cache
        system is *not* meant to be memory or cpu efficient for large
        categories

        Results are unsorted (except as sorted by MediaWiki), and need not
        be unique.

        """
        if cacheResults:
            gen = self._getAndCacheContents
        else:
            gen = self._getContentsNaive
        for tag, page in gen(recurse=recurse, startFrom=startFrom,
                             sortby=sortby, sortdir=sortdir, endsort=endsort):
            if tag == ARTICLE:
                yield page

    def articlesList(self, recurse=False, sortby=None, sortdir=None):
        """Creates a list of all articles of the current category.

        If recurse is True, also return articles of the subcategories.
        Recurse can be a number to restrict the depth at which subcategories
        are included.

        The elements of the returned list are sorted and unique.

        """
        articles = []
        for article in self.articles(recurse, sortby=sortby, sortdir=sortdir):
            articles.append(article)
        return unique(articles)

    def supercategories(self):
        """Yields all supercategories of the current category.

        Results are stored in the order in which they were entered, and need
        not be unique.

        """
        for supercat in self.categories():
            yield supercat

    def supercategoriesList(self):
        """Creates a list of all supercategories of the current category.

        The elements of the returned list are sorted and unique.

        """
        supercats = []
        for cat in self.supercategories():
            supercats.append(cat)
        return unique(supercats)

    def isEmptyCategory(self):
        """Return True if category has no members (including subcategories)."""
        for tag, title in self._parseCategory():
            return
        return True

    def isHiddenCategory(self):
        """Return True if the category is hidden."""
        text = self.get()
        hidden = re.search('__HIDDENCAT__', text)
        if hidden:
            return True

    def copyTo(self, catname):
        """Returns true if copying was successful, false if target page already
        existed.

        """
        catname = self.site().category_namespace() + ':' + catname
        targetCat = pywikibot.Page(self.site(), catname)
        if targetCat.exists():
            pywikibot.output('Target page %s already exists!'
                             % targetCat.title())
            return
        else:
            pywikibot.output('Moving text from %s to %s.'
                             % (self.title(), targetCat.title()))
            authors = ', '.join(self.contributingUsers())
            creationSummary = pywikibot.translate(pywikibot.getSite(),
                                                  msg_created_for_renaming) \
                                                  % (self.title(), authors)
            # Maybe sometimes length of summary is more than 200 characters and
            # thus will not be shown. For avoidning copyright violation bot must
            # listify authors in another place
            if len(creationSummary) > 200:
                talkpage = targetCat.toggleTalkPage()
                try:
                    talktext = talkpage.get()
                except pywikibot.NoPage:
                    talkpage.put(u"==Authors==\n%s-~~~~" % authors,
                                 u"Bot:Listifying authors")
                else:
                    talkpage.put(talktext + u"\n==Authors==\n%s-~~~~" % authors,
                                 u"Bot:Listifying authors")
            targetCat.put(self.get(), creationSummary)
            return True

    # Like copyTo above, except this removes a list of templates (like deletion
    # templates) that appear in the old category text.  It also removes all text
    # between the two HTML comments BEGIN CFD TEMPLATE and END CFD TEMPLATE.
    # (This is to deal with CFD templates that are substituted.)
    def copyAndKeep(self, catname, cfdTemplates):
        """Returns true if copying was successful, false if target page already
        existed.

        """
        targetCat = pywikibot.Page(self.site(), catname, defaultNamespace=14)
        if targetCat.exists():
            pywikibot.output('Target page %s already exists!'
                             % targetCat.title())
            return
        else:
            pywikibot.output('Moving text from %s to %s.'
                             % (self.title(), targetCat.title()))
            authors = ', '.join(self.contributingUsers())
            creationSummary = pywikibot.translate(pywikibot.getSite(),
                                                  msg_created_for_renaming) \
                                                  % (self.title(), authors)
            newtext = remove_cfd_templates(cfdTemplates, self.get())
        targetCat.put(newtext, creationSummary)
        return True


def remove_cfd_templates(cfdTemplates, pageText):
    for regexName in cfdTemplates:
        matchcfd = re.compile(r"{{%s.*?}}" % regexName, re.IGNORECASE)
        pageText = matchcfd.sub('', pageText)
        matchcomment = re.compile(
            r"<!--\s*?BEGIN CFD TEMPLATE\s*?-->.*?<!--\s*?END CFD TEMPLATE\s*?-->",
            re.IGNORECASE | re.MULTILINE | re.DOTALL)
        pageText = matchcomment.sub('', pageText)
        pos = 0
        while (pageText[pos:pos + 1] == "\n"):
            pos = pos + 1
        pageText = pageText[pos:]
    return pageText


def add_category(article, category, comment=None, createEmptyPages=False):
    """Given an article and a category, adds the article to the category."""
    cats = article.categories(get_redirect=True)
    if category not in cats:
        cats.append(category)
        try:
            text = article.get()
        except pywikibot.NoPage:
            if createEmptyPages:
                text = ''
            else:
                raise

        text = pywikibot.replaceCategoryLinks(text, cats)
        try:
            article.put(text, comment=comment)
        except pywikibot.EditConflict:
            pywikibot.output(u'Skipping %s because of edit conflict'
                             % article.title())


#def Category(code, name):
#    """Factory method to create category link objects from the category name"""
#    # Standardized namespace
#    ns = pywikibot.getSite().category_namespaces()[0]
#    # Prepend it
#    return Category(code, "%s:%s" % (ns, name))

def change_category(article, oldCat, newCat, comment=None, sortKey=None,
                    inPlace=False):
    """
    Remove page from oldCat and add it to newCat.

    @param oldCat and newCat: should be Category objects.
        If newCat is None, the category will be removed.

    @param comment: string to use as an edit summary

    @param sortKey: sortKey to use for the added category.
        Unused if newCat is None, or if inPlace=True

    @param inPlace: if True, change categories in place rather than
                  rearranging them.

    """
    cats = []

    # get list of Category objects the article is in and remove duplicates
    for cat in article.categories(get_redirect=True):
        if cat not in cats:
            cats.append(cat)

    site = article.site()

    if not sortKey:
        sortKey = oldCat.sortKey

    if not article.canBeEdited():
        pywikibot.output("Can't edit %s, skipping it..."
                         % article.title(asLink=True))
        return

    if oldCat not in cats:
        pywikibot.error(u'%s is not in category %s!'
                        % (article.title(asLink=True), oldCat.title()))
        return

    if inPlace or article.namespace() == 10:
        oldtext = article.get(get_redirect=True)
        newtext = pywikibot.replaceCategoryInPlace(oldtext, oldCat, newCat)
    else:
        if newCat:
            cats[cats.index(oldCat)] = Category(site, newCat.title(),
                                                sortKey=sortKey)
        else:
            cats.pop(cats.index(oldCat))
        oldtext = article.get(get_redirect=True)
        try:
            newtext = pywikibot.replaceCategoryLinks(oldtext, cats)
        except ValueError:
            # Make sure that the only way replaceCategoryLinks() can return
            # a ValueError is in the case of interwiki links to self.
            pywikibot.output(u'Skipping %s because of interwiki link to self'
                             % article)

    if oldtext != newtext:
        try:
            article.put(newtext, comment)
        except pywikibot.EditConflict:
            pywikibot.output(u'Skipping %s because of edit conflict'
                             % article.title())
        except pywikibot.SpamfilterError, e:
            pywikibot.output(u'Skipping %s because of blacklist entry %s'
                             % (article.title(), e.url))
        except pywikibot.LockedPage:
            pywikibot.output(u'Skipping %s because page is locked'
                             % article.title())
        except pywikibot.NoUsername:
            pywikibot.output(u'Page %s not saved; sysop privileges required.'
                             % article.title(asLink=True))
        except pywikibot.PageNotSaved, error:
            pywikibot.output(u"Saving page %s failed: %s"
                             % (article.title(asLink=True), error.message))


def categoryAllElementsAPI(CatName, cmlimit=5000, categories_parsed=[],
                           site=None):
    """ Category to load all the elements in a category using the APIs.
    Limit: 5000 elements.

    """
    pywikibot.output("Loading %s..." % CatName)

    # action=query&list=categorymembers&cmlimit=500&cmtitle=Category:License_tags
    params = {
        'action':  'query',
        'list':    'categorymembers',
        'cmlimit': cmlimit,
        'cmtitle': CatName,
    }

    data = query.GetData(params, site)
    categories_parsed.append(CatName)
    try:
        members = data['query']['categorymembers']
    except KeyError:
        if int(cmlimit) != 500:
            pywikibot.output(
                u'An Error occured, trying to reload the category.')
            return categoryAllElementsAPI(CatName, cmlimit=500)
        else:
            raise pywikibot.Error(data)
    if len(members) == int(cmlimit):
        raise pywikibot.Error(
            u'The category selected has >= %s elements, limit reached.'
            % cmlimit)
    allmembers = members
    results = list()
    for subcat in members:
        ns = subcat['ns']
        title = subcat['title']
        if ns == 14:
            if title not in categories_parsed:
                categories_parsed.append(title)
                (results_part,
                 categories_parsed) = categoryAllElementsAPI(title, 5000,
                                                             categories_parsed)
                allmembers.extend(results_part)
    for member in allmembers:
        results.append(member)
    return (results, categories_parsed)


def categoryAllPageObjectsAPI(CatName, cmlimit=5000, categories_parsed=[],
                              site=None):
    """From a list of dictionaries, return a list of page objects."""
    final = list()
    if site is None:
        site = pywikibot.getSite()
    for element in categoryAllElementsAPI(CatName, cmlimit, categories_parsed,
                                          site)[0]:
        final.append(pywikibot.Page(site, element['title']))
    return final


def test():
    site = pywikibot.getSite()
    cat = Category(site, 'Category:Software')
    pywikibot.output(u'SUBCATEGORIES:')
    for subcat in cat.subcategories():
        pywikibot.output(subcat.title())
    pywikibot.output(u'\nARTICLES:')
    for article in cat.articles():
        pywikibot.output(article.title())

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        pywikibot.output(u'Ignored argument: %s' % arg)
    test()
