# Encoding: utf-8

# --
# Copyright (c) 2008-2019 Net-ng.
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


def test_format_list():
    set_locale(Locale('en'))
    assert i18n.format_list(['apples', 'oranges', 'pears']) == 'apples, oranges, and pears'

    set_locale(Locale('zh'))
    assert i18n.format_list(['apples', 'oranges', 'pears']) == u'apples\u3001oranges\u548cpears'

    set_locale(Locale('fi'))
    assert i18n.format_list(['omena', 'peruna', 'aplari'], style='or') == 'omena, peruna tai aplari'
