import re

"""
This is a store of pre-compiled regexes that are used in the user agent
detection.  It's a bit clunky but we don't want to take a chance that these
fall out of the regex cache as they might need to be used frequently on a busy
website.

Anything that can be done with a simple string.find() is.
"""
_detection = {
    'tv': {
        'smart_tv': re.compile(r"""
                GoogleTV|
                SmartTV|
                Internet.TV|
                NetCast|
                NETTV|
                AppleTV|
                boxee|
                Kylo|
                Roku|
                DLNADOC|
                CE\-HTML
            """, re.VERBOSE | re.IGNORECASE),
        'console': re.compile(r"""
                Xbox|
                PLAYSTATION.3|
                Wii
            """, re.VERBOSE | re.IGNORECASE),
    },
    'tablet': {
        'ipad': re.compile(r'iP(a|ro)d', re.IGNORECASE),
        'mobiles': re.compile(r""" # Known to be phone UAs.
            Fennec|
            mobi|
            HTC.Magic|
            HTCX06HT|
            Nexus.One|
            SC-02B|
            fone.945
        """, re.VERBOSE | re.IGNORECASE),
        'android': re.compile(r""" # Pre Android 3.0.
            GT-P10|
            SC-01C|
            SHW-M180S|
            SGH-T849|
            SCH-I800|
            SHW-M180L|
            SPH-P100|
            SGH-I987|
            zt180|
            HTC(.Flyer|\_Flyer)|
            Sprint.ATP51|
            ViewPad7|
            pandigital(sprnova|nova)|
            Ideos.S7|
            Dell.Streak.7|
            Advent.Vega|
            A101IT|
            A70BHT|
            MID7015|
            Next2|
            nook
        """, re.VERBOSE | re.IGNORECASE),
        'mac': re.compile(r'Mac.OS', re.IGNORECASE),
    },
    'mobile': {
        'unique': re.compile(r""" # Unique mobile UAs.
            BOLT|
            Fennec|
            Iris|
            Maemo|
            Minimo|
            Mobi|
            mowser|
            NetFront|
            Novarra|
            Prism|
            RX-34|
            Skyfire|
            Tear|
            XV6875|
            XV6975|
            Google.Wireless.Transcoder
        """, re.VERBOSE | re.IGNORECASE),
        'windows': re.compile(r'Windows.NT.5', re.IGNORECASE),
        'opera': re.compile(r""" # Opera mobile UAs.
            HTC|
            Xda|
            Mini|
            Vario|
            SAMSUNG\-GT\-i8000|
            SAMSUNG\-SGH\-i9
        """, re.VERBOSE | re.IGNORECASE),
    },
    'desktop': {
        'windows': re.compile(r'Windows.(NT|XP|ME|9)'), # Case sensitive.
        'win': re.compile(r'Win(9|.9|NT)', re.IGNORECASE),
        'mac': re.compile(r'Macintosh|PowerPC', re.IGNORECASE),
        'nix': re.compile(r'Solaris|SunOS|BSD', re.IGNORECASE),
    },
    'robots': {
        'bots': re.compile(r""" # Search engines.
            Bot|
            Crawler|
            Spider|
            Yahoo|
            ia_archiver|
            Covario-IDS|
            findlinks|
            DataparkSearch|
            larbin|
            Mediapartners-Google|
            NG-Search|
            Snappy|
            Teoma|
            Jeeves|
            TinEye
        """, re.VERBOSE | re.IGNORECASE),
    },
}


class Device:
    """Class wrapper for results.

    Arguments:
    category -- String classification of device.

    Properties:
    category -- String classification of device: mobile|desktop|tablet|tv (default: mobile)
    desktop -- Boolean classification representing desktop.
    mobile -- Boolean classification representing mobile.
    tablet -- Boolean classification representing tablet.
    tv -- Boolean classification representing tv.
    """

    def __init__(self, category):
        if category not in ['mobile', 'tablet', 'desktop', 'tv']:
            category = 'mobile'
        self.category = category
        self.desktop = (category == 'desktop')
        self.mobile = (category == 'mobile')
        self.tablet = (category == 'tablet')
        self.tv = (category == 'tv')


