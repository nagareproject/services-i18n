# --
# Copyright (c) 2008-2018 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""Internationalization service
"""

from babel import support
from nagare import local


def get_locale():
    return getattr(local.request, 'locale')


def set_locale(locale):
    local.request.locale = locale


class LazyProxy(support.LazyProxy):
    """Picklable ``babel.support.LazyProxy`` objects
    """
    @property
    def value(self):
        """Always evaluate, without any cache
        """
        return self._func(*self._args, **self._kwargs)

    def __getstate__(self):
        return self._func, self._args, self._kwargs

    def __setstate__(self, attrs):
        self.__init__(attrs[0], *attrs[1], **attrs[2])

# Service API
# -----------


def gettext(msg, domain=None, **kw):
    return get_locale().gettext(msg, domain, **kw)


def ugettext(msg, domain=None, **kw):
    return get_locale().ugettext(msg, domain, **kw)
_ = ugettext  # noqa: E305


def ngettext(singular, plural, n, domain=None, **kw):
    return get_locale().ngettext(singular, plural, n, domain, **kw)


def ungettext(singular, plural, n, domain=None, **kw):
    return get_locale().ungettext(singular, plural, n, domain, **kw)
_N = ungettext  # noqa: E305


def lazy_gettext(msg, domain=None, **kw):
    return LazyProxy(gettext, msg, domain, **kw)


def lazy_ugettext(msg, domain=None, **kw):
    return LazyProxy(ugettext, msg, domain, **kw)
_L = lazy_ugettext  # noqa: E305


def lazy_ngettext(singular, plural, n, domain=None, **kw):
    return LazyProxy(ngettext, singular, plural, n, domain, **kw)


def lazy_ungettext(singular, plural, n, domain=None, **kw):
    return LazyProxy(ungettext, singular, plural, n, domain, **kw)
_LN = lazy_ungettext  # noqa: E305


def get_period_names():
    return get_locale().get_period_names()


def get_day_names(width='wide', context='format'):
    return get_locale().get_day_names(width, context)


def get_month_names(width='wide', context='format'):
    return get_locale().get_month_names(width, context)


def get_quarter_names(width='wide', context='format'):
    return get_locale().get_quarter_names(width, context)


def get_era_names(width='wide'):
    return get_locale().get_era_names(width)


def get_date_format(format='medium'):
    return get_locale().get_date_format(format)


def get_datetime_format(format='medium'):
    return get_locale().get_datetime_format(format)


def get_time_format(format='medium'):
    return get_locale().get_time_format(format)


def get_timezone_gmt(dt=None, width='long'):
    return get_locale().get_timezone_gmt(dt, width)


def get_timezone_location(dt_or_timezone=None):
    return get_locale().get_timezone_location(dt_or_timezone)


def get_timezone_name(dt_or_timezone=None, width='long', uncommon=False):
    return get_locale().get_timezone_name(dt_or_timezone, width, uncommon)


def get_currency_name(currency):
    return get_locale().get_currency_name(currency)


def get_currency_symbol(currency):
    return get_locale().get_currency_symbol(currency)


def get_decimal_symbol():
    return get_locale().get_decimal_symbol()


def get_plus_sign_symbol():
    return get_locale().get_plus_sign_symbol()


def get_minus_sign_symbol():
    return get_locale().get_minus_sign_symbol()


def get_exponential_symbol():
    return get_locale().get_exponential_symbol()


def get_group_symbol():
    return get_locale().get_group_symbol()


def format_number(number):
    return get_locale().format_number(number)


def format_decimal(number, format=None):
    return get_locale().format_decimal(number, format)


def format_currency(number, currency, format=None):
    return get_locale().format_currency(number, currency, format)


def format_percent(number, format=None):
    return get_locale().format_percent(number, format)


def format_scientific(number, format=None):
    return get_locale().format_scientific(number, format)


def parse_number(string):
    return get_locale().parse_number(string)


def parse_decimal(string):
    return get_locale().parse_decimal(string)


def to_timezone(dt):
    return get_locale().to_timezone(dt)


def to_utc(dt):
    return get_locale().to_utc(dt)


def format_time(t=None, format='medium'):
    return get_locale().format_time(t, format)


def format_date(d=None, format='medium'):
    return get_locale().format_date(d, format)


def format_datetime(dt=None, format='medium'):
    return get_locale().format_datetime(dt, format)


def parse_time(string):
    return get_locale().parse_time(string)


def parse_date(string):
    return get_locale().parse_date(string)
