# Encoding: utf-8

# --
# Copyright (c) 2008-2022 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import os

from nagare import local, i18n


def setup_module(module):
    local.request = local.Process()
    locale = i18n.Locale('fr', 'FR', dirname=os.path.join(os.path.dirname(__file__), 'locale'))
    i18n.set_locale(locale)


def test_gettext():
    s = i18n.gettext('hello')
    assert isinstance(s, str)
    assert s == 'bonjour'


def test_gettext_params():
    s = i18n.gettext('Holidays', year=2010)
    assert isinstance(s, str)
    assert s == 'Vacances 2010'


def test_gettext_unknown():
    s = i18n.gettext('unknown')
    assert isinstance(s, str)
    assert s == 'unknown'


def test_ugettext():
    s = i18n.ugettext('hello')
    assert isinstance(s, type(u''))
    assert s == u'bonjour'


def test_ugettext_params():
    s = i18n.ugettext('Holidays', year=2010)
    assert isinstance(s, type(u''))
    assert s == u'Vacances 2010'


def test_ugettext_unknown():
    s = i18n.ugettext('unknown')
    assert isinstance(s, type(u''))
    assert s == u'unknown'


def test__():
    s = i18n._('hello')
    assert isinstance(s, type(u''))
    assert s == u'bonjour'


def test_ngettext_singular():
    s = i18n.ngettext('horse', 'horses', 1)
    assert isinstance(s, str)
    assert s == 'cheval'


def test_ngettext_plural():
    s = i18n.ngettext('horse', 'horses', 3)
    assert isinstance(s, str)
    assert s == 'chevaux'


def test_ngettext_singular_unknown():
    s = i18n.ngettext('unknown1', 'unknown2', 1)
    assert isinstance(s, str)
    assert s == 'unknown1'


def test_ngettext_plural_unknown():
    s = i18n.ngettext('unknown1', 'unknown2', 3)
    assert isinstance(s, str)
    assert s == 'unknown2'


def test_ungettext_singular():
    s = i18n.ungettext('horse', 'horses', 1)
    assert isinstance(s, type(u''))
    assert s == u'cheval'


def test_ungettext_plural():
    s = i18n.ungettext('horse', 'horses', 3)
    assert isinstance(s, type(u''))
    assert s == u'chevaux'


def test_ungettext_singular_unknown():
    s = i18n.ungettext('unknown1', 'unknown2', 1)
    assert isinstance(s, type(u''))
    assert s == u'unknown1'


def test_ungettext_plural_unknown():
    s = i18n.ungettext('unknown1', 'unknown2', 3)
    assert isinstance(s, type(u''))
    assert s == u'unknown2'


def test_N_singular():
    s = i18n._N('horse', 'horses', 1)
    assert isinstance(s, type(u''))
    assert s == u'cheval'


def test_N_plural():
    s = i18n._N('horse', 'horses', 3)
    assert isinstance(s, type(u''))
    assert s == u'chevaux'


def test_lazy_gettext():
    s = i18n.lazy_gettext('hello')
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str)
    assert s == 'bonjour'


def test_lazy_gettext_params():
    s = i18n.lazy_gettext('Holidays', year=2010)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str)
    assert s == 'Vacances 2010'


def test_lazy_ugettext():
    s = i18n.lazy_ugettext('hello')
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, type(u''))
    assert s == u'bonjour'


def test_lazy_ugettext_params():
    s = i18n.lazy_ugettext('Holidays', year=2010)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, type(u''))
    assert s == u'Vacances 2010'


def test_L_ugettext():
    s = i18n._L('hello')
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, type(u''))
    assert s == u'bonjour'


def test_lazy_ngettext_singular():
    s = i18n.lazy_ngettext('horse', 'horses', 1)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str)
    assert s == 'cheval'


def test_lazy_ngettext_plural():
    s = i18n.lazy_ngettext('horse', 'horses', 3)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str)
    assert s == 'chevaux'


def test_lazy_ungettext_singular():
    s = i18n.lazy_ungettext('horse', 'horses', 1)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, type(u''))
    assert s == 'cheval'


def test_lazy_ungettext_plural():
    s = i18n.lazy_ungettext('horse', 'horses', 3)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, type(u''))
    assert s == 'chevaux'


def test_LN_ungettext_singular():
    s = i18n._LN('horse', 'horses', 1)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, type(u''))
    assert s == 'cheval'


def test_LN_ungettext_plural():
    s = i18n._LN('horse', 'horses', 3)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, type(u''))
    assert s == 'chevaux'
