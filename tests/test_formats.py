# Encoding: utf-8

# --
# Copyright (c) 2008-2018 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import decimal

from nagare import local, i18n


def setup_module(module):
    local.request = local.Process()
    i18n.set_locale(i18n.Locale('fr', 'FR'))


def test_get_currency_name():
    assert i18n.get_currency_name('USD') == u'dollar des États-Unis'


def test_get_currency_symbol():
    assert i18n.get_currency_symbol('USD') == '$US'


def test_get_decimal_symbol():
    assert i18n.get_decimal_symbol() == ','


def test_get_plus_sign_symbol():
    assert i18n.get_plus_sign_symbol() == '+'


def test_get_minus_sign_symbol():
    assert i18n.get_minus_sign_symbol() == '-'


def test_get_exponential_symbol():
    assert i18n.get_exponential_symbol() == 'E'


def test_get_group_symbol():
    assert i18n.get_group_symbol() == u'\N{NO-BREAK SPACE}'


def test_format_number():
    assert i18n.format_number(1099) == u'1\N{NO-BREAK SPACE}099'


def test_format_decimal():
    assert i18n.format_decimal(1236.1236) == u'1\N{NO-BREAK SPACE}236,124'


def test_format_currency():
    assert i18n.format_currency(1236.126, 'EUR') == u'1\N{NO-BREAK SPACE}236,13\N{NO-BREAK SPACE}\N{EURO SIGN}'


def test_format_percent():
    assert i18n.format_percent(24.1234) == u'2\N{NO-BREAK SPACE}412\N{NO-BREAK SPACE}%'


def test_format_scientific():
    assert i18n.format_scientific(10000) == '1E4'


def test_parse_number():
    assert i18n.parse_number(u'1\N{NO-BREAK SPACE}099') == 1099


def test_parse_decimal():
    assert i18n.parse_decimal(u'1\N{NO-BREAK SPACE}099,1234') == decimal.Decimal('1099.1234')