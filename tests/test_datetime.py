# Encoding: utf-8

# --
# Copyright (c) 2008-2020 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import datetime

import pytz
import pytest
from nagare import local

from nagare import i18n
from nagare.i18n import Locale, set_locale


def setup_module(module):
    local.request = local.Process()


def test_format_datetime():
    set_locale(Locale('en', 'US'))
    dt = datetime.datetime(2007, 4, 1, 15, 30)
    assert i18n.format_datetime(dt) == 'Apr 1, 2007, 3:30:00 PM'

    set_locale(Locale('fr', 'FR', timezone=pytz.timezone('Europe/Paris'), default_timezone=pytz.UTC))
    dt = datetime.datetime(2007, 4, 1, 15, 30)
    assert i18n.format_datetime(dt, 'full') == u'dimanche 1 avril 2007 à 17:30:00 heure d’été d’Europe centrale'

    set_locale(Locale('en', timezone=pytz.timezone('US/Eastern'), default_timezone=pytz.UTC))
    assert i18n.format_datetime(dt, "yyyy.MM.dd G 'at' HH:mm:ss zzz") == '2007.04.01 AD at 11:30:00 EDT'


def test_format_date():
    d = datetime.date(2007, 4, 1)

    set_locale(Locale('en', 'US'))
    assert i18n.format_date(d) == 'Apr 1, 2007'

    set_locale(Locale('de', 'DE'))
    assert i18n.format_date(d, format='full') == 'Sonntag, 1. April 2007'

    set_locale(Locale('en'))
    assert i18n.format_date(d, "EEE, MMM d, ''yy") == "Sun, Apr 1, '07"


def test_format_time():
    t = datetime.time(15, 30)

    set_locale(Locale('en', 'US'))
    assert i18n.format_time(t) == '3:30:00 PM'

    set_locale(Locale('de', 'DE'))
    assert i18n.format_time(t, format='short') == '15:30'

    set_locale(Locale('en'))
    assert i18n.format_time(t, "hh 'o''clock' a") == "03 o'clock PM"


def test_format_timedelta():
    set_locale(Locale('en', 'US'))
    assert i18n.format_timedelta(datetime.timedelta(weeks=12)) == '3 months'

    set_locale(Locale('es'))
    assert i18n.format_timedelta(1) == u'1 segundo'

    set_locale(Locale('en', 'US'))
    assert i18n.format_timedelta(datetime.timedelta(hours=3), granularity='day') == '1 day'

    set_locale(Locale('en', 'US'))
    assert i18n.format_timedelta(datetime.timedelta(hours=23), threshold=0.9) == '1 day'
    assert i18n.format_timedelta(datetime.timedelta(hours=23), threshold=1.1) == '23 hours'

    set_locale(Locale('fr', 'FR'))
    assert i18n.format_timedelta(datetime.timedelta(hours=1), add_direction=True) == 'dans 1 heure'
    assert i18n.format_timedelta(datetime.timedelta(hours=-1), add_direction=True) == 'il y a 1 heure'

    set_locale(Locale('en'))
    assert i18n.format_timedelta(datetime.timedelta(hours=3), format='short') == '3 hr'
    assert i18n.format_timedelta(datetime.timedelta(hours=3), format='narrow') == '3h'


def test_format_skeleton():
    t = datetime.datetime(2007, 4, 1, 15, 30)

    set_locale(Locale('fr'))
    assert i18n.format_skeleton('MMMEd', t) == 'dim. 1 avr.'

    set_locale(Locale('en'))
    assert i18n.format_skeleton('MMMEd', t) == 'Sun, Apr 1'

    set_locale(Locale('fi'))
    assert i18n.format_skeleton('yMMd', t) == '1.4.2007'
    with pytest.raises(KeyError, match='yMMd'):
        i18n.format_skeleton('yMMd', t, fuzzy=False)


def test_format_interval():
    set_locale(Locale('fi'))
    assert i18n.format_interval(datetime.datetime(2016, 1, 15), datetime.datetime(2016, 1, 17), 'yMd') == u'15.\u201317.1.2016'

    set_locale(Locale('en', 'GB'))
    assert i18n.format_interval(datetime.time(12, 12), datetime.time(16, 16), 'Hm') == u'12:12\u201316:16'

    set_locale(Locale('en', 'US'))
    assert i18n.format_interval(datetime.time(5, 12), datetime.time(16, 16), 'hm') == u'5:12 AM \u2013 4:16 PM'

    set_locale(Locale('it'))
    assert i18n.format_interval(datetime.time(16, 18), datetime.time(16, 24), 'Hm') == u'16:18\u201316:24'
    assert i18n.format_interval(datetime.time(16, 18), datetime.time(16, 18), 'Hm') == '16:18'

    set_locale(Locale('ja'))
    assert i18n.format_interval(datetime.date(2015, 1, 1), datetime.date(2017, 1, 1), 'wzq') == u'2015/01/01\uff5e2017/01/01'

    set_locale(Locale('ja'))
    assert i18n.format_interval(datetime.time(16, 18), datetime.time(16, 24), 'xxx') == u'16:18:00\uff5e16:24:00'

    set_locale(Locale('de'))
    assert i18n.format_interval(datetime.date(2016, 1, 15), datetime.date(2016, 1, 17), 'xxx') == u'15.01.2016 \u2013 17.01.2016'