class Categorizr:
    """Mobile first User Agent detection.

    Usage:  Call the .detect() method passing in a user agent string.

    Keyword arguments:
    tablets_as_desktops -- Report tablets as desktop. (default: False)
    tvs_as_desktops -- Report tablets as desktop. (default: False)
    robots_as_mobile -- Report search engine robots as mobile. (default: False)
    """

    def __init__(
        self,
        tablets_as_desktops=False,
        tvs_as_desktops=False,
        robots_as_mobile=False,
    ):
        self.tablets_as_desktops = tablets_as_desktops # Override tablets.
        self.tvs_as_desktops = tvs_as_desktops # Override TVs.
        self.robots_as_mobile = robots_as_mobile # Override robots.

    def _find(self, needle, haystack):
        """Short cut function for a case insensitive string find."""
        return haystack.lower().find(needle.lower()) > -1

    def _is_tv(self, user_agent):
        # Check if user agent is a smart TV - http://goo.gl/FocDk
        if _detection['tv']['smart_tv'].search(user_agent):
            return True
        # Check if user agent is a TV Based Gaming Console.
        if _detection['tv']['console'].search(user_agent):
            return True

    def _is_tablet(self, user_agent):
        # Check if user agent is a Tablet.
        if _detection['tablet']['ipad'].search(user_agent) or \
                self._find('tablet', user_agent) and \
                not self._find('RX-34', user_agent) or \
                self._find('FOLIO', user_agent):
            return True
        # Check if user agent is an Android Tablet.
        if self._find('linux', user_agent) and \
                self._find('android', user_agent) and \
                not _detection['tablet']['mobiles'].search(user_agent):
            return True
        # Check if user agent is a Kindle or Kindle Fire.
        if self._find('Kindle', user_agent) or \
                _detection['tablet']['mac'].search(user_agent) and \
                self._find('Silk', user_agent):
            return True
        # Check if user agent is a pre Android 3.0 Tablet.
        if _detection['tablet']['android'].search(user_agent) or \
                self._find('MB511', user_agent) and \
                self._find('RUTEM', user_agent):
            return True

    def _is_mobile(self, user_agent):
        # Check if user agent is unique Mobile User Agent.
        if _detection['mobile']['unique'].search(user_agent):
            return True
        # Check if user agent is an odd Opera User Agent - http://goo.gl/nK90K
        if self._find('Opera', user_agent) and \
                _detection['mobile']['windows'].search(user_agent) and \
                _detection['mobile']['opera'].search(user_agent):
            return True

    def _is_desktop(self, user_agent):
        # Check if user agent is Windows Desktop.
        if _detection['desktop']['windows'].search(user_agent) and \
                not self._find('Phone', user_agent) or \
                _detection['desktop']['win'].search(user_agent):
            return True
        #Check if agent is Mac Desktop.
        if _detection['desktop']['mac'].search(user_agent) and \
                not self._find('Silk', user_agent):
            return True
        # Check if user agent is a Linux Desktop.
        if self._find('Linux', user_agent) and \
                self._find('X11', user_agent):
            return True
        # Check if user agent is a Solaris, SunOS, BSD Desktop.
        if _detection['desktop']['nix'].search(user_agent):
            return True

    def _is_robot(self, user_agent):
        # Check if user agent is a BOT/Crawler/Spider.
        if _detection['robots']['bots'].search(user_agent):
            return True

    def detect(self, user_agent):
        """Categorises a user agent as desktop, mobile, tv or tablet.

        Returns:  A categorizr.Device instance representing the classification.

        Arguments:
        user_agent -- User agent string to categorise.
        """
        category = 'mobile' # Mobile first.

        # Main detection cascade.
        if self._is_tv(user_agent):
            category = 'tv'
        elif self._is_tablet(user_agent):
            category = 'tablet'
        elif self._is_mobile(user_agent):
            category = 'mobile'
        elif self._is_desktop(user_agent):
            category = 'desktop'
        elif self._is_robot(user_agent) and not self.robots_as_mobile:
            category = 'desktop'

        # Sort out overrides.
        if self.tablets_as_desktops and category == 'tablet':
            category = 'desktop'
        if self.tvs_as_desktops and category == 'tv':
            category = 'desktop'

        # Send back the results as a Device object.
        return Device(category)
