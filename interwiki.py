#coding: iso-8859-1
"""
Script to check language links for general pages. This works by downloading the
page, and using existing translations plus hints from the command line to
download the equivalent pages from other languages. All of such pages are
downloaded as well and checked for interwiki links recursively until there are
no more links that are encountered. A rationalization process then selects the
right interwiki links, and if this is unambiguous, the interwiki links in the
original page will be automatically updated and the modified page uploaded.

This script understands various command-line arguments:
    -force:        do not ask permission to make "controversial" changes,
                   like removing a language because none of the found
                   alternatives actually exists.

    -always:       make changes even when a single byte is changed in
                   the page, not only when one of the links has a significant
                   change.

    -hint:         used as -hint:de:Anweisung to give the robot a hint
                   where to start looking for translations. This is only
                   useful if you specify a single page to work on.
                   Special hints: all gives a hint for all seriouslangs, main
                   gives a hint for 8 of the largest languages, more for about
                   20 larger ones.
                   
    -same:         try to translate the page to other languages by
                   testing whether a page with the same name exists on each of
                   the other known wikipedias

    -name:         similar to -same, but UPPERCASE the last name for eo:

    -untranslated: untranslated pages are not skipped; instead in those
                   cases interactively a translation hint is asked of the user.

    -untranslatedonly: same as -untranslated, but pages which already have a
                   translation are skipped. Hint: do NOT use this in combination
                   with -start without a -number limit, because you will go through
                   the whole alphabet before any queries are performed!

    -askhints: same as -untranslated, but translations are also asked for pages
                   that already have translations.

    -file:         used as -file:filename, read a list of pages to treat
                   from the named file
                   
    -confirm:      ask for confirmation before any page is changed on the
                   live wikipedia. Without this argument, additions and
                   unambiguous modifications are made without confirmation.

    -autonomous:   run automatically, do not ask any questions. If a question
                   to an operator is needed, write the name of the page
                   to autonomous_problems.dat and continue on the next page.

    -test:         run on three pages named "Scheikunde", "Natuurkunde",
                   and "Wiskunde". This is a trivial test of the functionality.

    -nobell:       do not use the terminal bell to announce a question

    -nolog:        switch off the log file

    -nobacklink:   switch off the backlink warnings

    -start:        used as -start:pagename, specifies that the robot should
                   go alphabetically through all pages on the home wikipedia,
                   starting at the named page.

    -number:       used as -number:#, specifies that the robot should process
                   that amount of pages and then stop. This is only useful in
                   combination with -start. The default is not to stop.

    -years:        run on all year pages in numerical order. Stop at year 2050.
                   If the argument is given in the form -years:XYZ, it will 
                   run from [[XYZ]] through [[2050]]. If XYZ is a negative value,
                   it is interpreted as a year BC. If the argument is simply
                   given as -years, it will run from 1 through 2050.
                   
                   This implies -noredirect.
    
    -skipfile:     used as -skipfile:filename, skip all links mentioned in
                   the mentioned file from the list generated by -start. This
                   does not work with -number!

    -restore:      restore a set of "dumped" pages the robot was working on
                   when it terminated.
                   
    -warnfile:     used as -warnfile:filename, reads all warnings from the
                   given file that apply to the home wikipedia language, and
                   read the rest of the warning as a hint. Then treats all the
                   mentioned pages. A quicker way to implement warnfile
                   suggestions without verifying them against the live wikipedia
                   is using the warnfile.py robot.

    -noredirect:   do not follow redirects.

    -noshownew:    don't show the source of every new pagelink found.
    
    Arguments that are interpreted by more bots:

    -lang:         specifies the language the bot is run on (e.g. -lang:de).
                   Overwrites the settings in username.dat


Two configuration options can be used to change the workings of this robot:

treelang_backlink: if set to True, all problems in foreign wikipedias will
                   be reported
treelang_log:      if set to True, all messages will be logged to a file
                   as well as being displayed to the screen.

Both these options are set to True by default. They can be changed through
the user-config.py configuration file.

If interwiki.py is terminated before it is finished, it will write a file
"interwiki.dump"; the program will read it if invoked with the
"-restore". option, and finish all the subjects in that list. Please check what
the last subject in the list is (say it is "Brilliant"), and to continue the
run, do: "python interwiki.py -autonomous -restore -start:Brilliant_0"

"""
#
# (C) Rob W.W. Hooft, 2003
# (C) Daniel Herding, 2004
#
# Distribute under the terms of the PSF license.
#
__version__ = '$Id$'
#
import sys, copy, re

