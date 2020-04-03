# Encoding: utf-8

# --
# Copyright (c) 2008-2020 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

from nagare import local

from nagare import i18n
from nagare.i18n import Locale, set_locale


def setup_module(module):
    local.request = local.Process()


def test_get_official_languages():
    set_locale(Locale('en', 'US'))
    assert i18n.get_official_languages() == ()
    assert i18n.get_official_languages(de_facto=True) == ('en',)
    assert i18n.get_official_languages(regional=True) == ('es', 'haw')

    set_locale(Locale('fr', 'FR'))
    assert i18n.get_official_languages() == ('fr',)
    assert i18n.get_official_languages(de_facto=True) == ('fr',)
    assert i18n.get_official_languages(regional=True) == ('fr',)


def test_get_territory_language_info():
    set_locale(Locale('en', 'US'))
    assert {'en', 'es', 'fr'} <= set(i18n.get_territory_language_info())

    set_locale(Locale('fr', 'FR'))
    assert {'en', 'es', 'fr'} <= set(i18n.get_territory_language_info())
