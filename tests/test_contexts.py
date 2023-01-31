# Encoding: utf-8

# --
# Copyright (c) 2008-2023 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

from nagare import local, i18n


def setup_module(module):
    local.request = local.Process()


def test_context_manager():
    locale1 = i18n.Locale('fr', 'FR', domain='domain1')
    locale2 = i18n.Locale('fr', 'FR', domain='domain2')

    i18n.set_locale(locale1)
    assert i18n.get_locale().domain == 'domain1'

    with locale2:
        assert i18n.get_locale().domain == 'domain2'
        with locale2:
            assert i18n.get_locale().domain == 'domain2'

    assert i18n.get_locale().domain == 'domain1'