import wikipedia, config, unequal, titletranslate

msg = {
    'da':('Tilf�jer','Fjerner','�ndrer'),
    'de':('Erg�nze','Entferne','�ndere'),
    'en':('Adding','Removing','Modifying'),
    'fr':('Ajoute','Retire','Modifie'),
    'nl':('Erbij','Eraf','Anders'),
    'no':('Tilfoeyer','Fjerner','Endrer'),
    }

class Global:
    """Container class for global settings.
       Use of globals outside of this is to be avoided."""
    always = False
    autonomous = False
    backlink = config.treelang_backlink
    bell = True
    confirm = False
    debug = True
    followredirect = True
    force = False
    forreal = True
    log = config.treelang_log
    minarraysize = 100
    maxquerysize = 60
    msglang = 'en'
    same = False
    shownew = True
    skip = {}
    untranslated = False
    untranslatedonly = False
    askhints = False
    
class Subject:
    """Class to follow the progress of a single 'subject' (i.e. a page with
       all its translations)"""
    def __init__(self, pl, hints = None):
        """Constructor. Takes as arguments the PageLink on the home wikipedia
           plus optionally a list of hints for translation"""
        # Remember the "origin page"
        self.inpl = pl
        # Mark the origin page as todo.
        self.todo = {pl:pl.code()}
        # Nothing has been done yet
        self.done = {}
        # Add the translations given in the hints.
        self.translate(hints)
        if globalvar.confirm:
            self.confirm = 1
        else:
            self.confirm = 0
        self.untranslated = None
        self.hintsasked = False

    def pl(self):
        """Return the PageLink on the home wikipedia"""
        return self.inpl
    
    def translate(self, hints = None):
        """Add the translation hints given to the todo list"""
        import titletranslate
        arr = {}
        titletranslate.translate(self.inpl, arr, same = globalvar.same, hints = hints)
        for pl in arr.iterkeys():
            self.todo[pl] = pl.code()

    def openCodes(self):
        """Return a list of language codes for all things we still need to do"""
        return self.todo.values()

    def willWorkOn(self, code):
        """By calling this method, you 'promise' this instance that you will
           work on any todo items in the language given by 'code'. This routine
           will return a list of pages that can be treated."""
        # Bug-check: Isn't there any work still in progress?
        if hasattr(self,'pending'):
            raise 'Cant start on %s; still working on %s'%(code,self.pending)
        # Prepare a list of suitable pages
        self.pending=[]
        for pl in self.todo.keys():
            if pl.code() == code:
                self.pending.append(pl)
                del self.todo[pl]
        # If there are any, return them. Otherwise, nothing is in progress.
        if self.pending:
            return self.pending
        else:
            del self.pending
            return None

    def conditionalAdd(self, pl, counter):
        """Add the pagelink given to the todo list, but only if we didn't know
           it before. If it is added, update the counter accordingly."""
        if (pl not in self.done and
            pl not in self.todo and
            pl not in self.pending):
            self.todo[pl] = pl.code()
            counter.plus(pl.code())
            #print "DBG> Found new to do:",pl.asasciilink()
            return True
        return False
        
    def workDone(self, counter):
        """This is called by a worker to tell us that the promised work
           was completed as far as possible. The only argument is an instance
           of a counter class, that has methods minus() and plus() to keep
           counts of the total work todo."""
        # Loop over all the pages that should have been taken care of
        for pl in self.pending:
            # Mark the page as done
            self.done[pl] = pl.code()
            # Register this fact at the todo-counter.
            counter.minus(pl.code())
            # Assume it's not a redirect
            isredirect = 0
            # Now check whether any interwiki links should be added to the
            # todo list.
            if unequal.bigger(self.inpl, pl):
                print "NOTE: %s is bigger than %s, not following references" % (pl, self.inpl)
            else:
                try:
                    iw = pl.interwiki()
                except wikipedia.IsRedirectPage,arg:
                    pl3 = wikipedia.PageLink(pl.code(),arg.args[0])
                    print "NOTE: %s is redirect to %s" % (pl.asasciilink(), pl3.asasciilink())
                    if pl == self.inpl:
                        # This is a redirect page itself. We don't need to
                        # follow the redirection.
                        isredirect = 1
                        # In this case we can also stop all hints!
                        for pl2 in self.todo:
                            counter.minus(pl2.code())
                        self.todo = {}
                        pass
                    elif not globalvar.followredirect:
                        print "NOTE: not following redirects."
                    elif unequal.unequal(self.inpl, pl3):
                        print "NOTE: %s is unequal to %s, not adding it" % (pl3, self.inpl)
                    else:
                        if self.conditionalAdd(pl3, counter):
                            if globalvar.shownew:
                                print "%s: %s gives new redirect %s"% (self.inpl.asasciiselflink(), pl.asasciilink(), pl3.asasciilink())
                except wikipedia.NoPage:
                    print "NOTE: %s does not exist" % pl.asasciilink()
                    #print "DBG> ",pl.urlname()
                    if pl == self.inpl:
                        # This is the home subject page.
                        # In this case we can stop all hints!
                        for pl2 in self.todo:
                            counter.minus(pl2.code())
                        self.todo = {}
                        pass
                except wikipedia.SubpageError:
                    print "NOTE: %s subpage does not exist" % pl.asasciilink()
                else:
                    if self.inpl == pl:
                        self.untranslated = (len(iw) == 0)
                        if globalvar.untranslatedonly:
                            # Ignore the interwiki links.
                            iw = ()
                    if pl.isEmpty():
                        print "NOTE: %s is empty; ignoring it and its interwiki links" % pl.asasciilink()
                        # Ignore the interwiki links
                        iw = ()
                    for pl2 in iw:
                      if unequal.unequal(self.inpl, pl2):
                          print "NOTE: %s is unequal to %s, not adding it" % (pl2, self.inpl)
                      else:   
                          if self.conditionalAdd(pl2, counter):
                              if globalvar.shownew:
                                  print "%s: %s gives new interwiki %s"% (self.inpl.asasciiselflink(), pl.asasciilink(), pl2.asasciilink())
                              
        # These pages are no longer 'in progress'
        del self.pending
        # Check whether we need hints and the user offered to give them
        if self.untranslated and not self.hintsasked:
            print "NOTE: %s does not have any interwiki links" % self.inpl.asasciilink()
        if (self.untranslated or globalvar.askhints) and not self.hintsasked and not isredirect:
            # Only once! 
            self.hintsasked = True
            if globalvar.untranslated:
                if globalvar.bell:
                    sys.stdout.write('\07')
                newhint = None
                while 1:
                    newhint = raw_input("Hint:")
                    if newhint and not ':' in newhint:
                        print "Please enter a hint like language:pagename"
                        #print "or type 'q' to stop generating new pages"
                        print "or type nothing if you do not have a hint"
                    elif not newhint:
                        break
                    else:
                        arr = {}
                        import titletranslate
                        titletranslate.translate(pl, arr, same = False,
                                                 hints = [newhint])
                        for pl in arr.iterkeys():
                            self.todo[pl] = pl.code()
                            counter.plus(pl.code())

    def isDone(self):
        """Return True if all the work for this subject has completed."""
        return len(self.todo) == 0

    def problem(self, txt):
        """Report a problem with the resolution of this subject."""
        print "ERROR: %s"%txt
        self.confirm += 1
        if globalvar.autonomous:
            f=open('autonomous_problem.dat', 'a')
            f.write("%s {%s}\n" % (self.inpl.asasciilink(), txt))
            f.close()

    def ask(self, askall, pl):
        if not askall:
            return True
        answer = ' '
        while answer not in 'yn':
            answer = raw_input('%s y/n? '%pl.asasciilink())
        return answer=='y'
    
    def assemble(self, returnonquestion = False, askall = False):
        new = {}
        for pl in self.done.keys():
            code = pl.code()
            if code == wikipedia.mylang and pl.exists() and not pl.isRedirectPage() and not pl.isEmpty():
                if pl != self.inpl:
                    err = 'Someone refers to %s with us' % pl.asasciilink()
                    if returnonquestion:
                        print "ERROR: %s"%err
                        if globalvar.bell:
                            sys.stdout.write('\07')
                        return None
                    self.problem(err)
                    if globalvar.autonomous:
                        return None
            elif pl.exists() and not pl.isRedirectPage():
                if new.has_key(code) and new[code] is None:
                    print "NOTE: Ignoring %s"%(pl.asasciilink())
                elif new.has_key(code) and new[code] != pl:
                    err = "'%s' as well as '%s'" % (new[code].asasciilink(), pl.asasciilink())
                    if returnonquestion:
                        print "ERROR: %s"%err
                        if globalvar.bell:
                            sys.stdout.write('\07')
                        return None
                    self.problem(err)
                    if globalvar.autonomous:
                        return None
                    # beep before asking question
                    if globalvar.bell:
		        sys.stdout.write('\07')
                    while 1:
                        answer = raw_input("Use (f)ormer or (l)atter or (n)either or (g)ive up?")
                        if answer.startswith('f'):
                            break
                        elif answer.startswith('l'):
                            new[pl.code()] = pl
                            break
                        elif answer.startswith('n'):
                            new[pl.code()] = None
                            break
                        elif answer.startswith('g'):
                            # Give up
                            return None
                elif code in ('zh-tw','zh-cn') and new.has_key('zh') and new['zh'] is not None:
                    print "NOTE: Ignoring %s, using %s"%(new['zh'].asasciilink(),pl.asasciilink())
                    if self.ask(askall, pl):
                        new['zh'] = None # Remove the global zh link
                        new[code] = pl # Add the more precise one
                elif code == 'zh' and (
                    (new.has_key('zh-tw') and new['zh-tw'] is not None) or
                    (new.has_key('zh-cn') and new['zh-cn'] is not None)):
                    print "NOTE: Ignoring %s"%(pl.asasciilink())
                    pass # do not add global zh if there is a specific zh-tw or zh-cn
                elif code not in new:
                    if self.ask(askall, pl):
                        new[code] = pl

        # Remove the neithers
        for k,v in new.items():
            if v is None:
                del new[k]

        return new
    
    def finish(self, sa = None):
        """Round up the subject, making any necessary changes. This method
           should be called exactly once after the todo list has gone empty.

           This contains a shortcut: if a subject array is given in the argument
           sa, just before submitting a page change to the live wikipedia it is
           checked whether we will have to wait. If that is the case, the sa will
           be told to make another get request first."""
        if not self.isDone():
            raise "Bugcheck: finish called before done"
        if self.inpl.isRedirectPage():
            return
        if not self.untranslated and globalvar.untranslatedonly:
            return
        if len(self.done) == 1:
            # No interwiki at all
            return
        print "======Post-processing %s======"%(self.inpl.asasciilink())
        # Assemble list of accepted interwiki links
        if globalvar.autonomous:
            new = self.assemble()
            if new == None: # There are questions
                return
        else:
            new = self.assemble(returnonquestion = True)
            if new == None: # There are questions
                new = self.assemble(askall = True)
                if new == None:
                    return # User said give up
            
        print "==status=="
        old={}
        try:
            for pl in self.inpl.interwiki():
                old[pl.code()] = pl
        except wikipedia.NoPage:
            print "BUG:", self.inpl.asasciilink(), "No longer exists?"
        ####
        mods, removing = compareLanguages(old, new)
        if not mods and not globalvar.always:
            print "No changes needed"
            if globalvar.backlink:
                self.reportBacklinks(new)
        else:
            if mods:
                print "Changes to be made:",mods
            oldtext = self.inpl.get()
            newtext = wikipedia.replaceLanguageLinks(oldtext, new)
            if globalvar.debug:
                showDiff(oldtext, newtext)
            if newtext == oldtext:
                if globalvar.backlink:
                    self.reportBacklinks(new)
            else:
                print "NOTE: Replace %s" % self.inpl.asasciilink()
                if globalvar.forreal:
                    # Determine whether we need permission to submit
                    ask = False
                    if removing:
                        self.problem('removing: %s'%(",".join(removing)))
                        ask = True
                    if globalvar.force:
                        ask = False
                    if globalvar.confirm:
                        ask = True
                    # If we need to ask, do so
                    if ask:
                        if globalvar.autonomous:
                            # If we cannot ask, deny permission
                            answer = 'n'
                        else:
                            if globalvar.bell:
                                sys.stdout.write('\07')
                            answer = raw_input('submit y/n ?')
                    else:
                        # If we do not need to ask, allow
                        answer = 'y'
                    if answer == 'y':
                        # Check whether we will have to wait for wikipedia. If so, make
                        # another get-query first.
                        if sa:
                            while wikipedia.get_throttle.waittime() + 2.0 < wikipedia.put_throttle.waittime():
                                print "NOTE: Performing a recursive query first to save time...."
                                qdone = sa.oneQuery()
                                if not qdone:
                                    # Nothing more to do
                                    break
                        print "NOTE: Updating live wikipedia..."
                        status, reason, data = self.inpl.put(newtext,
                                                             comment='robot '+mods)
                        if str(status) != '302':
                            print status, reason
                        else:
                            if globalvar.backlink:
                                self.reportBacklinks(new)

    def reportBacklinks(self, new):
        """Report missing back links. This will be called from finish() if
           needed."""
        for code in new.keys():
            pl = new[code]
            if not unequal.bigger(self.inpl, pl):
                shouldlink = new.values() + [self.inpl]
                linked = pl.interwiki()
                for xpl in shouldlink:
                    if xpl != pl and not xpl in linked:
                        for l in linked:
                            if l.code() == xpl.code():
                                print "WARNING:", pl.asasciiselflink(), "does not link to", xpl.asasciilink(), "but to", l.asasciilink()
                                break
                        else:
                            print "WARNING:", pl.asasciiselflink(), "does not link to", xpl.asasciilink()
                # Check for superfluous links
                for xpl in linked:
                    if not xpl in shouldlink:
                        # Check whether there is an alternative page on that language.
                        for l in shouldlink:
                            if l.code() == xpl.code():
                                # Already reported above.
                                break
                        else:
                            # New warning
                            print "WARNING:", pl.asasciiselflink(), "links to incorrect", xpl.asasciilink()
    
