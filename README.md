#Categorizr.py

Python port of [Categorizr](https://github.com/bjankord/Categorizr)

##Usage

    from categorizr import Categorizr

    c = Categorizr()

    device = c.detect('user agent')

    if (device.desktop):
        print('Device is a desktop.')
    if (device.mobile):
        print('Device is a mobile.')
    if (device.tablet):
        print('Device is a tablet.')
    if (device.tv):
        print('Device is a TV.')

###Options

    c = Categorizr(tablets_as_desktops=True) # Class tablets a a desktop.
    c = Categorizr(tvs_as_desktops=True) # Class TVs a desktop.
    c = Categorizr(robots_as_mobile=True) # Class search engines as mobile.
