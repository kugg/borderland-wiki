#!/usr/bin/python
# -*- coding: utf-8  -*-
""" Script to enumerate all pages in the wikipedia and find all titles
with mixed latin and cyrilic alphabets.
"""

#
# Permutations code was taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/190465
#
from __future__ import generators

def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc
# End of permutation code

#
# Windows Concose colors
# This code makes this script Windows ONLY!!!  Feel free to adapt it to another platform
#
#
FOREGROUND_BLUE = 1
FOREGROUND_GREEN = 2
FOREGROUND_RED = 4

FOREGROUND_WHITE = 1|2|4

def SetColor(color):
    try:
        import win32console
        stdout=win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
        stdout.SetConsoleTextAttribute(color)
    except:
        if color == FOREGROUND_BLUE: print '(b:'
        if color == FOREGROUND_GREEN: print '(g:'
        if color == FOREGROUND_RED: print '(r:'
                
# end of console code




import sys, query, wikipedia, re, codecs


class CaseChecker( object ):

    knownWords = set([u'Zемфира', u'KoЯn', u'Deadушки', u'ENTERМУЗЫКА'])
    
    cyrLtr = u'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    latLtr = u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ukrLtr = u'АаБбВвГгҐґДдЕеЄєЖжЗзИиІіЇїЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЮюЯяЬь'

    cyrSuspects    = u'АаВЕеКкМмНОоРрСсТуХх'
    cyrLatSuspects = u'AaBEeKkMmHOoPpCcTyXx'
    ukrSuspects    = u'АаВвЕеІіКкМмНОоРрСсТтУуХх'
    ukrLatSuspects = u'AaBbEeIiKkMmHOoPpCcTtYyXx'

    cyrClrFnt = u'<font color=green>'
    latClrFnt = u'<font color=brown>'
    suffixClr = u'</font>'

    titles = True
    links = False
    aplimit = 500
    apfrom = u''
    title = None
    replace = False
    stopAfter = 0
    verbose = False
    wikilog = None
    
    def __init__(self, args):    
        
        for arg in args:
            arg = wikipedia.argHandler(arg, 'casechecker')
            if arg:
                if arg.startswith('-from:'):
                    self.apfrom = arg[6:]
                elif arg.startswith('-from'):
                    self.apfrom = wikipedia.input(u'Which page to start from: ')
                elif arg.startswith('-reqsize:'):
                    self.aplimit = int(arg[9:])
                elif arg == '-links':
                    self.links = True
                elif arg == '-linksonly':
                    self.links = True
                    self.titles = False
                elif arg == '-replace':
                    self.replace = True
                elif arg.startswith('-limit:'):
                    self.stopAfter = int(arg[7:])
                elif arg == '-verbose':
                    self.verbose = True
                elif arg.startswith('-wikilog:'):
                    try:
                        self.wikilog = codecs.open(arg[9:], 'a', 'utf-8')
                    except IOError:
                        self.wikilog = codecs.open(arg[9:], 'w', 'utf-8')
                else:
                    wikipedia.output(u'Unknown argument %s' % arg)
                    sys.exit()

        self.params = {'what'         : 'allpages',
                      'aplimit'       : self.aplimit, 
                      'apfilterredir' : 'nonredirects',
                      'noprofile'     : '' }

        if self.links:
            self.params['what'] += '|links';
            
        self.site = wikipedia.getSite()
        
        if self.site.lang == 'ru':
            self.localSuspects = self.cyrSuspects
            self.latinSuspects = self.cyrLatSuspects
            self.localLtr = self.cyrLtr
        elif self.site.lang == 'uk':
            self.localSuspects = self.ukrSuspects
            self.latinSuspects = self.ukrLatSuspects
            self.localLtr = self.ukrLtr
        else:
            raise u'Unsupported site ' + self.site.lang
    
        if len(self.localSuspects) != len(self.latinSuspects):
            raise u'Suspects must be the same size'

        self.cyrToLatDict = dict([(ord(self.localSuspects[i]), self.latinSuspects[i]) for i in range(len(self.localSuspects))])
        self.latToCyrDict = dict([(ord(self.latinSuspects[i]), self.localSuspects[i]) for i in range(len(self.localSuspects))])
    
        badPtrnStr = u'([%s][%s]|[%s][%s])' % (self.latLtr, self.localLtr, self.localLtr, self.latLtr)
        self.badPtrn = re.compile(badPtrnStr)
        self.badWordPtrn = re.compile(u'[%s%s]*%s[%s%s]*' % (self.latLtr, self.localLtr, badPtrnStr, self.latLtr, self.localLtr) )
            
        
    def Run(self):
        try:
            count = 0
            for namespace in [0, 10, 12, 14]:
                self.params['apnamespace'] = namespace
                self.apfrom = self.apfrom
                title = None
                
                while True:                
                    # Get data
                    self.params['apfrom'] = self.apfrom
                    data = query.GetData(self.site.lang, self.params, self.verbose)
                    try:
                        self.apfrom = data['query']['allpages']['next']
                    except:
                        self.apfrom = None
    
                    # Process received data
                    if 'pages' in data:
                        for pageID, page in data['pages'].iteritems():
                            printed = False
                            title = page['title']
                            if self.titles:
                                err = self.ProcessTitle(title)
                                if err:
                                    changed = False
                                    if self.replace and namespace != 14:
                                        newTitle = self.PickTarget(False, title, err[1])
                                        if newTitle:
                                            src = wikipedia.Page(self.site, title)
                                            src.move( newTitle, u'mixed case rename')
                                            changed = True
                                    
                                    if not changed:
                                        self.WikiLog(u"* " + err[0])
                                        printed = True
                                                                    
                            if self.links:
                                if 'links' in page:
                                    pageObj = None
                                    pageTxt = None
                                    msg = []
                                    for l in page['links']:
                                        ltxt = l['*']
                                        err = self.ProcessTitle(ltxt)
                                        if err:
                                            newTitle = None
                                            if self.replace:
                                                newTitle = self.PickTarget(True, ltxt, err[1])
                                                if newTitle:
                                                    if pageObj is None:
                                                        pageObj = wikipedia.Page(self.site, title)
                                                        pageTxt = pageObj.get()
                                                    msg.append(u'[[%s]] => [[%s]]' % (ltxt, newTitle))
                                                    pageTxt = pageTxt.replace(ltxt, newTitle)
                                                    pageTxt = pageTxt.replace(ltxt[0].lower() + ltxt[1:], newTitle[0].lower() + newTitle[1:])
                                            
                                            if not newTitle:
                                                if not printed:
                                                    self.WikiLog(u"* [[:%s]]: link to %s" % (title, err[0]))
                                                    printed = True
                                                else:
                                                    self.WikiLog(u"** link to %s" % err[0])
                                                
        
                                    if pageObj is not None:
                                        if pageObj.get() == pageTxt:
                                            self.WikiLog(u"* Error: Text replacement failed in [[:%s]] (%s)" % (title, u', '.join(msg)))
                                        else:
                                            wikipedia.output(u'Case Replacements: %s' % u', '.join(msg))
                                            try:
                                                pageObj.put(pageTxt, u'Case Replacements: %s' % u', '.join(msg))
                                            except:
                                                self.WikiLog(u"* Error: Could not save updated page [[:%s]] (%s)" % (title, u', '.join(msg)))
                                                
                        
                            count += 1
                            if self.stopAfter > 0 and count == self.stopAfter:
                                raise "Stopping because we are done"
                        
                    if self.apfrom is None:
                        break

            print "***************************** Done"
                
        except:
            if self.apfrom is not None:
                wikipedia.output(u'Exception at Title = %s, Next = %s' % (title, self.apfrom))
            wikipedia.stopme()
            raise

    def WikiLog(self, text):
        wikipedia.output(text)
        if self.wikilog:
            self.wikilog.write(text + u'\n')
            self.wikilog.flush()
        
    def ProcessTitle(self, title):
        
        found = False
        for m in self.badWordPtrn.finditer(title):
            
            badWord = title[m.span()[0] : m.span()[1]]
            if badWord in self.knownWords:
                continue

            if not found:
                # lazy-initialization of the local variables
                possibleWords = []
                tempWords = []
                count = 0
                duplWordCount = 0
                ambigBadWords = set()
                ambigBadWordsCount = 0
                mapCyr = {}
                mapLat = {}
                found = True
                                        
            # See if it would make sense to treat the whole word as either cyrilic or latin
            mightBeLat = mightBeCyr = True
            for l in badWord:
                if l in self.localLtr:
                    if mightBeLat and l not in self.localSuspects:
                        mightBeLat = False
                else:
                    if mightBeCyr and l not in self.latinSuspects:
                        mightBeCyr = False
                    if l not in self.latLtr: raise "Assert failed"
            
            if mightBeCyr:
                mapCyr[badWord] = badWord.translate(self.latToCyrDict)
            if mightBeLat:
                mapLat[badWord] = badWord.translate(self.cyrToLatDict)
            if mightBeCyr and mightBeLat:
                ambigBadWords.add(badWord)
                ambigBadWordsCount += 1    # Cannot do len(ambigBadWords) because they might be duplicates
            count += 1

        if not found:
            return None
        
        infoText = self.MakeLink(title)
        possibleAlternatives = []
        
        if len(mapCyr) + len(mapLat) - ambigBadWordsCount < count:
            # We cannot auto-translate - offer a list of suggested words
            infoText += u", word sugestions: " + u', '.join([self.ColorCodeWord(t) for t in mapCyr.values() + mapLat.values()])
        else:
            
            # Replace all unambiguous bad words
            for k,v in mapLat.items() + mapCyr.items():
                if k not in ambigBadWords:
                    title = title.replace(k,v)

            if len(ambigBadWords) == 0:
                # There are no ambiguity, we can safelly convert
                possibleAlternatives.append(title)
                infoText += u", will convert to " + self.MakeLink(title)
            else:
                # Try to pick 0, 1, 2, ..., len(ambiguous words) unique combinations
                # from the bad words list, and convert just the picked words to cyrilic,
                # whereas making all other words as latin character.
                for itemCntToPick in range(0, len(ambigBadWords)+1):
                    title2 = title
                    for uc in xuniqueCombinations(list(ambigBadWords), itemCntToPick):
                        wordsToLat = ambigBadWords.copy()
                        for bw in uc:
                            title2 = title2.replace(bw, mapCyr[bw])
                            wordsToLat.remove(bw)
                        for bw in wordsToLat:
                            title2 = title2.replace(bw, mapLat[bw])
                        possibleAlternatives.append(title2)

                infoText += u", can be converted to " + u', '.join([self.MakeLink(t) for t in possibleAlternatives])

        return (infoText, possibleAlternatives)
    
    def PickTarget(self, isLink, original, candidates):
        if len(candidates) == 0:
            return None
        
        if isLink:
            if len(candidates) == 1:
                return candidates[0]
            
            pagesDontExist = []
            pagesRedir = {}
            pagesExist = []
            
            for newTitle in candidates:
                dst = wikipedia.Page(self.site, newTitle)
                if not dst.exists():
                    pagesDontExist.append(newTitle)
                elif dst.isRedirectPage():
                    pagesRedir[newTitle] = dst.getRedirectTarget()
                else:
                    pagesExist.append(newTitle)
            
            if len(pagesExist) == 1:
                return pagesExist[0]
            elif len(pagesExist) == 0 and len(pagesRedir) > 0:
                if len(pagesRedir) == 1:
                    return pagesRedir.keys()[0]
                t = None
                for k,v in pagesRedir.iteritems():
                    if not t:
                        t = v # first item
                    elif t != v:
                        break
                else:
                    # all redirects point to the same target
                    # pick the first one, doesn't matter what it is
                    return pagesRedir.keys()[0]
                
            wikipedia.output(u'Could not auto-decide. Which should be chosen?')
            self.ColorCodeWord(original, True)
            count = 1
            for t in candidates:
                if t in pagesDontExist: msg = u'missing'
                elif t in pagesRedir: msg = u'Redirect to ' + pagesRedir[t]
                else: msg = u'page exists'
                self.ColorCodeWord(u'  %d: %s (%s)\n' % (count, t, msg), True)
                count += 1
            
            answers = [str(i) for i in range(0, count)]
            choice = int(wikipedia.inputChoice(u'Which link to choose? (0 to skip)', answers, [a[0] for a in answers]))
            if choice > 0:
                return candidates[choice-1]

        else:
            if len(candidates) == 1:
                newTitle = candidates[0]
                dst = wikipedia.Page(self.site, newTitle)
                if not dst.exists():
                    # choice = wikipedia.inputChoice(u'Move %s to %s?' % (title, newTitle), ['Yes', 'No'], ['y', 'n'])
                    return newTitle
        
        return None

    def ColorCodeWord(self, word, toScreen = False):
        
        if not toScreen: res = u"<b>"
        lastIsCyr = word[0] in self.localLtr
        if lastIsCyr:
            if toScreen: SetColor(FOREGROUND_GREEN)
            else: res += self.cyrClrFnt
        else:
            if toScreen: SetColor(FOREGROUND_RED)
            else: res += self.latClrFnt

        for l in word:
            if l in self.localLtr:
                if not lastIsCyr:
                    if toScreen: SetColor(FOREGROUND_GREEN)
                    else: res += self.suffixClr + self.cyrClrFnt
                    lastIsCyr = True
            elif l in self.latLtr:
                if lastIsCyr:
                    if toScreen: SetColor(FOREGROUND_RED)
                    else: res += self.suffixClr + self.latClrFnt
                    lastIsCyr = False
            if toScreen: wikipedia.output(l, newline=False)
            else: res += l
        
        if toScreen: SetColor(FOREGROUND_WHITE)
        else: return res + self.suffixClr + u"</b>"
        

    def MakeLink(self, title):
        return u"[[:%s|««« %s »»»]]" % (title, self.ColorCodeWord(title))
        
if __name__ == "__main__":
    bot = CaseChecker(sys.argv[1:])
    bot.Run()