class SubjectArray:
    """A class keeping track of a list of subjects, controlling which pages
       are queried from which languages when."""
    
    def __init__(self):
        """Constructor. We always start with empty lists."""
        self.subjects = []
        self.counts = {}
        self.generator = None

    def add(self, pl, hints = None):
        """Add a single subject to the list"""
        subj = Subject(pl, hints = hints)
        self.subjects.append(subj)
        for code in subj.openCodes():
            # Keep correct counters
            self.plus(code)

    def setGenerator(self, generator):
        """Add a generator of subjects. Once the list of subjects gets
           too small, this generator is called to produce more PageLinks"""
        self.generator = generator

    def dump(self, fn):
        f = open(fn, 'w')
        for subj in self.subjects:
            f.write(subj.pl().asasciilink()+'\n')
        f.close()
        
    def generateMore(self, number):
        """Generate more subjects. This is called internally when the
           list of subjects becomes to small, but only if there is a
           generator"""
        fs = self.firstSubject()
        if fs:
            print "NOTE: The first unfinished subject is:", fs.pl().asasciilink()
        print "NOTE: Number of pages queued is %d, trying to add %d more."%(
            len(self.subjects), number)
        for i in range(number):
            try:
                pl=self.generator.next()
                while pl in globalvar.skip:
                    pl=self.generator.next()
                self.add(pl)
            except StopIteration:
                self.generator = None
                break

    def firstSubject(self):
        """Return the first subject that is still being worked on"""
        if self.subjects:
            return self.subjects[0]
        
    def maxOpenCode(self):
        """Return the code of the foreign language that has the most
           open queries plus the number. If there is nothing left, return
           None, 0. Only languages that are TODO for the first Subject
           are returned."""
        max = 0
        maxlang = None
        oc = self.firstSubject().openCodes()
        if not oc:
            # The first subject is done. This might be a recursive call made because we
            # have to wait before submitting another modification to go live. Select
            # any language from counts.
            oc = self.counts.keys()
        if wikipedia.mylang in oc:
            return wikipedia.mylang
        for lang in oc:
            count = self.counts[lang]
            if count > max:
                max = count
                maxlang = lang
        return maxlang

    def selectQueryCode(self):
        """Select the language code the next query should go out for."""
        # How many home-language queries we still have?
        mycount = self.counts.get(wikipedia.mylang,0)
        # Do we still have enough subjects to work on for which the
        # home language has been retrieved? This is rough, because
        # some subjects may need to retrieve a second home-language page!
        if len(self.subjects) - mycount < globalvar.minarraysize:
            # Can we make more home-language queries by adding subjects?
            if self.generator and mycount < globalvar.maxquerysize:
                self.generateMore(globalvar.maxquerysize - mycount)
            # If we have a few, getting the home language is a good thing.
            if self.counts[wikipedia.mylang] > 4:
                return wikipedia.mylang
        # If getting the home language doesn't make sense, see how many 
        # foreign page queries we can find.
        return self.maxOpenCode()
    
    def oneQuery(self):
        """Perform one step in the solution process"""
        # First find the best language to work on
        code = self.selectQueryCode()
        if code == None:
            print "NOTE: Nothing left to do"
            return False
        # Now assemble a reasonable list of pages to get
        group = []
        plgroup = []
        for subj in self.subjects:
            # Promise the subject that we will work on the code language
            # We will get a list of pages we can do.
            x = subj.willWorkOn(code)
            if x:
                plgroup.extend(x)
                group.append(subj)
                if len(plgroup)>=globalvar.maxquerysize:
                    break
        if len(plgroup) == 0:
            print "NOTE: Nothing left to do 2"
            return False
        # Get the content of the assembled list in one blow
        try:
            wikipedia.getall(code, plgroup)
        except wikipedia.SaxError:
            # Ignore this error, and get the pages the traditional way.
            pass
        # Tell all of the subjects that the promised work is done
        for subj in group:
            subj.workDone(self)
        return True
        
    def queryStep(self):
        self.oneQuery()
        # Delete the ones that are done now.
        for i in range(len(self.subjects)-1, -1, -1):
            subj = self.subjects[i]
            if subj.isDone():
                subj.finish(self)
                del self.subjects[i]
    
    def isDone(self):
        """Check whether there is still more work to do"""
        return len(self) == 0 and self.generator is None

    def plus(self, code): 
        """This is a routine that the Subject class expects in a counter"""
        try:
            self.counts[code] += 1
        except KeyError:
            self.counts[code] = 1

    def minus(self, code):
        """This is a routine that the Subject class expects in a counter"""
        self.counts[code] -= 1
        
    def run(self):
        """Start the process until finished"""
        while not self.isDone():
            self.queryStep()

    def __len__(self):
        return len(self.subjects)

