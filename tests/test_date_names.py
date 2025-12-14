# --
# Copyright (c) 2014-2025 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import datetime

import pytz

from nagare import i18n, local
from nagare.i18n import Locale


def setup_module(module):
    local.request = local.Process()
    i18n.set_locale(i18n.Locale('fr', 'FR'))


def test_get_period_names():
    assert i18n.get_period_names() == {
        'morning1': 'matin',
        'afternoon1': 'après-midi',
        'evening1': 'soir',
        'night1': 'matin',
    }


def test_get_day_names():
    assert i18n.get_day_names() == {
        0: 'lundi',
        1: 'mardi',
        2: 'mercredi',
        3: 'jeudi',
        4: 'vendredi',
        5: 'samedi',
        6: 'dimanche',
    }
    assert i18n.get_day_names(width='wide') == {
        0: 'lundi',
        1: 'mardi',
        2: 'mercredi',
        3: 'jeudi',
        4: 'vendredi',
        5: 'samedi',
        6: 'dimanche',
    }
    assert i18n.get_day_names(width='abbreviated') == {
        0: 'lun.',
        1: 'mar.',
        2: 'mer.',
        3: 'jeu.',
        4: 'ven.',
        5: 'sam.',
        6: 'dim.',
    }
    assert i18n.get_day_names(width='narrow') == {0: 'L', 1: 'M', 2: 'M', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}


def test_get_month_names():
    assert i18n.get_month_names() == {
        1: 'janvier',
        2: 'février',
        3: 'mars',
        4: 'avril',
        5: 'mai',
        6: 'juin',
        7: 'juillet',
        8: 'août',
        9: 'septembre',
        10: 'octobre',
        11: 'novembre',
        12: 'décembre',
    }
    assert i18n.get_month_names(width='wide') == {
        1: 'janvier',
        2: 'février',
        3: 'mars',
        4: 'avril',
        5: 'mai',
        6: 'juin',
        7: 'juillet',
        8: 'août',
        9: 'septembre',
        10: 'octobre',
        11: 'novembre',
        12: 'décembre',
    }
    assert i18n.get_month_names(width='abbreviated') == {
        1: 'janv.',
        2: 'févr.',
        3: 'mars',
        4: 'avr.',
        5: 'mai',
        6: 'juin',
        7: 'juil.',
        8: 'août',
        9: 'sept.',
        10: 'oct.',
        11: 'nov.',
        12: 'déc.',
    }
    assert i18n.get_month_names(width='narrow') == {
        1: 'J',
        2: 'F',
        3: 'M',
        4: 'A',
        5: 'M',
        6: 'J',
        7: 'J',
        8: 'A',
        9: 'S',
        10: 'O',
        11: 'N',
        12: 'D',
    }


def test_get_quarter_names():
    assert i18n.get_quarter_names() == {1: '1er trimestre', 2: '2e trimestre', 3: '3e trimestre', 4: '4e trimestre'}
    assert i18n.get_quarter_names(width='wide') == {
        1: '1er trimestre',
        2: '2e trimestre',
        3: '3e trimestre',
        4: '4e trimestre',
    }
    assert i18n.get_quarter_names(width='abbreviated') == {1: 'T1', 2: 'T2', 3: 'T3', 4: 'T4'}
    assert i18n.get_quarter_names(width='narrow') == {1: '1', 2: '2', 3: '3', 4: '4'}


def test_get_era_names():
    locale = i18n.Locale('en', 'US')

    assert locale.get_era_names() == {0: 'Before Christ', 1: 'Anno Domini'}
    assert locale.get_era_names(width='wide') == {0: 'Before Christ', 1: 'Anno Domini'}
    assert locale.get_era_names(width='abbreviated') == {0: 'BC', 1: 'AD'}
    assert locale.get_era_names(width='narrow') == {0: 'B', 1: 'A'}


def test_get_date_format():
    assert i18n.get_date_format(format='full').pattern == 'EEEE d MMMM y'
    assert i18n.get_date_format(format='long').pattern == 'd MMMM y'
    assert i18n.get_date_format().pattern == 'd MMM y'
    assert i18n.get_date_format(format='medium').pattern == 'd MMM y'
    assert i18n.get_date_format(format='short').pattern == 'dd/MM/y'


def test_get_datetime_format():
    assert i18n.get_datetime_format(format='full') == '{1}, {0}'
    assert i18n.get_datetime_format(format='long') == '{1}, {0}'
    assert i18n.get_datetime_format() == '{1}, {0}'
    assert i18n.get_datetime_format(format='medium') == '{1}, {0}'
    assert i18n.get_datetime_format(format='short') == '{1} {0}'


def test_get_time_format():
    assert i18n.get_time_format(format='full').pattern == 'HH:mm:ss zzzz'
    assert i18n.get_time_format(format='long').pattern == 'HH:mm:ss z'
    assert i18n.get_time_format().pattern == 'HH:mm:ss'
    assert i18n.get_time_format(format='medium').pattern == 'HH:mm:ss'
    assert i18n.get_time_format(format='short').pattern == 'HH:mm'


def test_get_timezone_gmt():
    utc_date = datetime.datetime(2007, 4, 1, 15, 30)

    tz = pytz.timezone('Pacific/Pitcairn')
    d = Locale('en', timezone=tz).to_timezone(utc_date)

    assert i18n.get_timezone_gmt(d, width='long') == 'UTC-08:00'
    assert i18n.get_timezone_gmt(d) == 'UTC-08:00'
    assert i18n.get_timezone_gmt(d, width='short') == '-0800'

    locale = i18n.Locale('en', 'US')

    assert locale.get_timezone_gmt(d, width='long') == 'GMT-08:00'
    assert locale.get_timezone_gmt(d) == 'GMT-08:00'
    assert locale.get_timezone_gmt(d, width='short') == '-0800'


def test_get_timezone_location():
    tz = pytz.timezone('Africa/Bamako')
    assert i18n.get_timezone_location(tz) == 'Mali'


def test_get_timezone_name():
    utc_date = datetime.datetime(2007, 4, 1, 15, 30)

    tz = pytz.timezone('Pacific/Pitcairn')
    d = Locale('en', timezone=tz).to_timezone(utc_date)

    assert i18n.get_timezone_name(d) == 'heure des îles Pitcairn'
    assert i18n.get_timezone_name(d, width='long') == 'heure des îles Pitcairn'
    assert i18n.get_timezone_name(d, width='short') == '-0800'
