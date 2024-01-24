# Encoding: utf-8

# --
# Copyright (c) 2008-2024 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import datetime

import pytz
from nagare import local, i18n


def setup_module(module):
    local.request = local.Process()


def test_to_timezone_no_timezone_datetime():
    d1 = datetime.datetime(2007, 4, 1, 15, 30)

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_timezone(d1)
    assert d2.tzinfo is None
    assert d2.strftime('%H:%M') == '15:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Pacific/Pitcairn'))
    d2 = i18n.to_timezone(d1)
    assert str(d2.tzinfo) == 'Pacific/Pitcairn'
    assert d2.strftime('%H:%M') == '15:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Pacific/Pitcairn', default_timezone=pytz.UTC))
    d2 = i18n.to_timezone(d1)
    assert str(d2.tzinfo) == 'Pacific/Pitcairn'
    assert d2.strftime('%H:%M') == '07:30'


def test_to_timezone_utc_datetime():
    d1 = datetime.datetime(2007, 4, 1, 15, 30, tzinfo=pytz.UTC)

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_timezone(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '15:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Pacific/Pitcairn'))
    d2 = i18n.to_timezone(d1)
    assert str(d2.tzinfo) == 'Pacific/Pitcairn'
    assert d2.strftime('%H:%M') == '07:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Pacific/Pitcairn', default_timezone=pytz.UTC))
    d2 = i18n.to_timezone(d1)
    assert str(d2.tzinfo) == 'Pacific/Pitcairn'
    assert d2.strftime('%H:%M') == '07:30'


def test_to_timezone_local_datetime():
    tz = pytz.timezone('Pacific/Pitcairn')
    d1 = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_timezone(d1)
    assert str(d2.tzinfo) == 'Pacific/Pitcairn'
    assert d2.strftime('%H:%M') == '15:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_timezone(d1)
    assert str(d2.tzinfo) == 'Africa/Niamey'
    assert d2.strftime('%H:%M') == '00:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_timezone(d1)
    assert str(d2.tzinfo) == 'Africa/Niamey'
    assert d2.strftime('%H:%M') == '00:30'