def showDiff(oldtext, newtext):
    import difflib
    sep = '\r\n'
    ol = oldtext.split(sep)
    if len(ol) == 1:
        sep = '\n'
        ol = oldtext.split(sep)
    nl = newtext.split(sep)
    for line in difflib.ndiff(ol,nl):
        if line[0] in ['+','-']:
            print repr(line)[2:-1]
    
def compareLanguages(old, new):
    removing = []
    adding = []
    modifying = []
    for code in old.keys():
        if code not in new:
            # Zh is allowed to be removed if it is replaced by both zh-cn and
            # zh-tw.  Do not call such a removal a removal but a modification.
            if code == 'zh' and 'zh-cn' in new and 'zh-tw' in new:
                modifying.append(code)
            else:
                removing.append(code)
        elif old[code] != new[code]:
            modifying.append(code)

    for code2 in new.keys():
        if code2 not in old:
            adding.append(code2)
    s = ""
    if adding:
        s = s + " %s:" % (msg[globalvar.msglang][0]) + ",".join(adding)
    if removing: 
        s = s + " %s:" % (msg[globalvar.msglang][1]) + ",".join(removing)
    if modifying:
        s = s + " %s:" % (msg[globalvar.msglang][2]) + ",".join(modifying)
    return s,removing

def ReadWarnfile(fn, sa):
    import re
    R=re.compile(r'WARNING: ([^\[]*):\[\[([^\[]+)\]\]([^\[]+)\[\[([^\[]+):([^\[]+)\]\]')
    f=open(fn)
    hints={}
    for line in f.readlines():
        m=R.search(line)
        if m:
            #print "DBG>",line
            if m.group(1)==wikipedia.mylang:
                #print m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
                if not hints.has_key(m.group(2)):
                    hints[m.group(2)]=[]
                #print m.group(3)
                if m.group(3) != ' links to incorrect ':
                    try:
                        hints[m.group(2)].append('%s:%s'%(m.group(4),wikipedia.link2url(m.group(5),m.group(4))))
                    except wikipedia.Error:
                        print "DBG> Failed to add", line
                #print "DBG> %s : %s" % (m.group(2), hints[m.group(2)])
    f.close()
    for pagename in hints:
        pl = wikipedia.PageLink(wikipedia.mylang, pagename)
        sa.add(pl, hints = hints[pagename])

