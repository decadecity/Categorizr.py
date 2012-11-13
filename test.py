import simplejson
import unittest

from __init__ import Categorizr, Device

#c = Categorizr()

class TestDevice(unittest.TestCase):
    """Test the Device class that handles results of testing."""

    def test_device_mobile(self):
        d = Device('mobile')
        self.assertEqual(d.category, 'mobile')
        self.assertTrue(d.mobile)
        self.assertFalse(d.tablet)
        self.assertFalse(d.desktop)
        self.assertFalse(d.tv)

    def test_device_tablet(self):
        d = Device('tablet')
        self.assertEqual(d.category, 'tablet')
        self.assertFalse(d.mobile)
        self.assertTrue(d.tablet)
        self.assertFalse(d.desktop)
        self.assertFalse(d.tv)

    def test_device_desktop(self):
        d = Device('desktop')
        self.assertEqual(d.category, 'desktop')
        self.assertFalse(d.mobile)
        self.assertFalse(d.tablet)
        self.assertTrue(d.desktop)
        self.assertFalse(d.tv)

    def test_device_tv(self):
        d = Device('tv')
        self.assertEqual(d.category, 'tv')
        self.assertFalse(d.mobile)
        self.assertFalse(d.tablet)
        self.assertFalse(d.desktop)
        self.assertTrue(d.tv)

    def test_device_other(self):
        d = Device('other')
        self.assertEqual(d.category, 'mobile')
        self.assertTrue(d.mobile)
        self.assertFalse(d.tablet)
        self.assertFalse(d.desktop)
        self.assertFalse(d.tv)

class TestCategorizr(unittest.TestCase):
    """Test the Categorizr class correctly matches UAs."""

    def test_find(self):
        """Ensure the find function can do a case insensitive find."""
        c = Categorizr()
        self.assertTrue(c._find('edc', 'MixedCase'))

    def test_overide_tablets(self):
        """Check that tablets can be overridden as desktop."""
        c = Categorizr()
        d = c.detect('tablet')
        self.assertEqual(d.category, 'tablet')
        c1 = Categorizr(tablets_as_desktops=True)
        d = c1.detect('tablet')
        self.assertEqual(d.category, 'desktop')

    def test_overide_tvs(self):
        """Check that TVs can be overridden as desktop."""
        c = Categorizr()
        d = c.detect('googletv')
        self.assertEqual(d.category, 'tv')
        c1 = Categorizr(tvs_as_desktops=True)
        d = c1.detect('googletv')
        self.assertEqual(d.category, 'desktop')

    def test_overide_robots(self):
        """Check that robots can be overridden as mobile."""
        c = Categorizr()
        d = c.detect('bot')
        self.assertEqual(d.category, 'desktop')
        c1 = Categorizr(robots_as_mobile=True)
        d = c1.detect('bot')
        self.assertEqual(d.category, 'mobile')

def add_test(cls, i, test):
    """
    This monkey patches a test function into a class.

    cls Class to which we add the test.
    i Unique identifier to name the test.
    test List of two items, the UA to test and the category we expect from it.
    """
    def inner_test(self):
        c = Categorizr()
        d = c.detect(test[0])
        self.assertEqual(d.category, test[1])
    inner_test.__name__ = "test_%s" % (i)
    inner_test.__doc__ = "Testing %s" % (test[0])
    setattr(cls,inner_test.__name__,inner_test)


if __name__ == '__main__':
    import sys
    import os
    import fcntl

    # Make stdin a non-blocking file.
    fd = sys.stdin.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    try:
        json = sys.stdin.read()
    except IOError:
        sys.stderr.write('Please supply JSON test data via STDIN.\n')
        sys.exit(1)
    try:
        user_agents = simplejson.loads(json)
    except simplejson.decoder.JSONDecodeError:
        sys.stderr.write('Test data was not valid JSON.\n')
        sys.exit(1)

    # Monkey patch the tests from the JSON data into the Categorizr test class.
    i = 0
    for test in user_agents:
        if len(test) != 3:
            sys.stderr.write('The JSON test data appears to be in the wrong format.\n')
            sys.exit(1)
        test_ua = [test[0], test[1]]
        add_test(TestCategorizr, i, test_ua)
        i += 1
        if test[2] == "i":
            # We need test in a case insensitive manner.
            test_ua = [test[0].lower(), test[1]]
            add_test(TestCategorizr, i, test_ua)
            i += 1
            test_ua = [test[0].upper(), test[1]]
            add_test(TestCategorizr, i, test_ua)
            i += 1

    unittest.main()
