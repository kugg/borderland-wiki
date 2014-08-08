#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Include Commons template in home wiki.

This bot functions mainly in the en.wikipedia, because it
compares the names of articles and category in English
language (standard language in Commons). If the name of
an article in Commons will not be in English but with
redirect, this also functions.

Run:
Syntax: python commons_link.py [action] [pagegenerator]

where action can be one of these:
 * pages      : Run over articles, include {{commons}}
 * categories : Run over categories, include {{commonscat}}

and pagegenerator can be one of these:
&params;

"""
#
# (C) Leonardo Gregianin, 2006
# (C) Pywikibot team, 2007-2014
#
# Distributed under the terms of the MIT license.
#

__version__ = '$Id$'

import re
import wikipedia as pywikibot
import pagegenerators
import catlib

docuReplacements = {
    '&params;':     pagegenerators.parameterHelp,
}

comment1 = {
    'ar': u'روبوت: تضمين قالب كومنز',
    'cs': u'Robot přidal šablonu commons',
    'en': u'Robot: Include commons template',
    'fa': u'ربات: افزودن الگوی ویکی‌انبار',
    'he': u'בוט: מוסיף תבנית Commons',
    'ja': u'ロボットによる: テンプレcommons追加',
    'nl': u'Bot: sjabloon commons toegevoegd',
    'zh': u'機器人: 增加commons模板',
}

comment2 = {
    'ar': u'روبوت: تضمين قالب تصنيف كومنز',
    'cs': u'Robot přidal šablonu commonscat',
    'en': u'Robot: Include commonscat template',
    'fa': u'ربات: افزودن الگوی رده‌بندی ویکی‌انبار',
    'he': u'בוט: מוסיף תבנית Commonscat',
    'ja': u'ロボットによる: テンプレcommonscat追加',
    'nl': u'Bot: sjabloon commonscat toegevoegd',
    'zh': u'機器人: 增加commonscat模板',
}


class CommonsLinkBot:
    def __init__(self, generator, acceptall=False):
        self.generator = generator
        self.acceptall = acceptall

    def pages(self):
        for page in self.generator:
            try:
                pywikibot.output(u'\n>>>> %s <<<<' % page.title())
                commons = pywikibot.getSite().image_repository()
                commonspage = pywikibot.Page(commons, page.title())
                try:
                    getcommons = commonspage.get(get_redirect=True)
                    if page.title() == commonspage.title():
                        oldText = page.get()
                        text = oldText

                        # for commons template
                        findTemplate = re.compile(ur'\{\{[Cc]ommonscat')
                        s = findTemplate.search(text)
                        findTemplate2 = re.compile(ur'\{\{[Ss]isterlinks')
                        s2 = findTemplate2.search(text)
                        if s or s2:
                            pywikibot.output(u'** Already done.')
                        else:
                            text = pywikibot.replaceCategoryLinks(
                                text + u'{{commons|%s}}' % commonspage.title(),
                                page.categories())
                            if oldText != text:
                                pywikibot.showDiff(oldText, text)
                                if not self.acceptall:
                                    choice = pywikibot.inputChoice(
                                        u'Do you want to accept these changes?',
                                        ['Yes', 'No', 'All'], ['y', 'N', 'a'],
                                        'N')
                                    if choice == 'a':
                                        self.acceptall = True
                                if self.acceptall or choice == 'y':
                                    try:
                                        msg = pywikibot.translate(
                                            pywikibot.getSite(), comment1)
                                        page.put(text, msg)
                                    except pywikibot.EditConflict:
                                        pywikibot.output(
                                            u'Skipping %s because of edit '
                                            u'conflict'
                                            % (page.title()))

                except pywikibot.NoPage:
                    pywikibot.output(u'Page does not exist in Commons!')

            except pywikibot.NoPage:
                pywikibot.output(u'Page %s does not exist?!' % page.title())
            except pywikibot.IsRedirectPage:
                pywikibot.output(u'Page %s is a redirect; skipping.'
                                 % page.title())
            except pywikibot.LockedPage:
                pywikibot.output(u'Page %s is locked?!' % page.title())

    def categories(self):
        for page in self.generator:
            try:
                pywikibot.output(u'\n>>>> %s <<<<' % page.title())
                commons = pywikibot.getSite().image_repository()
                commonsCategory = catlib.Category(commons,
                                                  'Category:%s' % page.title())
                try:
                    getcommonscat = commonsCategory.get(get_redirect=True)
                    commonsCategoryTitle = commonsCategory.title()
                    categoryname = commonsCategoryTitle.split('Category:', 1)[1]
                    if page.title() == categoryname:
                        oldText = page.get()
                        text = oldText

                        # for commonscat template
                        findTemplate = re.compile(ur'\{\{[Cc]ommons')
                        s = findTemplate.search(text)
                        findTemplate2 = re.compile(ur'\{\{[Ss]isterlinks')
                        s2 = findTemplate2.search(text)
                        if s or s2:
                            pywikibot.output(u'** Already done.')
                        else:
                            text = pywikibot.replaceCategoryLinks(
                                text + u'{{commonscat|%s}}' % categoryname,
                                page.categories())
                            if oldText != text:
                                pywikibot.showDiff(oldText, text)
                                if not self.acceptall:
                                    choice = pywikibot.inputChoice(
                                        u'Do you want to accept these changes?',
                                        ['Yes', 'No', 'All'], ['y', 'N', 'a'],
                                        'N')
                                    if choice == 'a':
                                        self.acceptall = True
                                if self.acceptall or choice == 'y':
                                    try:
                                        msg = pywikibot.translate(
                                            pywikibot.getSite(), comment2)
                                        page.put(text, msg)
                                    except pywikibot.EditConflict:
                                        pywikibot.output(
                                            u'Skipping %s because of edit '
                                            u'conflict'
                                            % (page.title()))

                except pywikibot.NoPage:
                    pywikibot.output(u'Category does not exist in Commons!')

            except pywikibot.NoPage:
                pywikibot.output(u'Page %s does not exist' % page.title())
            except pywikibot.IsRedirectPage:
                pywikibot.output(u'Page %s is a redirect; skipping.'
                                 % page.title())
            except pywikibot.LockedPage:
                pywikibot.output(u'Page %s is locked' % page.title())

if __name__ == "__main__":
    genFactory = pagegenerators.GeneratorFactory()
    try:
        action = None
        for arg in pywikibot.handleArgs():
            if arg in ('pages', 'categories'):
                action = arg
            else:
                genFactory.handleArg(arg)

        gen = genFactory.getCombinedGenerator()
        if gen and action:
            gen = pagegenerators.PreloadingGenerator(gen)
            bot = CommonsLinkBot(gen, acceptall=False)
            getattr(bot, action)()
        else:
            pywikibot.showHelp(u'commons_link')
    finally:
        pywikibot.stopme()