#===========
        
globalvar=Global()
    
if __name__ == "__main__":
    inname = []
    hints = []
    start = None
    number = None
    skipfile = None

    sa=SubjectArray()

    for arg in sys.argv[1:]:
        wikipedia.argHandler(arg)

    for arg in sys.argv[1:]:
        if wikipedia.argHandler(arg):
            pass
        elif arg == '-force':
            globalvar.force = True
        elif arg == '-always':
            globalvar.always = True
        elif arg == '-same':
            globalvar.same = True
        elif arg == '-untranslated':
            globalvar.untranslated = True
        elif arg == '-untranslatedonly':
            globalvar.untranslated = True
            globalvar.untranslatedonly = True
        elif arg == '-askhints':
            globalvar.untranslated = True
            globalvar.untranslatedonly = False
            globalvar.askhints = True
        elif arg.startswith('-hint:'):
            hints.append(arg[6:])
        elif arg.startswith('-warnfile:'):
            ReadWarnfile(arg[10:], sa)
        elif arg == '-name':
            globalvar.same = 'name'
        elif arg == '-confirm':
            globalvar.confirm = True
        elif arg == '-autonomous':
            globalvar.autonomous = True
        elif arg == '-noshownew':
            globalvar.shownew = False
        elif arg == '-nolog':
            globalvar.log = False
        elif arg == '-nobacklink':
            globalvar.backlink = False
        elif arg == '-noredirect':
            globalvar.followredirect = False
        elif arg.startswith('-years'):
            # Look if user gave a specific year at which to start
            # Must be a natural number or negative integer.
            if len(arg) > 7 and (arg[7:].isdigit() or (arg[7] == "-" and arg[8:].isdigit())):
                startyear = int(arg[7:])
            else:
                startyear = 1
            print "Starting with year %d" %startyear
            for i in range(startyear,2050):
                if i % 100 == 0:
                    print "Preparing %d..." % i
                # For years BC, append language-dependent text, e.g. "v. Chr."
                # This text is read from titletranslate.py
                if i < 0:
                    current_year = (titletranslate.yearBCfmt[wikipedia.mylang]) % (-i)
                else:
                    current_year = str(i)
                # There is no year 0
                if i != 0:
                    sa.add(wikipedia.PageLink(wikipedia.mylang, current_year))
            globalvar.followredirect = False
        elif arg == '-nobell':
            globalvar.bell = False
        elif arg == '-test':
            sa.add(wikipedia.PageLink(wikipedia.mylang, 'Scheikunde'))
            sa.add(wikipedia.PageLink(wikipedia.mylang, 'Wiskunde'))
            sa.add(wikipedia.PageLink(wikipedia.mylang, 'Natuurkunde'))
        elif arg.startswith('-skipfile:'):
            skipfile = arg[10:]
        elif arg == '-restore':
            for pl in wikipedia.PageLinksFromFile('interwiki.dump'):
                sa.add(pl)
        elif arg.startswith('-file:'):
            for pl in wikipedia.PageLinksFromFile(arg[6:]):
                sa.add(pl)
        elif arg.startswith('-start:'):
            start = arg[7:]
        elif arg.startswith('-number:'):
            number = int(arg[8:])
        else:
            inname.append(arg)

    if msg.has_key(wikipedia.mylang):
        globalvar.msglang = wikipedia.mylang

    if globalvar.log:
        import logger
        sys.stdout = logger.Logger(sys.stdout, filename = 'treelang.log')

    unequal.read_exceptions()
    
    if skipfile:
        for pl in wikipedia.PageLinksFromFile(skipfile):
            globalvar.skip[pl] = None

    if start:
        if number:
            print "Treating %d pages starting at %s" % (number, start)
            i = 0
            for pl in wikipedia.allpages(start = start):
                sa.add(pl)
                i += 1
                if i >= number:
                    break
        else:
            print "Treating pages starting at %s" % start
            sa.setGenerator(wikipedia.allpages(start = start))

    inname = '_'.join(inname)
    if sa.isDone() and not inname:
        inname = raw_input('Which page to check:')

    if inname:
        inpl = wikipedia.PageLink(wikipedia.mylang, inname)
        sa.add(inpl, hints = hints)

    try:
        sa.run()
    except KeyboardInterrupt:
        sa.dump('interwiki.dump')
    except:
        sa.dump('interwiki.dump')
        raise









