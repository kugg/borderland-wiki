#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Externals modules automatic setup checker and installer for various OS.
"""

#
# (C) DrTrigon, 2013
# (C) Pywikipedia team, 2013
#
# Distributed under the terms of the MIT license.
#
# Strongly inspired by files beeing part of VisTrails distribution
#   utils/installbundle.py
#   utils/requirements.py
# Copyright (C) 2006-2010 University of Utah. All rights reserved.
# GNU General Public License version 2.0 by the Free Software Foundation
#
__version__ = '$Id$'
#


# External dependencies for the compat repository. Please confer the docu at
# https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation#Dependencies and
# 'externals/README' also.
# The very essential packages are PRE-INSTALLED (e.g. 'BeautifulSoup.py'),
# please make sure to match/sync them with the list here. Best is to first
# update the PACKAGE in the list here and then use:
# >>> import wikipedia, externals
# >>> externals.check_setup('PACKAGE')
# in order to to pull the correct version easily it into the repo for commit.
#
# supports: 0. git submodule
#           1. package management system (yum, apt-get, ...)
#           2. download from url (e.g. archive, svn or git repo)
#           3. checkout from mercurial repo ('hg clone ...' if no url is
#              available) - not needed at the moment
#           (what about python eggs?!)
# dependencies: (git, python)
#               yum, apt-get or whatever your system uses
#               mercurial (hg) / subversion (svn)
#               patch (unix/linux & gnuwin32 version/flavour)
modules_needed = {
          'patch.exe': ({},  # for win32 only, unix/linux is already equipped with a patch tool
                        {  'url': 'https://downloads.sourceforge.net/project/gnuwin32/patch/2.5.9-7/patch-2.5.9-7-bin.zip',
                          'path': 'bin/patch.exe'},
                        {}),  # OK
            'crontab': ({},
                        #{  'url': 'https://github.com/josiahcarlson/parse-crontab/archive/master.zip',
                        #  'path': 'parse-crontab-master/crontab',}),  # OK
                        {  'url': 'https://github.com/josiahcarlson/parse-crontab/archive/1ec538ff67df6a207993a6c5b6988f4f628c5776.zip',
                          'path': 'parse-crontab-1ec538ff67df6a207993a6c5b6988f4f628c5776/crontab',},
                        {}),  # OK
                'odf': ({},
                        #{  'url': 'https://pypi.python.org/packages/source/o/odfpy/odfpy-0.9.6.tar.gz',
                        #  'path': 'odfpy-0.9.6/odf',}),  # OK
                        {  'url': 'https://pypi.python.org/packages/source/o/odfpy/odfpy-0.9.4.tar.gz',
                          'path': 'odfpy-0.9.4/odf'},
                        {}),  # OK
           'openpyxl': ({},
                        {  'url': 'https://bitbucket.org/ericgazoni/openpyxl/get/1.5.6.tar.gz',
                          'path': 'ericgazoni-openpyxl-e5934500ffac/openpyxl'},
                        {}),  # OK
# git submodule: see '.gitmodules' files
#          'spelling': $ git submodule add https://gerrit.wikimedia.org/r/p/pywikibot/spelling.git externals/spelling
   'BeautifulSoup.py': ({'linux-fedora': ['python-BeautifulSoup'],
                         'linux-ubuntu': ['python-beautifulsoup']},
                        {  'url': 'https://pypi.python.org/packages/source/B/BeautifulSoup/BeautifulSoup-3.2.0.tar.gz',
                          'path': 'BeautifulSoup-3.2.0/BeautifulSoup.py'},
                        {}),  # PRE-INSTALLED
             'irclib': ({'linux-fedora': ['python-irclib'],
                         'linux-ubuntu': ['python-irclib']},
                        {},  # http://python-irclib.sourceforge.net/
                        {}),  # OK
   'mwparserfromhell': ({},
                        {  'url': 'https://github.com/earwig/mwparserfromhell/archive/v0.2.zip',
                        #{  'url': 'https://github.com/earwig/mwparserfromhell/archive/master.zip',
                          'path': 'mwparserfromhell-0.2/mwparserfromhell'},
                        {}),  # OK
          'colormath': ({'linux-fedora': [],
                         'linux-ubuntu': ['python-colormath'],},
                        {  'url': 'https://github.com/gtaylor/python-colormath/archive/master.zip',
                          'path': 'python-colormath-master/colormath',},
                        {}),  # OK
               'jseg': ({},
                        {  'url': 'http://vision.ece.ucsb.edu/segmentation/jseg/software/jseg.zip',
                          'path': 'jseg',
                         #$ diff -Nau --exclude="*.o" --exclude="*.pyc" --exclude="segdist_cpp*" TEST_jseg/ jseg/ > patch-jseg
                         'patch': 'patch-jseg'},
                        {}),  # OK
       'jseg/jpeg-6b': ({},
                        {  'url': 'http://vision.ece.ucsb.edu/segmentation/jseg/software/jpeg-6b.zip',
                          'path': 'jpeg-6b',},
                        {}),  # OK
              '_mlpy': ({},
                        {  'url': 'https://downloads.sourceforge.net/project/mlpy/mlpy%203.5.0/mlpy-3.5.0.tar.gz',
                          'path': 'mlpy-3.5.0/mlpy'},
                        {}),  # OK
           '_music21': ({},
                        {  'url': 'https://music21.googlecode.com/files/music21-1.4.0.tar.gz',
                          'path': 'music21-1.4.0',
                         #$ diff -Naur --exclude="*.pyc" TEST__music21/ _music21/ > patch-music21
                         'patch': 'patch-music21'},
                        {}),  # OK
# TODO: vvv (future; enable for and use in 'catimages.py')
# TODO: needs an '__init__.py' in order to download models according to ../_ocropus/ocropy/models/README and finish setup/install (post-install)
           '_ocropus': ({},
                        {  'url': 'https://ocropus.googlecode.com/archive/ocropus-0.6.zip',
                          'path': 'ocropus-1598de2c16ec',},
                        {}),  # OK
    '_ocropus/ocropy': ({},
                        {  'url': 'https://ocropy.ocropus.googlecode.com/archive/7888246ee98dd6e5ee8002dc95d71f1fdabcc05f.zip',
                          'path': 'ocropy.ocropus-7888246ee98d',
                         #$ diff -Naur --exclude=".hg" --exclude=".pynative" --exclude="Notebooks" --exclude="OLD" --exclude="models" --exclude="tests" --exclude="*.pyc" --exclude="*.jpg" TEST__ocropus/ _ocropus/ > patch-ocropy
                         'patch': 'patch-ocropy'},
                        {}),  # OK
# git submodule: see '.gitmodules' files
#             'opencv': $ git submodule add https://gerrit.wikimedia.org/r/pywikibot/opencv.git externals/opencv
#                       $ svn propedit svn:externals externals/opencv/haarcascades/haartraining/
#                         HaarTraining https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/HaarTraining
#                         HaarTraining.tar.gz https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/HaarTraining.tar.gz
#                         convert_cascade.c https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/convert_cascade.c
#                         create_pos_neg.py https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/create_pos_neg.py
#                         createtestsamples.pl https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/createtestsamples.pl
#                         createtrainsamples.pl https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/createtrainsamples.pl
'opencv/haarcascades': ({},
                        {  'url': 'https://github.com/wikimedia/pywikibot-bots-drtrigonbot/raw/master/externals/haarcascades-full.tar.gz',
                          'path': 'haarcascades'},
                        {}),  # OK
# git submodule: see '.gitmodules' files
#       'pycolorname': $ git submodule add https://gerrit.wikimedia.org/r/pywikibot/pycolorname.git externals/pycolorname
             'pydmtx': ({'linux-fedora': ['python-libdmtx'],
                         'linux-ubuntu': ['libdmtx-dev']},
                        {  'url': 'https://github.com/dmtx/dmtx-wrappers/archive/master.zip',
                          'path': 'dmtx-wrappers-master/python',
                         #$ diff -Nau --exclude="*.pyc" TEST_pydmtx/ pydmtx/ > patch-pydmtx
                         'patch': 'patch-pydmtx'},
                        {}),  # OK
             'py_w3c': ({},
                        {  'url': 'https://bitbucket.org/nmb10/py_w3c/downloads/py_w3c-v0.1.0.tar.gz',
                          'path': 'py_w3c-0.1.0/py_w3c'},
                        {}),  # OK
# TODO: vvv (future; enable for and use in 'catimages.py')
# TODO: needs an '__init__.py' in order to handle complex installation... compile needed? (post-install)
               'slic': ({},
#                        {  'url': 'http://ivrg.epfl.ch/files/content/sites/ivrg/files/supplementary_material/RK_SLICsuperpixels/SLICSuperpixelsAndSupervoxelsCode.zip',
#                          'path': 'SLICSuperpixelsAndSupervoxelsCode/SLICSuperpixels',},
#                        {}),  # OK
#        'slic/python': ({},
#                        {  'url': 'https://github.com/amueller/slic-python/archive/9aede5ef38495e2dbd0ca126821b7dd7e0e5304f.zip',
#                          'path': 'slic-python-9aede5ef38495e2dbd0ca126821b7dd7e0e5304f',},
#                         #'patch': 'patch-slic',},
#                        {}),  # OK
                        {  'url': 'https://github.com/wikimedia/pywikibot-bots-drtrigonbot/raw/master/externals/amueller-slic-python-9aede5e-with-SLICSuperpixelsAndSupervoxelsCode.tar.gz',
                          'path': 'slic'},
                        {}),  # OK
              '_zbar': ({'linux-fedora': ['zbar'],
                         'linux-ubuntu': ['python-zbar']},
                        {  'url': 'https://pypi.python.org/packages/source/z/zbar/zbar-0.10.tar.bz2',
                          'path': 'zbar-0.10',
                         #$ diff -Nau --exclude="*.pyc" TEST__zbar/ _zbar/ > patch-zbar
                         'patch': 'patch-zbar'},
                        {}),  # OK
# TODO: vvv (future; '_bob' & 'xbob_flandmark' might be used some day in 'catimages.py' - but is quite big...)
               '_bob': ({},
                        {  'url': 'https://www.idiap.ch/software/bob/packages/bob-1.1.2.zip',
                          'path': 'bob-1.1.2',
                         #$ diff -Naur --exclude="*.pyc" --exclude="build" --exclude="bob.egg-info" TEST__bob/ _bob/ > patch-bob
                         'patch': 'patch-bob',},
                        {}),  # OK
# TODO: needs an '__init__.py' in order to handle complex compilation, dependent on '_bob'... (post-install)
     'xbob_flandmark': ({},
                        {  'url': 'https://pypi.python.org/packages/source/x/xbob.flandmark/xbob.flandmark-1.0.9.zip',
                          'path': 'xbob.flandmark-1.0.9',
                         #$ diff -Naur --exclude="*.pyc" --exclude="*.so" --exclude="bin" --exclude="build" --exclude="develop-eggs" --exclude="eggs" --exclude="parts" TEST_xbob_flandmark/ xbob_flandmark/ > patch-xbob-flandmark
                         'patch': 'patch-xbob-flandmark',},
                        {}),  # OK
}

modules_order = ['crontab', 'odf', 'openpyxl', 'BeautifulSoup.py', 'irclib',
                 'mwparserfromhell', 'colormath', 'jseg', 'jseg/jpeg-6b',
                 '_mlpy', '_music21', '_ocropus', 'opencv/haarcascades',
                 'pydmtx', 'py_w3c', 'slic', '_zbar', '_bob', 'xbob_flandmark']

_patch_permission = None


import os
import sys
import inspect
import wikipedia as pywikibot  # sets externals path
#from pywikibot.comms import http

# allow imports from externals
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


### BEGIN of VisTrails inspired and copied code ###

def has_logger():
    #return hasattr(sys.modules['wikipedia'], 'logger')
    return hasattr(pywikibot, 'logger')


# TODO: solve properly because this is just a work-a-round, because module
# externals get imported in wikipedia.py before logger is setup properly, which
# should be changed! (meanwhile this is acceptable because code here should be
# executed once only...)
def lowlevel_warning(text):
    if has_logger():
        pywikibot.warning(text)
    else:
        print "WARNING:", text


def guess_system():
    import platform
    return ("%s-%s" % (platform.system(), platform.dist()[0])).lower()


def show_question(module):
    lowlevel_warning("Required package missing: %s\n"
                     "This package is not installed, but required by the file"
                     " '%s'." % (module, inspect.stack()[2][1]))
    lowlevel_warning("For more and additional information, please confer:\n"
                     "https://www.mediawiki.org/wiki/Manual:Pywikibot/"
                     "Installation#Dependencies")
    options = [(i+1) for i, item in enumerate(modules_needed[module]) if item]
    options += [0, 's', '']
    options.sort()
    options_msg = ("""There are multiple ways to solve this:
RECOMMENDED for     admins: always option [0] or the next available (e.g. [1])
RECOMMENDED for non-admins: always option [2] (if available)
0: automatically determine the best of the following methods (may need
   administrator privileges)
""")
    if 1 in options:
        options_msg += ("1: install the package using the OS package"
                        " management system like yum\n"
                        "   or apt (needs administrator privileges)\n")
    if 2 in options:
        options_msg += ("2: download the package from its source URL and"
                        " install it locally into\n"
                        "   the pywikipedia package externals directory\n")
    if 3 in options:
        options_msg += ("3: download the package from its mercurial repo and"
                        " install it locally into\n"
                        "   the pywikipedia package externals directory\n")
    options_msg += "s: SKIP and solve manually"
    lowlevel_warning(options_msg)
    v = None
    while (v not in options):
        lowlevel_warning("Please choose [%s, s - default]: "
                         % (", ".join(map(str, options[:-2]))))
        v = raw_input().lower()
        try:
            v = int(v)
        except:
            pass
    return v


def show_patch_question():
    global _patch_permission
    if _patch_permission is None:
        lowlevel_warning(
            "Give externals permission to execute the patch command?"
            " [y(es), n(o) - default]: ")
        v = raw_input().upper()
        _patch_permission = (v == 'Y') or (v == 'YES')
    return _patch_permission


def python_module_exists(module_name):
    """python_module_exists(module_name): Boolean.
    Returns if python module of given name can be safely imported.

    """

    module_name = module_name.replace(u'.py', u'')
    module_name = module_name[1:] if module_name[0] == u'_' else module_name

    try:
        sys.modules[module_name]
        return True
    except KeyError:
        pass
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def linux_ubuntu_install(package_name):
    cmd = 'apt-get install -y'

    if type(package_name) == str:
        cmd += ' ' + package_name
    elif type(package_name) == list:
        for package in package_name:
            if type(package) != str:
                raise TypeError("Expected string or list of strings")
            cmd += ' ' + package

    sucmd = "sudo %s" % cmd
    result = os.system(sucmd)
    return (result == 0)  # 0 indicates success


def linux_fedora_install(package_name):
    cmd = 'yum -y install'

    if type(package_name) == str:
        cmd += ' ' + package_name
    elif type(package_name) == list:
        for package in package_name:
            if type(package) != str:
                raise TypeError("Expected string or list of strings")
            cmd += ' ' + package

    sucmd = "su -c'%s'" % cmd
    result = os.system(sucmd)
    return (result == 0)


def linux_install(dependency_dictionary):
    """ Tries to import a python module. If unsuccessful, tries to install
    the appropriate bundle and then reimport. py_import tries to be smart
    about which system it runs on.

    """

    # Ugly fix to avoid circular import
    distro = guess_system()
    if not distro in dependency_dictionary:
        return False
    else:
        files = dependency_dictionary[distro]
        lowlevel_warning('Installing package(s) "%s"' % files)
        func = distro.replace('-', '_') + '_install'
        lowlevel_warning("Externals will need administrator privileges, and"
                         " you might get asked for the administrator"
                         " password. This prompt can be skipped with [Ctrl]+"
                         "[c] or [Enter].")
        if files and (func in globals()):
            callable_ = globals()[func]
            return callable_(files)
        else:
            return False


def sunos_install(dependency_dictionary):
    lowlevel_warning(u'Not implemented yet, use download mode (2) instead.')
    return False    # skip this in order to trigger 'download_install' next


def windows_install(dependency_dictionary):
    lowlevel_warning(
        u'Not available in windows OS, use download mode (2) instead.')
    return False    # skip this in order to trigger 'download_install' next

### END of VisTrails inspired and copied code   ### ### ### ### ### ### ### ###


def download_install(package, module, path):
    if not package:
        return
    lowlevel_warning(u'Download package "%s" from %s'
                     % (module, package['url']))
    import mimetypes
    import urllib2
    for i in range(3):
        response = urllib2.urlopen(package['url'])
        #response = http.request(pywikibot.getSite(), package['url'],
        #                        no_hostname = True, back_response = True)[0]
        if 'Content-Length' in response.headers:
            size = response.headers['Content-Length']
            break
        if response.headers.get('Transfer-Encoding', '') == 'chunked':
            size = '<unknown>'
            break
        lowlevel_warning(u'Could not retrieve data, re-trying ...')
    lowlevel_warning(u'Size of download: %s byte(s)' % size)
    #mime = response.headers['Content-Type'].lower().split('/')
    mime = mimetypes.guess_type(package['url'],
                                strict=True)[0].lower().split('/')
    lowlevel_warning(u'MIME type: %s' % mime)

    lowlevel_warning(u'Extract package "%s" to %s.'
                     % (module, os.path.join(path, module)))
    if len(mime) > 1:
        import StringIO
        if mime[1] in ['zip', 'x-zip-compressed']:
            import zipfile
            arch = zipfile.ZipFile(StringIO.StringIO(response.read()))
        elif mime[1] == 'x-tar':
            import tarfile
            arch = tarfile.open(fileobj=StringIO.StringIO(response.read()))
        else:
            raise NotImplementedError(u'Not implemented mime type %s'
                                      % mime[1])
        arch.extractall(os.path.join(path, '__setup_tmp/'))
        arch.close()
        import shutil
        shutil.move(os.path.join(path, '__setup_tmp/', package['path']),
                    os.path.join(path, module))
        shutil.rmtree(os.path.join(path, '__setup_tmp/'))

        result = 0
        if 'patch' in package:
            if sys.platform == 'win32':
                if not check_setup('patch.exe'):
                    result = -1
            if result == 0 and show_patch_question():
                lowlevel_warning(u'Applying patch to %s in order to finish'
                                 u' the installation of package "%s".'
                                 % (os.path.join(path, module), module))
                if sys.platform == 'win32':
                    cmd = '%s -p0 -d %s -i %s --binary' \
                          % (os.path.join(path, 'patch.exe'), path,
                             os.path.join(path, package['patch']))
                else:              # unix/linux, (mac too?)
                    cmd = '%s -p0 -d %s < %s' \
                          % ('patch', path,
                             os.path.join(path, package['patch']))
                result = os.system(cmd)

        lowlevel_warning(u'Package "%s" installed to %s.'
                         % (module, os.path.join(path, module)))
        return (result == 0)


def mercurial_repo_install(package, module, path):
    if package:
        cmd = 'hg clone'
        lowlevel_warning(u'Mercurial clone "%s" from %s'
                         % (module, package['url']))
        cmd += " -r %s %s %s" % (package['rev'], package['url'],
                                 os.path.join(path, module))
        result = os.system(cmd)
        return (result == 0)


def check_setup(m):
    path = os.path.dirname(os.path.abspath(os.path.join(os.curdir, __file__)))
    mf = os.path.join(path, m)

    # search missing module
    if python_module_exists(m):
        return
    if os.path.exists(mf):
        return

    sel = show_question(m)

    # install the missing module
    dist = guess_system()
    func = dist.split(u'-')[0] + '_install'
    if sel in [0, 1]:
        lowlevel_warning(
            u'(1) Trying to install by use of "%s" package management system:'
            % dist)
        if (func in globals()) and globals()[func](modules_needed[m][0]):
            return sel
    if sel in [0, 2]:
        lowlevel_warning(u'(2) Trying to install by download from source URL:')
        if download_install(modules_needed[m][1], m, path):
            return sel
    if sel in [0, 3]:
        lowlevel_warning(u'(3) Trying to install by use of mercurial:')
        if (len(modules_needed[m]) > 2) and \
           mercurial_repo_install(modules_needed[m][2], m, path):
            return sel
    if sel in range(4):
        lowlevel_warning(u'No suitable package could be found nor installed!')

    lowlevel_warning(u'Several scripts might fail, if the modules are not'
                     u' installed as needed! You can either install them'
                     u' by yourself to the system or extract them into the'
                     u' externals/ directory. If you do not install them, this'
                     u' script will ask you again next time when executed.')


def check_setup_all():
    for m in modules_order:
        check_setup(m)
