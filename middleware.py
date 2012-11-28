from hashlib import md5

from django.conf import settings
from django.core.cache import cache

from __init__ import Categorizr

"""
You can set the options for Categorizr in Django's settings.
This should be a dictionary in the following format:

CATEGORIZR = {
    'tablets_as_desktops' = False,
    'tvs_as_desktops' = False,
    'robots_as_mobile' = False,
}
"""

try:
    c = Categorizr(**settings.CATEGORIZR)
except AttributeError:
    c = Categorizr()

class CategorizrMiddleware():
    """
    Adds CATEGORIZR to the request object.  This will be a Device object -
    see the Categorizr implementation for details.
    """

    def process_request(self, request):
        ua = request.META.get('HTTP_USER_AGENT', '')
        # Make this safe for memcache.
        key = 'categorizr::%s' % (md5(ua).hexdigest())
        category = cache.get(key)
        if category is None:
            category = c.detect(ua)
        request.CATEGORIZR = category