def test_get_timezone_gmt():
    dt = datetime.datetime(2007, 4, 1, 15, 30)

    set_locale(Locale('en'))
    assert i18n.get_timezone_gmt(dt) == 'GMT+00:00'
    assert i18n.get_timezone_gmt(dt, return_z=True) == 'Z'
    assert i18n.get_timezone_gmt(dt, width='iso8601_short') == '+00'

    dt = Locale(timezone='America/Los_Angeles').to_timezone(datetime.datetime(2007, 4, 1, 15, 30))
    assert i18n.get_timezone_gmt(dt) == 'GMT-07:00'

    set_locale(Locale('en'))
    assert i18n.get_timezone_gmt(dt, 'short') == '-0700'
    assert i18n.get_timezone_gmt(dt, width='iso8601_short') == '-07'

    set_locale(Locale('fr', 'FR'))
    assert i18n.get_timezone_gmt(dt, 'long') == 'UTC-07:00'


def test_get_timezone_location():
    set_locale(Locale('de', 'DE'))
    tz = pytz.timezone('America/St_Johns')
    assert i18n.get_timezone_location(tz) == u'Kanada (St. John’s)'

    set_locale(Locale('de', 'DE'))
    tz = pytz.timezone('America/Mexico_City')
    assert i18n.get_timezone_location(tz) == 'Mexiko (Mexiko-Stadt)'


def test_get_timezone_name():
    dt = Locale(timezone='America/Los_Angeles').to_timezone(datetime.datetime.now())
    set_locale(Locale('en', 'US'))
    assert i18n.get_timezone_name(dt) in ('Pacific Standard Time', 'Pacific Daylight Time')
    assert i18n.get_timezone_name(dt, return_zone=True) == 'America/Los_Angeles'
    assert i18n.get_timezone_name(dt, width='short') in ('PST', 'PDT')

    tz = pytz.timezone('America/Los_Angeles')
    assert i18n.get_timezone_name(tz) == 'Pacific Time'
    assert i18n.get_timezone_name(tz, 'short') == 'PT'

    set_locale(Locale('de', 'DE'))
    tz = pytz.timezone('Europe/Berlin')
    assert i18n.get_timezone_name(tz) == u'Mitteleurop\xe4ische Zeit'

    set_locale(Locale('pt', 'BR'))
    assert i18n.get_timezone_name(tz) == u'Hor\xe1rio da Europa Central'

    set_locale(Locale('de', 'DE'))
    tz = pytz.timezone('America/St_Johns')
    assert i18n.get_timezone_name(tz) == u'Neufundland-Zeit'


def test_get_period_names():
    set_locale(Locale('en', 'US'))

    assert i18n.get_period_names()['am'] == 'AM'


def test_get_day_names():
    set_locale(Locale('en', 'US'))
    assert i18n.get_day_names('wide')[1] == 'Tuesday'

    set_locale(Locale('es'))
    assert i18n.get_day_names('abbreviated')[1] == 'mar.'

    set_locale(Locale('de', 'DE'))
    assert i18n.get_day_names('narrow', context='stand-alone')[1] == 'D'


def test_get_month_names():
    set_locale(Locale('en', 'US'))
    assert i18n.get_month_names('wide')[1] == 'January'

    set_locale(Locale('es'))
    assert i18n.get_month_names('abbreviated')[1] == 'ene.'

    set_locale(Locale('de', 'DE'))
    assert i18n.get_month_names('narrow', context='stand-alone')[1] == 'J'


def test_get_quarter_names():
    set_locale(Locale('en', 'US'))
    assert i18n.get_quarter_names('wide')[1] == '1st quarter'

    set_locale(Locale('de', 'DE'))
    assert i18n.get_quarter_names('abbreviated')[1] == 'Q1'


def test_get_era_names():
    set_locale(Locale('en', 'US'))
    assert i18n.get_era_names('wide')[1] == 'Anno Domini'

    set_locale(Locale('de', 'DE'))
    assert i18n.get_era_names('abbreviated')[1] == 'n. Chr.'


def test_get_date_format():
    set_locale(Locale('en', 'US'))
    assert str(i18n.get_date_format()) == 'MMM d, y'

    set_locale(Locale('de', 'DE'))
    assert str(i18n.get_date_format()) == 'dd.MM.y'


def test_get_datetime_format():
    set_locale(Locale('en', 'US'))
    assert i18n.get_datetime_format() == '{1}, {0}'


def test_get_time_format():
    set_locale(Locale('en', 'US'))
    assert str(i18n.get_time_format()) == 'h:mm:ss a'

    set_locale(Locale('de', 'DE'))
    assert str(i18n.get_time_format('full')) == 'HH:mm:ss zzzz'


def test_parse_date():
    set_locale(Locale('en', 'US'))
    assert i18n.parse_date('4/1/04') == datetime.date(2004, 4, 1)

    set_locale(Locale('de', 'DE'))
    assert i18n.parse_date('01.04.2004') == datetime.date(2004, 4, 1)


def test_parse_time():
    set_locale(Locale('en', 'US'))
    assert i18n.parse_time('15:30:00') == datetime.time(15, 30)


def test_parse_pattern():
    assert i18n.parse_pattern('MMMMd').format == '%(MMMM)s%(d)s'
    assert i18n.parse_pattern('MMM d, yyyy').format == '%(MMM)s %(d)s, %(yyyy)s'
    assert i18n.parse_pattern("H:mm' Uhr 'z").format == '%(H)s:%(mm)s Uhr %(z)s'
    assert i18n.parse_pattern("hh' o''clock'").format == "%(hh)s o'clock"
