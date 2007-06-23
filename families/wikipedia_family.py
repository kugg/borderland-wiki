# -*- coding: utf-8  -*-

import urllib
import family, config

__version__ = '$Id$'

# The Wikimedia family that is known as Wikipedia, the Free Encyclopedia

class Family(family.Family):

    def __init__(self):
        family.Family.__init__(self)
        self.name = 'wikipedia'

        self.langs = {
            'dk':'da.wikipedia.org',
            'jp':'ja.wikipedia.org',
            'minnan':'zh-min-nan.wikipedia.org',
            'nb':'no.wikipedia.org',
            'test':'test.wikipedia.org',
            'tokipona':'tokipona.wikipedia.org',
            'zh-cn':'zh.wikipedia.org',
            'zh-tw':'zh.wikipedia.org',
            'zh-classic': 'zh-classical.wikipedia.org'
            # database thinks 'zh-classical' is 'zh-classic' as field type is varchar(10)
            }
        for lang in self.knownlanguages:
            if lang not in self.langs:
                self.langs[lang] = lang+'.wikipedia.org'

        # Override defaults
        self.namespaces[2]['cs'] = u'Wikipedista'
        self.namespaces[3]['cs'] = u'Wikipedista diskuse'

        # Most namespaces are inherited from family.Family.
        self.namespaces[4] = {
            '_default': [u'Wikipedia', self.namespaces[4]['_default']],
            'ar': u'ويكيبيديا',
            'ast':u'Uiquipedia',
            'az': u'Vikipediya',
            'be': u'Вікіпедыя',
            'be-x-old': u'Вікіпэдыя',
            'bpy': u'উইকিপিডিয়া',
            'bg': u'Уикипедия',
            'bn': u'উইকিপেডিয়া',
            'ca': u'Viquipèdia',
            'cs': u'Wikipedie',
            'csb': u'Wiki',
            'cu': u'Википедї',
            'cv': u'Википеди',
            'cy': u'Wicipedia',
            'el': u'Βικιπαίδεια',
            'eo': u'Vikipedio',
            'et': u'Vikipeedia',
            'fa': u'ویکی‌پدیا',
            'fr': u'Wikipédia',
            'fur':u'Vichipedie',
            'fy': u'Wikipedy',
            'ga': u'Vicipéid',
            'gu': u'વિકિપીડિયા',
            'he': u'ויקיפדיה',
            'hi': u'विकिपीडिया',
            'hr': u'Wikipedija',
            'hsb': u'Wikipedija',
            'hu': u'Wikipédia',
            'ka': u'ვიკიპედია',
            'kk': u'Уикипедия',
            'ko': u'위키백과',
            'ku': u'Wîkîpediya',
            'la': u'Vicipaedia',
            'mk': u'Википедија',
            'ml': u'വിക്കിപീഡിയ',
            'mt': u'Wikipedija',
            'nds-nl': u'Wikipedie',
            'new': u'विकिपिडिया',
            'nv': u'Wikiibíídiiya',
            'oc': u'Wikipèdia',
            'pa': u'ਵਿਕਿਪੀਡਿਆ',
            'rmy':u'Vikipidiya',
            'ru': u'Википедия',
            'sk': u'Wikipédia',
            'sl': u'Wikipedija',
            'sr': u'Википедија',
            'ta': [u'Wikipedia', u'விக்கிபீடியா'],  # Very strange - the localized version is not the main one
            'te': u'వికీపీడియా',
            'tg': u'Википедиа',
            'th': u'วิกิพีเดีย',
            'tr': u'Vikipedi',
            'uk': u'Вікіпедія',
            'ur': u'منصوبہ',
            'vo': u'Vükiped',
            'yi': u'װיקיפּעדיע',
        }

        self.namespaces[5] = {
            '_default': [u'Wikipedia talk', self.namespaces[5]['_default']],
            'ab': u'Обсуждение Wikipedia',
            'af': u'WikipediaBespreking',
            'af': u'Wikipediabespreking',
            'als': u'Wikipedia Diskussion',
            'an': u'Descusión Wikipedia',
            'ar': u'نقاش ويكيبيديا',
            'ast': u'Uiquipedia discusión',
            'av': u'Обсуждение Wikipedia',
            'ay': u'Wikipedia Discusión',
            'az': u'Vikipediya müzakirəsi',
            'ba': u'Wikipedia б-са фекер алышыу',
            'bar': u'Wikipedia Diskussion',
            'bat-smg': u'Wikipedia aptarimas',
            'be': u'Вікіпедыя размовы',
            'be-x-old': u'Абмеркаваньне Вікіпэдыя',
            'bg': u'Уикипедия беседа',
            'bm': u'Discussion Wikipedia',
            'bn': u'উইকিপেডিয়া আলাপ',
            'bpy': u'উইকিপিডিয়া য়্যারী',
            'br': u'Kaozeadenn Wikipedia',
            'bs': u'Razgovor s Wikipediom',
            'ca': u'Viquipèdia Discussió',
            'ce': u'Обсуждение Wikipedia',
            'cs': u'Wikipedie diskuse',
            'csb': u'Diskùsëjô Wiki',
            'cu': u'Википедїѩ бесѣда',
            'cv': u'Википеди сӳтсе явмалли',
            'cy': u'Sgwrs Wicipedia',
            'da': u'Wikipedia-diskussion',
            'de': u'Wikipedia Diskussion',
            'el': u'Βικιπαίδεια συζήτηση',
            'eo': u'Vikipedia diskuto',
            'es': u'Wikipedia Discusión',
            'et': u'Vikipeedia arutelu',
            'eu': u'Wikipedia eztabaida',
            'fa': u'بحث ویکی‌پدیا',
            'fi': u'Keskustelu Wikipediasta',
            'fiu-vro': u'Wikipedia arotus',
            'fo': u'Wikipedia kjak',
            'fr': u'Discussion Wikipédia',
            'fur': u'Discussion Vichipedie',
            'fy': u'Wikipedy oerlis',
            'ga': u'Plé Vicipéide',
            'gn': u'Wikipedia Discusión',
            'gu': u'વિકિપીડિયા talk',
            'he': u'שיחת ויקיפדיה',
            'hi': u'विकिपीडिया वार्ता',
            'hr': u'Razgovor Wikipedija',
            'hsb': u'Wikipedija diskusija',
            'hu': u'Wikipédia vita',
            'hy': u'Wikipedia քննարկում',
            'ia': u'Discussion Wikipedia',
            'id': u'Pembicaraan Wikipedia',
            'is': u'Wikipediaspjall',
            'it': u'Discussioni Wikipedia',
            'ja': u'Wikipedia‐ノート',
            'jv': u'Dhiskusi Wikipedia',
            'ka': u'ვიკიპედია განხილვა',
            'kab': u'Amyannan n Wikipedia',
            'kk': u'Уикипедия талқылауы',
            'kn': u'Wikipedia ಚರ್ಚೆ',
            'ko': u'위키백과토론',
            'ksh':u'Wikipedia Klaaf',
            'ku': u'Wîkîpediya nîqaş',
            'kv': u'Обсуждение Wikipedia',
            'la': u'Disputatio Vicipaediae',
            'li': u'Euverlèk Wikipedia',
            'lt': u'Wikipedia aptarimas',
            'lv': u'Wikipedia diskusija',
            'mk': u'Разговор за Википедија',
            'ml': u'വിക്കിപീഡിയ സംവാദം',
            'mr': u'Wikipedia चर्चा',
            'ms': u'Perbualan Wikipedia',
            'mt': u'Wikipedija talk',
            'mzn': u'بحث Wikipedia',
            'nah': u'Wikipedia Discusión',
            'nap': u'Discussioni Wikipedia',
            'nds': u'Wikipedia Diskuschoon',
            'nds-nl': u'Overleg Wikipedie',
            'new': u'विकिपिडिया खँलाबँला',
            'nl': u'Overleg Wikipedia',
            'nn': u'Wikipedia-diskusjon',
            'no': u'Wikipedia-diskusjon',
            'nv': u"Wikiibíídiiya baa yinísht'į́",
            'oc': u'Discussion Wikipèdia',
            'os': u'Дискусси Wikipedia',
            'pa': u'ਵਿਕਿਪੀਡਿਆ ਚਰਚਾ',
            'pl': u'Dyskusja Wikipedii',
            'pms':u'Discussion ant sla Wikipedia',
            'pt': u'Wikipedia Discussão',
            'qu': u'Wikipedia Discusión',
            'rmy':u'Vikipidiyake vakyarimata',
            'ro': u'Discuţie Wikipedia',
            'ru': u'Обсуждение Википедии',
            'sa': u'Wikipediaसंभाषणं',
            'sc': u'Wikipedia discussioni',
            'sk': u'Diskusia k Wikipédii',
            'sl': u'Pogovor o Wikipediji',
            'sq': u'Wikipedia diskutim',
            'sr': u'Разговор о Википедији',
            'su': u'Obrolan Wikipedia',
            'sv': u'Wikipediadiskussion',
            'ta': [u'Wikipedia பேச்சு', u'விக்கிபீடியா பேச்சு'],
            'te': u'వికీపీడియా చర్చ',
            'tg': u'Баҳси Википедиа',
            'th': u'คุยเรื่องวิกิพีเดีย',
            'tr': u'Vikipedi tartışma',
            'tt': u'Wikipedia bäxäse',
            'ty': u'Discussion Wikipedia',
            'udm': u'Wikipedia сярысь вераськон',
            'uk': u'Обговорення Вікіпедії',
            'ur': u'تبادلۂ خیال منصوبہ',
            'uz': u'Wikipedia munozarasi',
            'vec':u'Discussion Wikipedia',
            'vi': u'Thảo luận Wikipedia',
            'vls': u'Discuusje Wikipedia',
            'vo': u'Bespik dö Vükiped',
            'wa': u'Wikipedia copene',
            'xal': u'Wikipedia тускар ухалвр',
            'yi': u'װיקיפּעדיע רעדן',
            'zea': u'Overleg Wikipedia',
        }

        self.namespaces[100] = {
            '_default': u'Portal',
            'ar': u'بوابة',
            'bpy': u'হমিলদুৱার',
            'br': u'Porched',
            'cs': u'Portál',
            'el': u'Πύλη',
            'eo': u'Portalo',
            'eu': u'Atari',
            'fa': u'درگاه',
            'fi': u'Teemasivu',
            'fr': u'Portail',
            'it': u'Portale',
            'he': u'פורטל',
            'hi': u'प्रवेशद्वार',
            'hu': u'Portál',
            'is': u'Gátt',
            'it': u'Portale',
            'ka': u'პორტალი',
            'kk': u'Портал',
            'li': u'Portaol',
            'ml': u'കവാടം',
            'new': u'दबू',
            'nl': u'Portaal',
            'ru': u'Портал',
            'sk': u'Portál',
            'sr': u'Портал',
            'tg': u'Портал',
            'vo': u'Bespik dö Vükiped',
            'zh-classical': u'門',
        }

        self.namespaces[101] = {
            '_default': u'Portal talk',
            'ar': u'نقاش البوابة',
            'bpy': u'হমিলদুৱার য়্যারী',
            'br': u'Kaozeal:Porched',
            'ca': u'Portal Discussió',
            'cs': u'Portál diskuse',
            'da': u'Portaldiskussion',
            'de': u'Portal Diskussion',
            'el': u'Συζήτηση πύλης',
            'eo': u'Portala diskuto',
            'es': u'Portal Discusión',
            'eu': u'Atari eztabaida',
            'fa': u'بحث درگاه',
            'fi': u'Keskustelu teemasivusta',
            'fr': u'Discussion Portail',
            'he': u'שיחת פורטל',
            'hi': u'प्रवेशद्वार वार्ता',
            'hr': u'Razgovor o portalu',
            'hu': u'Portál vita',
            'id': u'Pembicaraan Portal',
            'is': u'Gáttaspjall',
            'it': u'Discussioni portale',
            'ja': u'Portal‐ノート',
            'ka': u'პორტალი განხილვა',
            'kk': u'Портал талқылауы',
            'li': u'Euverlèk portaol',
            'lmo': u'Descüssiú Portal',
            'ml': u'കവാടം',
            'nds':u'Portal Diskuschoon',
            'new':u'दबू खँलाबँला',
            'nl': u'Overleg portaal',
            'no': u'Portaldiskusjon',
            'pl': u'Dyskusja portalu',
            'pt': u'Portal Discussão',
            'ro': u'Discuţie Portal',
            'ru': u'Обсуждение портала',
            'sk': u'Diskusia k portálu',
            'sq': u'Portal diskutim',
            'sr': u'Разговор о порталу',
            'su': u'Obrolan portal',
            'sv': u'Portaldiskussion',
            'tg': u'Баҳси портал',
            'tr': u'Portal tartışma',
            'zh-classical': u'議',
        }

        self.namespaces[102] = {
            '_default': u'WikiProject',
            'ca': u'Viquiprojecte',
            'cs': u'Rejstřík',
            'es': u'Wikiproyecto',
            'eu': u'Wikiproiektu',
            'fr': u'Projet',
            'it': u'Progetto',
            'lmo': u'Purtaal',
            'pl': u'Wikiprojekt',
        }

        self.namespaces[103] = {
            '_default': u'WikiProject talk',
            'ca': u'Viquiprojecte Discussió',
            'cs': u'Rejstřík diskuse',
            'es': u'Wikiproyecto Discusión',
            'eu': u'Wikiproiektu eztabaida',
            'fr': u'Discussion Projet',
            'it': u'Discussioni progetto',
            'lmo': u'Descüssiun Purtaal',
            'pl': u'Dyskusja Wikiprojektu',
        }

        self.namespaces[104] = {
            '_default': u'Reference',
            'es': u'Anexo',
            'fr': u'Référence',

        }

        self.namespaces[105] = {
            '_default': u'Reference talk',
            'es': u'Anexo Discusión',
            'fr' : u'Discussion Référence',
        }

        self.namespaces[106] = {
            '_default': u'Table',
        }

        self.namespaces[107] = {
            '_default': u'Table talk',
        }

        self.disambiguationTemplates = {

            '_default': [u'Disambig'],
            'af':  [u'Dubbelsinnig', u'Disambig'],
            'als': [u'Begriffsklärung', u'BKL', u'Disambig'],
            'an':  [u'Desambig',u'Disambig'],
            'ang': [u'Disambig'],
            'arc': [u'ܕ'],
            'ast': [u'Dixebra'],
            'ar':  [u'Disambig', u'توضيح'],
            'be':  [u'Неадназначнасць', u'Disambig'],
            'be-x-old':  [u'Неадназначнасць', u'Неадназначнасьць', u'Disambig'],
            'bg':  [u'Пояснение', u'Disambig'],
            'br':  [u'Hvlstumm', u'Digejañ'],
            'bs':  [u'Čvor'],
            'ca':  [u'Desambiguació', u'Disambig', u'Desambigua'],
            'ceb': [u'Giklaro'],
            'cs':  [u'Rozcestník', u'Rozcestník - 2 znaky', u'Rozcestník - Příjmení',
                    u'Rozcestník - místopisné jméno', u'Disambig', u'Rozcestník - příjmení',],
            'cy':  [u'Anamrwysedd', u'Disambig', u'Gwahaniaethu'],
            'da':  [u'Flertydig'],
            'de':  [u'Begriffsklärung', u'BKL', u'Disambig'],
            'el':  [u'Disambig', u'Αποσαφ'],
            'en':  [u'Disambig', u'Disambiguation', u'2CC', u'2LC',
                    u'2LCdisambig', u'3CC', u'3LC', u'4CC', u'4LC', u'4LA',
                    u'5CC', u'TLAdisambig', u'Hndis', u'Numberdis',
                    u'Roadis', u'Roaddis', u'Geodis', u'TLA', u'Surname',
                    u'Dab', u'Disambig-cleanup', u'Disamb',
                    u'Schooldis', u'Shipindex', u'Songdis', u'4cc', u'3cc'],
            'eo':  [u'Apartigilo',u'Disambig'],
            'es':  [u'Desambiguacion', u'Desambiguación', u'Desambig', u'Disambig',u'Des'],
            'et':  [u'Täpsustuslehekülg', u'Täpsustus', u'Disambig'],
            'eu':  [u'Argipen', u'Disambig'],
            'fa':  [u'ابهام‌زدایی'],
            'fi':  [u'Täsmennyssivu', u'Disambig'],
            'fr':  [u'Homonymie', u'Homonymie dynastique', u'Paronymie', u'Sigles n lettres'],
            'frp': [u'Homonimos'],
            'fy':  [u'Tfs',u'Neibetsjuttings'],
            'ga':  [u'Idirdhealú', u'Disambig'],
            'gl':  [u'Homónimos', u'Disambig'],
            'he':  [u'DisambiguationAfter', u'פירושונים', u'Disambig'],
            'hr':  [u'Disambig', u'Razdvojba'],
            'hu':  [u'Egyert', u'Disambig',u'Egyért'],
            'ia':  [u'Disambiguation', u'Disambig'],
            'id':  [u'Disambig'],
            'io':  [u'Homonimo', u'Disambig'],
            'is':  [u'Aðgreining', u'Disambig'],
            'it':  [u'Disambigua', u'Sigla2', u'Sigla3', u'Cogni'],
            'ja':  [u'Aimai', u'Disambig'],
            'ka':  [u'მრავალმნიშვნელოვანი', u'მრავმნიშ'],
            'kg':  [u'Bisongidila'],
            'kw':  [u'Klerheans'],
            'ko':  [u'Disambig'],
            'ku':  [u'Cudakirin'],
            'la':  [u'Discretiva'],
            'lb':  [u'Homonymie', u'Disambig'],
            'li':  [u'Verdudeliking', u'Verdudelikingpazjena', u'Vp'],
            'ln':  [u'Bokokani'],
            'lt':  [u'Disambig'],
            'mk':  [u'Појаснување'],
            'mo':  [u'Дезамбигуйзаре', u'Disambig'],
            'ms':  [u'Nyahkekaburan'],
            'mt':  [u'Diżambigwazzjoni'],
            'nds': [u'Mehrdüdig Begreep','Disambig'],
            'nds-nl': [u'Dv'],
            'nl':  [u'Dp', u'DP', u'Dp2', u'Dpintro', u'Cognomen'],
            'nn':  [u'Fleirtyding'],
            'no':  [u'Peker', u'Etternavn', u'Disambig', u'Tobokstavsforkortelse',
                    u'Trebokstavsforkortelse'],
            'nov': [u'Desambig'],
            'oc':  [u'Omonimia',],
            'pl':  [u'Disambig', u'DisambRulers', u'DisambigC',u'Strona ujednoznaczniająca'],
            'pt':  [u'Desambiguação', u'Disambig', u'Desambig'],
            'ro':  [u'Dezambiguizare', u'Disambig', u'Hndis'],
            'ru':  [u'Disambig', u'Неоднозначность', u'неоднозначность'],
            'scn': [u'Disambigua', u'Disambig', u'Sigla2', u'Sigla3'],
            'simple': [u'Disambig', u'Disambiguation', u'3CC',u'2CC'],
            'sk':  [u'Disambig', u'Rozlišovacia stránka', u'Disambiguation'],
            'sl':  [u'Disambig', u'Razločitev', u'Disambig-ship'],
            'sq':  [u'Kthjellim', u'Disambig'],
            'sr':  [u'Вишезначна одредница', u'Disambig'],
            'su':  [u'Disambig'],
            'sv':  [u'Betydelselista', u'Disambig', u'Förgrening', u'Gaffel',
                    u'Efternamn', u'Gren', u'Förgreningssida', u'3LC',
                    u'Trebokstavsförkortning', u'TLAdisambig'],
            'sw':  [u'Maana'],
            'th':  [u'แก้กำกวม', u'Disambig'],
            'tl':  [u'Paglilinaw', u'Disambig'],
            'tr':  [u'Anlam ayrım', u'Disambig', u'Anlam ayrımı'],
            'uk':  [u'DisambigG', u'Disambig'],
            'vi':  [u'Trang định hướng', u'Định hướng', u'Disambig', u'Hndis'],
            'vo':  [u'Telplänov'],
            'wa':  [u'Omonimeye', u'Disambig'],
            'yi':  [u'באדייטען'],
            'zh':  [u'Disambig', u'消歧义', u'消歧义页', u'消歧義'],
            'zh-min-nan': [u'Khu-pia̍t-ia̍h', 'KhPI', u'Disambig'],
            'zh-yue': [u'搞清楚',u'Disambig'],
        }

        self.disambcatname = {
            'af':  u'dubbelsinnig',
            'als': u'Begriffsklärung',
            'ang': u'Scīrung',
            'ast': u'Dixebra',
            'ar':  u'صفحات توضيح',
            'be':  u'Disambig',
            'be-x-old':  u'Вікіпэдыя:Неадназначнасьці',
            'bg':  u'Пояснителни страници',
            'ca':  u'Registre de pàginas de desambiguació',
            'cs':  u'Rozcestníky',
            'cy':  u'Gwahaniaethu',
            'da':  u'Flertdig',
            'de':  u'Begriffsklärung',
            'el':  u'Αποσαφήνιση',
            'en':  u'Disambiguation',
            'eo':  u'Apartigiloj',
            'es':  u'Desambiguación',
            'et':  u'Täpsustusleheküljed',
            'eu':  u'Argipen orriak',
            'fa':  u'صفحات ابهام‌زدایی',
            'fi':  u'Täsmennyssivu',
            'fr':  u'Homonymie',
            'fy':  u'Trochferwiisside',
            'ga':  u'Idirdhealáin',
            'gl':  u'Homónimos',
            'he':  u'פירושונים',
            'ia':  u'Disambiguation',
            'id':  u'Disambiguasi',
            'io':  u'Homonimi',
            'is':  u'Aðgreiningarsíður',
            'it':  u'Disambigua',
            'ja':  u'曖昧さ回避',
            'ka':  u'მრავალმნიშვნელოვანი',
            'kw':  u'Folennow klerheans',
            'ko':  u'동음이의어 문서',
            'ku':  u'Rûpelên cudakirinê',
            'la':  u'Discretiva',
            'lb':  u'Homonymie',
            'li':  u'Verdudelikingspazjena',
            'ln':  u'Bokokani',
            'lt':  u'Nuorodiniai straipsniai',
            'ms':  u'Nyahkekaburan',
            'mt':  u'Diżambigwazzjoni',
            'nds': u'Mehrdüdig Begreep',
            'nds-nl': u'Deurverwiespagina',
            'nl':  u'Wikipedia:Doorverwijspagina',
            'nn':  u'Fleirtydingssider',
            'no':  u'Pekere',
            'pl':  u'Strony ujednoznaczniające',
            'pt':  u'Desambiguação',
            'ro':  u'Dezambiguizare',
            'ru':  u'Многозначные термины',
            'scn': u'Disambigua',
            'sk':  u'Rozlišovacie stránky',
            'sl':  u'Razločitev',
            'sq':  u'Kthjellime',
            'sr':  u'Вишезначна одредница',
            'su':  u'Disambiguasi',
            'sv':  u'Förgreningssider',
            'th':  u'การแก้ความกำกวม',
            'tl':  u'Paglilinaw',
            'tr':  u'Anlam ayrım',
            'uk':  u'Багатозначні геопункти',
            'vi':  u'Trang định hướng',
            'vo':  u'Telplänovapads',
            'wa':  u'Omonimeye',
            'zh':  u'消歧义',
            'zh-min-nan': u'Khu-pia̍t-ia̍h',
            }

        # On most Wikipedias page names must start with a capital letter, but some
        # languages don't use this.

        self.nocapitalize = ['jbo','tlh']


        # A revised sorting order worked out on http://meta.wikimedia.org/wiki/Interwiki_sorting_order
        self.alphabetic_revised = ['aa','af','ak','als','am','ang','ab','ar','an',
            'arc','roa-rup','frp','as','ast','gn','av','ay','az','id','ms','bm',
            'bn','zh-min-nan','map-bms','jv','su','ban','ba','be','be-x-old','bh',
            'bi','bo','bs','br','bug','bg','bxr','ca','ceb','cv','cs','ch',
            'ny','sn',
            'tum','cho','co','za','cy','da','pdc','de','dv','nv','dz','mh','et',
            'na','el','eml','en','es','eo','eu','ee','to','fab','fa','fo','fr','fy','ff',
            'fur','ga','gv','sm','gd','gl','gay','ki','glk','gu','got','zh-classical','hak','xal','ko','ha','haw',
            'hy','hi','ho','hsb','hr','io','ig','ilo','bpy','ia','ie','iu','ik','os','xh','zu',
            'is','it','he','kl','pam','kn','kr','ka','ks','csb','kk','kk-cn','kk-kz','kw','rw','ky',
            'rn','sw','kv','kg','ht','kj','ku','lad','lbe','lo','ltg','la','lv','lb','lij','lt',
            'li','ln','jbo','lg','lmo','hu','mk','mg','ml','mt','mi','mr','mzn','chm','cdo','mo',
            'mn','mus','my','nah','fj','nl','nds-nl','cr','ne','new','ja','nap','ce',
            'pih','no','nn','nrm','nov','oc','or','om','ng','hz','ug','uz','pa',
            'pi','pag','pap','ps','km','pms','nds','pl','pt','kk-tr','ty','ksh','ro',
            'rmy','rm','qu','ru','se','sa','sg','sc','sco','st','tn','sq','ru-sib','scn',
            'si','simple','sd','ss','sk','sl','cu','so','sr','sh','fi','sv','tl',
            'ta','kab','roa-tara','tt','te','tet','th','vi','ti','tlh','tg','tpi','chr','chy',
            've','tr','tk','tw','udm','uk','ur','vec','vo','fiu-vro','wa',
            'vls','war','wo','wuu','ts','ii','yi','yo','zh-yue','cbk-zam','diq','zea','bat-smg',
            'zh','zh-tw','zh-cn']

        # A sorting order for lb.wikipedia worked out by http://lb.wikipedia.org/wiki/User_talk:Otets
        self.alphabetic_lb = ['aa', 'af', 'ak', 'als', 'am', 'ang', 'ab', 'ar', 'an',
            'arc', 'roa-rup', 'frp', 'as', 'ast', 'gn', 'av', 'ay', 'az', 'id', 'ms', 'bm',
            'bn', 'zh-min-nan', 'map-bms', 'jv', 'su', 'ban', 'bug', 'ba', 'be', 'bh', 'mt',
            'be-x-old', 'bi', 'bo', 'bs', 'br', 'bg', 'bxr', 'ca', 'ceb', 'cs', 'ch',
            'chr', 'chy',
            'ny', 'sn', 'tum', 've', 'cho', 'co', 'za', 'cy', 'da', 'pdc', 'de', 'dv',
            'nv', 'dz', 'mh', 'na', 'el', 'eml', 'en', 'es', 'eo', 'et', 'eu', 'ee', 'to',
            'fab', 'fa', 'fo', 'fr', 'fy', 'ff', 'fur', 'ga', 'gv', 'sm', 'gd', 'gl',
            'gay', 'ki', 'glk', 'gu', 'got', 'zh-classical', 'hak', 'xal', 'ko', 'ha', 'haw', 'hy', 'he', 'hi', 'ho', 'hsb',
            'hr', 'io', 'ig', 'bpy', 'ilo', 'ia', 'ie', 'iu', 'ik', 'os', 'xh', 'zu', 'is', 'it',
            'ja', 'kl', 'pam', 'kn', 'kr', 'ka', 'ks', 'csb', 'kw', 'rw', 'ky', 'rn', 'sw',
            'kv', 'kg', 'ht', 'kj', 'ku', 'lad', 'lbe', 'lo', 'ltg', 'la', 'lv', 'lb', 'lij', 'lt', 'li',
            'ln', 'jbo', 'lg', 'lmo', 'hu', 'mk', 'mg', 'ml', 'mi', 'mr', 'mzn', 'chm',
            'cdo', 'mo', 'mn', 'mus', 'my', 'nah', 'fj', 'nap', 'nds-nl', 'nl', 'cr', 'ne', 'new', 'ce',
            'pih', 'no', 'nn', 'nrm', 'nov', 'oc', 'or', 'om', 'ng', 'hz', 'ug', 'uz', 'pa', 'kk',
            'kk-cn', 'kk-kz', 'kk-tr',
            'pi', 'pam', 'pag', 'pap', 'ps', 'km', 'pms', 'nds', 'pl', 'pt', 'ty', 'ksh', 'ro', 'rmy', 'rm', 'qu',
            'ru', 'se', 'sa', 'sg', 'sc', 'sco', 'st', 'tn', 'sq', 'ru-sib', 'scn', 'si',
            'simple', 'sd', 'ss', 'sk', 'sl', 'cu', 'so', 'sr', 'sh', 'fi', 'sv', 'tl',
            'ta', 'kab', 'roa-tara', 'tt', 'te', 'tet', 'th', 'vi', 'ti', 'tlh', 'tg', 'tpi', 'cv', 'tr',
            'tk', 'tw', 'udm', 'uk', 'ur', 'vec', 'vo', 'fiu-vro', 'wa', 'vls', 'war',
            'wo', 'wuu', 'ts', 'ii', 'yi', 'yo', 'zh-yue', 'cbk-zam', 'diq', 'zea', 'bat-msg', 'zh',
            'zh-tw', 'zh-cn']

        # Order for fy: alphabetical by code, but y counts as i

        def fycomp(x,y):
            x = x.replace("y","i")+x.count("y")*"!"
            y = y.replace("y","i")+y.count("y")*"!"
            return cmp(x,y)
        self.fyinterwiki = self.alphabetic[:]
        self.fyinterwiki.sort(fycomp)

        # Which languages have a special order for putting interlanguage links,
        # and what order is it? If a language is not in interwiki_putfirst,
        # alphabetical order on language code is used. For languages that are in
        # interwiki_putfirst, interwiki_putfirst is checked first, and
        # languages are put in the order given there. All other languages are put
        # after those, in code-alphabetical order.

        self.interwiki_putfirst = {
            'en': self.alphabetic,
            'et': self.alphabetic_revised,
            'fi': self.alphabetic_revised,
            'fy': self.fyinterwiki,
            'he': ['en'],
            'hu': ['en'],
            'lb': self.alphabetic_lb,
            'nn': ['no','nb','sv','da'] + self.alphabetic,
            'no': self.alphabetic,
            'pl': self.alphabetic,
            'simple': self.alphabetic,
            'te': ['en','hi', 'kn', 'ta', 'ml'],
            'vi': self.alphabetic_revised,
            'yi': ['en','he','de']
        }

        self.obsolete = {'dk':'da',
                    'minnan':'zh-min-nan',
                    'mo':None,
                    'nb':'no',
                    'jp':'ja',
                    'tokipona':None,
                    'zh-tw':'zh',
                    'zh-cn':'zh'
        }

        # Language codes of the largest wikis. They should be roughly sorted
        # by size.
        # Note: currently they have been sorted by number of pages, but with languages
        # not in the Latin alphabet counted 1/3 lower

        self.languages_by_size = [
            'en','de','fr','pl','nl','it','pt','ja','es','sv',
            'ru','fi','no','eo','zh','tr','sk','cs','da','ro',
            'id','ca','hu','sl','lt','uk','lmo','he','et','ceb',
            'hr','sr','bg','ko','gl','nn','ms','ar','te','vi',
            'bs','eu','simple','is','io','el','sq','th','lb','br',
            'fa','la','nap','sh','su','bn','jv','ka','scn','new',
            'lv','ku','nds','wa','cy','bpy','ast','pms','oc','af',
            'hi','ht','ta','ksh','mr','mk','az','an','tl','co',
            'ga','ru-sib','be-x-old','fy','gd','vec','tg','vo','tt','cv',
            'sw','ur','uz','ia','kn','als','li','pam','sa','nrm',
            'zh-min-nan','fo','nds-nl','yi','ilo','qu','war','zh-yue','fur','hy',
            'am','frp','sco','nov','se','ml','yo','bat-smg','vls','lij',
            'map-bms','mt','bh','csb','pdc','diq','kw','fiu-vro','nah','os',
            'be','lad','hsb','to','ang','zh-classical','bar','ne','ln','mi', 
            'ps','tk','jbo','kk','ty','rm','mn','wo','tpi','ie',
            'roa-rup','arc','mo','tet','pag','dv','kg','na','ks','sc',
            'ky','mg','gu','rmy','eml','glk','wuu','cbk-zam','so','udm',
            'gv','na','cu','bo','bm','sm','iu','chr','sd','ba',
            'si','cr','lo','av','ug','km','zu','pi','got','cdo',
            'ce','ti',]

        # Languages that used to be coded in iso-8859-1
        self.latin1old = ['de', 'en', 'et', 'es', 'ia', 'la', 'af', 'cs',
                    'fr', 'pt', 'sl', 'bs', 'fy', 'vi', 'lt', 'fi', 'it',
                    'no', 'simple', 'gl', 'eu', 'nds', 'co', 'mi', 'mr',
                    'id', 'lv', 'sw', 'tt', 'uk', 'vo', 'ga', 'na', 'es',
                    'nl', 'da', 'dk', 'sv', 'test']

        self.mainpages = {
            'aa' :            u'Main Page',
            'ab' :            u'Main Page',
            'af' :            u'Tuisblad',
            'ak' :            u'Main Page',
            'als':            u'Houptsyte',
            'am' :            u'ዋናው ገጽ',
            'an' :            u'Portalada',
            'ang':            u'Héafodsíde',
            'ar' :            u'الصفحة الرئيسية',
            'arc':            u'Main Page',
            'as' :            u'Main Page',
            'ast':            u'Portada',
            'av' :            u'Main Page',
            'ay' :            u'Main Page',
            'az' :            u'Main Page',
            'ba' :            u'Баш бит',
            'be' :            u'Галоўная старонка',
            'be-x-old':       u'Галоўная старонка',
            'bg' :            u'Начална страница',
            'bh' :            u'Main Page',
            'bi' :            u'Main Page',
            'bm' :            u'Nyɛ fɔlɔ',
            'bn' :            u'প্রধান পাতা',
            'bo' :            u'Main Page',
            'br' :            u'Main Page',
            'bs' :            u'Početna strana',
            'ca' :            u'Portada',
            'ce' :            u'Main Page',
            'ceb':            u'Main Page',
            'ch' :            u'Main Page',
            'cho':            u'Main Page',
            'chr':            u'Main Page',
            'chy':            u'Main Page',
            'co' :            u'Main Page',
            'cr' :            u'Main Page',
            'cs' :            u'Hlavní strana',
            'csb':            u'Przédnô starna',
            'cv' :            u'Тĕп страницă',
            'cy' :            u'Hafan',
            'da' :            u'Forside',
            'de' :            u'Hauptseite',
            'dv' :            u'Main Page',
            'dz' :            u'Main Page',
            'ee' :            u'Main Page',
            'el' :            u'Κύρια Σελίδα',
            'en' :            u'Main Page',
            'eo' :            u'Ĉefpaĝo',
            'es' :            u'Portada',
            'et' :            u'Esileht',
            'eu' :            u'Azala',
            'fa' :            u'صفحه‌ی اصلی',
            'ff' :            u'Hello jaɓɓorgo',
            'fi' :            u'Etusivu',
            'fiu-vro':        u'Pääleht',
            'fj' :            u'Main Page',
            'fo' :            u'Forsíða',
            'fr' :            u'Accueil',
            'fur':            u'Pagjine principâl',
            'fy' :            u'Haadside',
            'ga' :            u'Príomhleathanach',
            'gd' :            u'Duille Mòr',
            'gl' :            u'Portada',
            'gn' :            u'Main Page',
            'got':            u'Main Page',
            'gu' :            u'મુખપૃષ્ઠ',
            'gv' :            u'Main Page',
            'ha' :            u'Main Page',
            'hak':            u'Thèu-chông',
            'haw':            u'Main Page',
            'he' :            u'עמוד ראשי',
            'hi' :            u'मुख्य पृष्ठ',
            'ho' :            u'Main Page',
            'hr' :            u'Glavna stranica',
            'ht' :            u'Main Page',
            'hu' :            u'Kezdőlap',
            'hy' :            u'Գլխավոր Էջ',
            'hz' :            u'Main Page',
            'ia' :            u'Wikipedia:Frontispicio',
            'id' :            u'Halaman Utama',
            'ie' :            u'Principal págine',
            'ig' :            u'Main Page',
            'ii' :            u'Main Page',
            'ik' :            u'Main Page',
            'io' :            u'Frontispico',
            'is' :            u'Forsíða',
            'it' :            u'Pagina principale',
            'iu' :            u'Main Page',
            'ja' :            u'メインページ',
            'jbo':            u'ralju ckupau',
            'jv' :            u'Kaca Utama',
            'ka' :            u'მთავარი გვერდი',
            'kab':            u'Asebtar amenzawi',
            'kg' :            u'Main Page',
            'ki' :            u'Main Page',
            'kj' :            u'Main Page',
            'kk' :            u'Main Page',
            'kl' :            u'Main Page',
            'km' :            u'Main Page',
            'kn' :            u'ಮುಖ್ಯ ಪುಟ',
            'ko' :            u'대문',
            'kr' :            u'Main Page',
            'ks' :            u'Main Page',
            'ku' :            u'Serûpel',
            'kv' :            u'Main Page',
            'kw' :            u'Main Page',
            'ky' :            u'Main Page',
            'la' :            u'Pagina prima',
            'lb' :            u'Haaptsäit',
            'lg' :            u'Main Page',
            'li' :            u'Huidpazjena',
            'ln' :            u'Lonkásá ya liboso',
            'lo' :            u'Main Page',
            'lt' :            u'Pradžia',
            'lv' :            u'Sākumlapa',
            'mg' :            u'Fandraisana',
            'mh' :            u'Main Page',
            'mi' :            u'Hau Kāinga',
            'mk' :            u'Почетна страна',
            'ml' :            u'Main Page',
            'mn' :            u'Main Page',
            'mo' :            u'Main Page',
            'mr' :            u'मुखपृष्ठ',
            'ms' :            u'Laman Utama',
            'mt' :            u'Paġna prinċipali',
            'mus':            u'Main Page',
            'my' :            u'ဗဟုိစာမ္ယက္‌န္ဟာ',
            'na' :            u'Etang õgõg',
            'nah':            u'Main Page',
            'nds':            u'Hööftsiet',
            'nds-nl':         u'Heufdpagina',
            'ne' :            u'Main Page',
            'ng' :            u'Main Page',
            'nl' :            u'Hoofdpagina',
            'nn' :            u'Hovudside',
            'no' :            u'Hovedside',
            'nv' :            u'Íiyisíí Naaltsoos',
            'ny' :            u'Main Page',
            'oc' :            u'Acuèlh',
            'om' :            u'Main Page',
            'or' :            u'Main Page',
            'os' :            u'Сæйраг фарс',
            'pa' :            u'ਮੁੱਖ ਪੰਨਾ',
            'pam':            u'Main Page',
            'pi' :            u'Main Page',
            'pl' :            u'Strona główna',
            'ps' :            u'Main Page',
            'pt' :            u'Página principal',
            'qu' :            u'Qhapaq panka',
            'rm' :            u'Main Page',
            'rn' :            u'Main Page',
            'ro' :            u'Pagina principală',
            'roa-rup':        u'Main Page',
            'ru' :            u'Заглавная страница',
            'rw' :            u'Main Page',
            'sa' :            u'मुखपृष्ठं',
            'sc' :            u'Pàzina printzipale',
            'scn':            u'Paggina principali',
            'sco':            u'Main Page',
            'sd' :            u'Main Page',
            'se' :            u'Váldosiidu',
            'sg' :            u'Main Page',
            'sh' :            u'Glavna stranica / Главна страница',
            'si' :            u'Main Page',
            'simple':         u'Main Page',
            'sk' :            u'Hlavná stránka',
            'sl' :            u'Glavna stran',
            'sm' :            u'Main Page',
            'sn' :            u'Main Page',
            'so' :            u'Main Page',
            'sq' :            u'Faqja Kryesore',
            'sr' :            u'Главна страна',
            'ss' :            u'Main Page',
            'st' :            u'Main Page',
            'su' :            u'Tepas',
            'sv' :            u'Huvudsida',
            'sw' :            u'Mwanzo',
            'ta' :            u'முதற் பக்கம்',
            'te' :            u'మొదటి పేజీ',
            'tg' :            u'Main Page',
            'th' :            u'หน้าหลัก',
            'ti' :            u'Main Page',
            'tk' :            u'Main Page',
            'tl' :            u'Unang Pahina',
            'tn' :            u'Main Page',
            'to' :            u'Main Page',
            'tpi':            u'Main Page',
            'tr' :            u'Ana Sayfa',
            'ts' :            u'Main Page',
            'tt' :            u'Täwge Bit',
            'tum':            u'Main Page',
            'tw' :            u'Main Page',
            'ty' :            u'Main Page',
            'ug' :            u'Main Page',
            'uk' :            u'Головна стаття',
            'ur' :            u'صفحہ اول',
            'uz' :            u'Main Page',
            've' :            u'Main Page',
            'vi' :            u'Trang Chính',
            'vo' :            u'Cifapad',
            'wa' :            u'Mwaisse pådje',
            'wo' :            u'Main Page',
            'xh' :            u'Main Page',
            'yi' :            u'ערשטע זײַט',
            'yo' :            u'Main Page',
            'za' :            u'Main Page',
            'zh' :            u'首页',
            'zh-min-nan':     u'Thâu-ia̍h',
            'zu' :            u'Main Page',
        }

    def version(self, code):
        return "1.11"
    
    def dbName(self, code):
        # returns the name of the MySQL database
        # for historic reasons, the databases are called wikixx instead of
        # wikipediaxx for Wikipedias.
        return '%swiki' % code

    def code2encodings(self, code):
        """Return a list of historical encodings for a specific language
           wikipedia"""
        # Historic compatibility
        if code == 'pl':
            return 'utf-8', 'iso8859-2'
        if code == 'ru':
            return 'utf-8', 'iso8859-5'
        if code in self.latin1old:
            return 'utf-8', 'iso-8859-1'
        return self.code2encoding(code),