def test_to_utc_no_timezone_datetime():
    d1 = datetime.datetime(2007, 4, 1, 15, 30)

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_utc(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '15:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_utc(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '14:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_utc(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '15:30'


def test_to_utc_utc_datetime():
    d1 = datetime.datetime(2007, 4, 1, 15, 30, tzinfo=pytz.UTC)

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_utc(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '15:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_utc(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '15:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_utc(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '15:30'


def test_to_utc_local_datetime():
    tz = pytz.timezone('Pacific/Pitcairn')
    d1 = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_utc(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '23:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_utc(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '23:30'

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_utc(d1)
    assert str(d2.tzinfo) == 'UTC'
    assert d2.strftime('%H:%M') == '23:30'


def test_format_time_time_fr1():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    t = datetime.time(15, 30)

    assert i18n.format_time(t, format='full') == u'15:30:00 temps universel coordonné'
    assert i18n.format_time(t, format='long') == '15:30:00 TU'
    assert i18n.format_time(t, format='medium') == '15:30:00'
    assert i18n.format_time(t) == '15:30:00'
    assert i18n.format_time(t, format='short') == '15:30'


def test_format_time_time_fr2():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    t = datetime.time(15, 30)

    assert i18n.format_time(t, format='full') == u'15:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(t, format='long') == '15:30:00 +0100'
    assert i18n.format_time(t, format='medium') == '15:30:00'
    assert i18n.format_time(t) == '15:30:00'
    assert i18n.format_time(t, format='short') == '15:30'


def test_format_time_time_fr3():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    t = datetime.time(15, 30, tzinfo=pytz.timezone('Pacific/Pitcairn'))

    assert i18n.format_time(t, format='full') == u'15:30:00 temps universel coordonné'
    assert i18n.format_time(t, format='long') == '15:30:00 TU'
    assert i18n.format_time(t, format='medium') == '15:30:00'
    assert i18n.format_time(t) == '15:30:00'
    assert i18n.format_time(t, format='short') == '15:30'


def test_format_time_time_fr4():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    t = datetime.time(15, 30, tzinfo=pytz.timezone('Pacific/Pitcairn'))

    assert i18n.format_time(t, format='full') == u'15:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(t, format='long') == '15:30:00 +0100'
    assert i18n.format_time(t, format='medium') == '15:30:00'
    assert i18n.format_time(t) == '15:30:00'
    assert i18n.format_time(t, format='short') == '15:30'


def test_format_time_time_en():
    i18n.set_locale(i18n.Locale('en', 'US', timezone='Pacific/Pitcairn'))

    t = datetime.time(15, 30)

    assert i18n.format_time(t, format='full').encode('ascii', 'ignore') == b'3:30:00PM Pitcairn Time'
    assert i18n.format_time(t, format='long').encode('ascii', 'ignore') == b'3:30:00PM -0800'
    assert i18n.format_time(t, format='medium').encode('ascii', 'ignore') == b'3:30:00PM'
    assert i18n.format_time(t).encode('ascii', 'ignore') == b'3:30:00PM'
    assert i18n.format_time(t, format='short').encode('ascii', 'ignore') == b'3:30PM'


def test_format_time_time_with_format():
    i18n.set_locale(i18n.Locale('en', 'US', timezone='Pacific/Pitcairn'))

    t = datetime.time(15, 30)
    assert i18n.format_time(t, format="hh 'o''clock' a, zzzz") == "03 o'clock PM, Pitcairn Time"

    t = datetime.time(15, 30, tzinfo=pytz.timezone('Africa/Niamey'))
    assert i18n.format_time(t, format="hh 'o''clock' a, zzzz") == "03 o'clock PM, Pitcairn Time"


def test_format_time_datetime_fr1():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    d = datetime.datetime(2007, 4, 1, 15, 30)

    assert i18n.format_time(d, format='full') == u'15:30:00 temps universel coordonné'
    assert i18n.format_time(d, format='long') == '15:30:00 TU'
    assert i18n.format_time(d, format='medium') == '15:30:00'
    assert i18n.format_time(d) == '15:30:00'
    assert i18n.format_time(d, format='short') == '15:30'


def test_format_time_datetime_fr2():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    d = datetime.datetime(2007, 4, 1, 15, 30)

    assert i18n.format_time(d, format='full') == u'15:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(d, format='long') == '15:30:00 +0100'
    assert i18n.format_time(d, format='medium') == '15:30:00'
    assert i18n.format_time(d) == '15:30:00'
    assert i18n.format_time(d, format='short') == '15:30'


def test_format_time_datetime_fr3():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))

    d = datetime.datetime(2007, 4, 1, 15, 30)

    assert i18n.format_time(d, format='full') == u'16:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(d, format='long') == '16:30:00 +0100'
    assert i18n.format_time(d, format='medium') == '16:30:00'
    assert i18n.format_time(d) == '16:30:00'
    assert i18n.format_time(d, format='short') == '16:30'


def test_format_time_datetime_fr4():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.format_time(d, format='full') == u'23:30:00 temps universel coordonné'
    assert i18n.format_time(d, format='long') == '23:30:00 TU'
    assert i18n.format_time(d, format='medium') == '23:30:00'
    assert i18n.format_time(d) == '23:30:00'
    assert i18n.format_time(d, format='short') == '23:30'


def test_format_time_datetime_fr5():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.format_time(d, format='full') == u'00:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(d, format='long') == '00:30:00 +0100'
    assert i18n.format_time(d, format='medium') == '00:30:00'
    assert i18n.format_time(d) == '00:30:00'
    assert i18n.format_time(d, format='short') == '00:30'


def test_format_time_datetime_with_format():
    i18n.set_locale(i18n.Locale('en', 'US', timezone='Pacific/Pitcairn'))

    d = datetime.datetime(2007, 4, 1, 15, 30)
    assert i18n.format_time(d, format="hh 'o''clock' a, zzzz") == u"03 o'clock PM, Pitcairn Time"

    tz = pytz.timezone('Africa/Niamey')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))
    assert i18n.format_time(d, format="hh 'o''clock' a, zzzz") == u"06 o'clock AM, Pitcairn Time"


def test_format_date_date():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    d = datetime.date(2007, 4, 1)

    assert i18n.format_date(d, format='full') == 'dimanche 1 avril 2007'
    assert i18n.format_date(d, format='long') == '1 avril 2007'
    assert i18n.format_date(d, format='medium') == '1 avr. 2007'
    assert i18n.format_date(d) == '1 avr. 2007'
    assert i18n.format_date(d, format='short') == '01/04/2007'


def test_format_date_datetime():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.format_date(d, format='full') == 'dimanche 1 avril 2007'
    assert i18n.format_date(d, format='long') == '1 avril 2007'
    assert i18n.format_date(d, format='medium') == '1 avr. 2007'
    assert i18n.format_date(d) == '1 avr. 2007'
    assert i18n.format_date(d, format='short') == '01/04/2007'


def test_format_date_date_with_format():
    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d = datetime.date(2007, 4, 1)

    assert i18n.format_date(d, 'EEE, MMM d, yy') == 'dim., avr. 1, 07'


def test_format_datetime():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.format_datetime(d, format='full') == u'lundi 2 avril 2007, 00:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_datetime(d, format='long') == u'2 avril 2007, 00:30:00 +0100'
    assert i18n.format_datetime(d, format='medium') == u'2 avr. 2007, 00:30:00'
    assert i18n.format_datetime(d) == u'2 avr. 2007, 00:30:00'
    assert i18n.format_datetime(d, format='short') == '02/04/2007 00:30'


def test_format_datetime_with_format():
    i18n.set_locale(i18n.Locale('en', 'US', timezone='Pacific/Pitcairn'))

    d = datetime.datetime(2007, 4, 1, 15, 30)
    assert i18n.format_datetime(d, format="yyyy.MM.dd G 'at' HH:mm:ss zzz") == '2007.04.01 AD at 15:30:00 -0800'

    tz = pytz.timezone('Africa/Niamey')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))
    assert i18n.format_datetime(d, format="yyyy.MM.dd G 'at' HH:mm:ss zzz") == '2007.04.01 AD at 06:30:00 -0800'
