# Encoding: utf-8

# --
# Copyright (c) 2008-2021 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import datetime

from nagare import local, i18n


def setup_module(module):
    local.request = local.Process()
    i18n.set_locale(i18n.Locale('fr', 'FR'))


def test_parse_time_fr():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    t = i18n.parse_time('15:30:10')
    assert isinstance(t, datetime.time)
    assert (t.hour, t.minute, t.second) == (15, 30, 10)


def test_parse_time_en():
    i18n.set_locale(i18n.Locale('en', 'US'))

    t = i18n.parse_time('15:30:10')
    assert isinstance(t, datetime.time)
    assert (t.hour, t.minute, t.second) == (15, 30, 10)


def test_parse_date_fr():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    d = i18n.parse_date('4/1/04')
    assert isinstance(d, datetime.date)
    assert (d.year, d.month, d.day) == (2004, 1, 4)

    d = i18n.parse_date('4/1/2004')
    assert isinstance(d, datetime.date)
    assert (d.year, d.month, d.day) == (2004, 1, 4)


def test_parse_date_en():
    i18n.set_locale(i18n.Locale('en', 'US'))

    d = i18n.parse_date('4/1/04')
    assert isinstance(d, datetime.date)
    assert (d.year, d.month, d.day) == (2004, 4, 1)

    d = i18n.parse_date('4/1/2004')
    assert isinstance(d, datetime.date)
    assert (d.year, d.month, d.day) == (2004, 4, 1)
