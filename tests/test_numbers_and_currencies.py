# --
# Copyright (c) 2014-2025 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import datetime
from decimal import Decimal

import pytest
from babel.numbers import NumberFormatError

from nagare import i18n, local
from nagare.i18n import Locale, set_locale


def setup_module(module):
    local.request = local.Process()


def test_format_number():
    set_locale(Locale('en', 'US'))
    assert i18n.format_number(1099) == '1,099'

    set_locale(Locale('de', 'DE'))
    assert i18n.format_number(1099) == '1.099'


def test_format_decimal():
    set_locale(Locale('en', 'US'))
    assert i18n.format_decimal(1.2345) == '1.234'
    assert i18n.format_decimal(1.2346) == '1.235'
    assert i18n.format_decimal(1.2346, decimal_quantization=False) == '1.2346'
    assert i18n.format_decimal(-1.2346) == '-1.235'
    set_locale(Locale('sv', 'SE'))
    assert i18n.format_decimal(1.2345) == '1,234'

    set_locale(Locale('de'))
    assert i18n.format_decimal(12345) == '12.345'


def test_format_currency():
    set_locale(Locale('en', 'US'))
    assert i18n.format_currency(1099.98, 'USD') == '$1,099.98'

    set_locale(Locale('es', 'CO'))
    assert i18n.format_currency(1099.98, 'USD') == 'US$1.099,98'

    set_locale(Locale('de', 'DE'))
    assert i18n.format_currency(1099.98, 'EUR') == '1.099,98\xa0\u20ac'

    set_locale(Locale('en', 'US'))
    assert i18n.format_currency(1099.98, 'EUR', '\xa4\xa4 #,##0.00') == 'EUR 1,099.98'

    set_locale(Locale('en', 'US'))
    assert i18n.format_currency(1099.98, 'JPY', currency_digits=False) == '\xa51,099.98'

    set_locale(Locale('es', 'ES'))
    assert i18n.format_currency(1099.98, 'COP', '#,##0.00', currency_digits=False) == '1.099,98'

    set_locale(Locale('en', 'US'))
    assert i18n.format_currency(1099.9876, 'USD') == '$1,099.99'
    assert i18n.format_currency(1099.9876, 'USD', decimal_quantization=False) == '$1,099.9876'


def test_get_exponential_symbol():
    set_locale(Locale('en', 'US'))
    assert i18n.get_exponential_symbol() == 'E'


def test_get_group_symbol():
    set_locale(Locale('en', 'US'))
    assert i18n.get_group_symbol() == ','


def test_format_percent():
    set_locale(Locale('en', 'US'))
    assert i18n.format_percent(0.34) == '34%'
    assert i18n.format_percent(25.1234) == '2,512%'

    set_locale(Locale('sv', 'SE'))
    assert i18n.format_percent(25.1234) == '2\xa0512\xa0%'

    set_locale(Locale('en', 'US'))
    assert i18n.format_percent(25.1234, '#,##0\u2030') == '25,123\u2030'

    set_locale(Locale('en', 'US'))
    assert i18n.format_percent(23.9876) == '2,399%'
    assert i18n.format_percent(23.9876, decimal_quantization=False) == '2,398.76%'


def test_format_scientific():
    set_locale(Locale('en', 'US'))
    assert i18n.format_scientific(10000) == '1E4'
    assert i18n.format_scientific(1234567, '##0E00') == '1.234567E06'


def test_parse_number():
    set_locale(Locale('en', 'US'))
    assert i18n.parse_number('1,099') == 1099

    set_locale(Locale('de', 'DE'))
    assert i18n.parse_number('1.099') == 1099

    set_locale(Locale('de', 'DE'))
    with pytest.raises(NumberFormatError):
        i18n.parse_number('1.099,98')


def test_parse_decimal():
    set_locale(Locale('en', 'US'))
    assert i18n.parse_decimal('1,099.98') == Decimal('1099.98')

    set_locale(Locale('de', 'DE'))
    assert i18n.parse_decimal('1.099,98') == Decimal('1099.98')

    set_locale(Locale('de', 'DE'))
    with pytest.raises(NumberFormatError):
        i18n.parse_decimal('2,109,998')


def test_get_currency_name():
    set_locale(Locale('en', 'US'))
    assert i18n.get_currency_name('USD') == 'US Dollar'


def test_get_currency_symbol():
    set_locale(Locale('en', 'US'))
    assert i18n.get_currency_symbol('USD') == '$'


def test_get_decimal_symbol():
    set_locale(Locale('en', 'US'))
    assert i18n.get_decimal_symbol() == '.'


def test_get_plus_sign_symbol():
    set_locale(Locale('en', 'US'))
    assert i18n.get_plus_sign_symbol() == '+'


def test_get_minus_sign_symbol():
    set_locale(Locale('en', 'US'))
    assert i18n.get_minus_sign_symbol() == '-'


def test_get_territory_currencies():
    set_locale(Locale(territory='AT'))
    assert i18n.get_territory_currencies(datetime.date(1995, 1, 1), datetime.date(2011, 1, 1)) == ['ATS', 'EUR']
    assert i18n.get_territory_currencies(datetime.date(1995, 1, 1)) == ['ATS']
    assert i18n.get_territory_currencies(datetime.date(2011, 1, 1)) == ['EUR']

    set_locale(Locale('en', 'US'))
    assert i18n.get_territory_currencies() == ['USD']
    assert i18n.get_territory_currencies(tender=False, non_tender=True, start_date=datetime.date(2014, 1, 1)) == [
        'USN',
        'USS',
    ]
