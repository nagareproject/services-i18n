# Encoding: utf-8

# --
# Copyright (c) 2008-2018 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import datetime

import pytz
from nagare import local, i18n
from nagare.i18n import Locale


def setup_module(module):
    local.request = local.Process()
    i18n.set_locale(i18n.Locale('fr', 'FR'))


def test_get_period_names():
    assert i18n.get_period_names() == {
        'afternoon1': u'après-midi',
        'am': u'AM',
        'evening1': u'soir',
        'midnight': u'minuit',
        'morning1': u'matin',
        'night1': u'nuit',
        'noon': u'midi',
        'pm': u'PM'
    }


def test_get_day_names():
    assert i18n.get_day_names() == {0: u'lundi', 1: u'mardi', 2: u'mercredi', 3: u'jeudi', 4: u'vendredi', 5: u'samedi', 6: u'dimanche'}
    assert i18n.get_day_names(width='wide') == {0: u'lundi', 1: u'mardi', 2: u'mercredi', 3: u'jeudi', 4: u'vendredi', 5: u'samedi', 6: u'dimanche'}
    assert i18n.get_day_names(width='abbreviated') == {0: u'lun.', 1: u'mar.', 2: u'mer.', 3: u'jeu.', 4: u'ven.', 5: u'sam.', 6: u'dim.'}
    assert i18n.get_day_names(width='narrow') == {0: u'L', 1: u'M', 2: u'M', 3: u'J', 4: u'V', 5: u'S', 6: u'D'}


def test_get_month_names():
    assert i18n.get_month_names() == {1: u'janvier', 2: u'février', 3: u'mars', 4: u'avril', 5: u'mai', 6: u'juin', 7: u'juillet', 8: u'août', 9: u'septembre', 10: u'octobre', 11: u'novembre', 12: u'décembre'}
    assert i18n.get_month_names(width='wide') == {1: u'janvier', 2: u'février', 3: u'mars', 4: u'avril', 5: u'mai', 6: u'juin', 7: u'juillet', 8: u'août', 9: u'septembre', 10: u'octobre', 11: u'novembre', 12: u'décembre'}
    assert i18n.get_month_names(width='abbreviated') == {1: u'janv.', 2: u'févr.', 3: u'mars', 4: u'avr.', 5: u'mai', 6: u'juin', 7: u'juil.', 8: u'août', 9: u'sept.', 10: u'oct.', 11: u'nov.', 12: u'déc.'}
    assert i18n.get_month_names(width='narrow') == {1: u'J', 2: u'F', 3: u'M', 4: u'A', 5: u'M', 6: u'J', 7: u'J', 8: u'A', 9: u'S', 10: u'O', 11: u'N', 12: u'D'}


def test_get_quarter_names():
    assert i18n.get_quarter_names() == {1: u'1er trimestre', 2: u'2e trimestre', 3: u'3e trimestre', 4: u'4e trimestre'}
    assert i18n.get_quarter_names(width='wide') == {1: u'1er trimestre', 2: u'2e trimestre', 3: u'3e trimestre', 4: u'4e trimestre'}
    assert i18n.get_quarter_names(width='abbreviated') == {1: u'T1', 2: u'T2', 3: u'T3', 4: u'T4'}
    assert i18n.get_quarter_names(width='narrow') == {1: u'1', 2: u'2', 3: u'3', 4: u'4'}


def test_get_era_names():
    locale = i18n.Locale('en', 'US')

    assert locale.get_era_names() == {0: u'Before Christ', 1: u'Anno Domini'}
    assert locale.get_era_names(width='wide') == {0: u'Before Christ', 1: u'Anno Domini'}
    assert locale.get_era_names(width='abbreviated') == {0: u'BC', 1: u'AD'}
    assert locale.get_era_names(width='narrow') == {0: u'B', 1: u'A'}


def test_get_date_format():
    assert i18n.get_date_format(format='full').pattern == 'EEEE d MMMM y'
    assert i18n.get_date_format(format='long').pattern == 'd MMMM y'
    assert i18n.get_date_format().pattern == 'd MMM y'
    assert i18n.get_date_format(format='medium').pattern == 'd MMM y'
    assert i18n.get_date_format(format='short').pattern == 'dd/MM/y'


def test_get_datetime_format():
    assert i18n.get_datetime_format(format='full') == u"{1} 'à' {0}"
    assert i18n.get_datetime_format(format='long') == u"{1} 'à' {0}"
    assert i18n.get_datetime_format() == u"{1} 'à' {0}"
    assert i18n.get_datetime_format(format='medium') == u"{1} 'à' {0}"
    assert i18n.get_datetime_format(format='short') == u'{1} {0}'


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

    assert i18n.get_timezone_gmt(d, width='long') == u'UTC-08:00'
    assert i18n.get_timezone_gmt(d) == u'UTC-08:00'
    assert i18n.get_timezone_gmt(d, width='short') == '-0800'

    locale = i18n.Locale('en', 'US')

    assert locale.get_timezone_gmt(d, width='long') == u'GMT-08:00'
    assert locale.get_timezone_gmt(d) == u'GMT-08:00'
    assert locale.get_timezone_gmt(d, width='short') == '-0800'


def test_get_timezone_location():
    tz = pytz.timezone('Africa/Bamako')
    assert i18n.get_timezone_location(tz) == 'Mali'


def test_get_timezone_name():
    utc_date = datetime.datetime(2007, 4, 1, 15, 30)

    tz = pytz.timezone('Pacific/Pitcairn')
    d = Locale('en', timezone=tz).to_timezone(utc_date)

    assert i18n.get_timezone_name(d) == u'heure des îles Pitcairn'
    assert i18n.get_timezone_name(d, width='long') == u'heure des îles Pitcairn'
    assert i18n.get_timezone_name(d, width='short') == '-0800'
