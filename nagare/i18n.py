# --
# Copyright (c) 2008-2021 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""Internationalization service
"""

import datetime
from operator import itemgetter

import pytz
from nagare import local
from babel import dates, numbers, languages, lists, support
from babel import core, negotiate_locale, Locale as CoreLocale


def get_locale():
    return getattr(local.request, 'nagare_locale', Locale())


def set_locale(locale):
    local.request.nagare_locale = locale


class LazyProxy(support.LazyProxy):
    """Picklable ``babel.support.LazyProxy`` objects
    """
    def __init__(self, func, *args, **kw):
        """Always evaluate, without any cache
        """
        super(LazyProxy, self).__init__(func, *args, enable_cache=True, **kw)

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


def to_timezone(dt):
    return get_locale().to_timezone(dt)


def to_utc(dt):
    return get_locale().to_utc(dt)


def format_datetime(dt=None, format='medium'):
    return get_locale().format_datetime(dt, format)


def format_date(d=None, format='medium'):
    return get_locale().format_date(d, format)


def format_time(t=None, format='medium'):
    return get_locale().format_time(t, format)


def format_timedelta(delta, granularity='second', threshold=.85, add_direction=False, format='long'):
    return get_locale().format_timedelta(delta, granularity, threshold, add_direction, format)


def format_skeleton(skeleton, datetime=None, fuzzy=True):
    return get_locale().format_skeleton(skeleton, datetime, fuzzy)


def format_interval(start, end, skeleton=None, fuzzy=True):
    return get_locale().format_interval(start, end, skeleton, fuzzy)


def get_timezone(zone=None):
    return dates.get_timezone(zone)


def get_timezone_gmt(datetime=None, width='long', return_z=False):
    return get_locale().get_timezone_gmt(datetime, width, return_z)


def get_timezone_location(return_city=False):
    return get_locale().get_timezone_location(return_city)


def get_timezone_name(dt_or_timezone=None, width='long', uncommon=False, zone_variant=None, return_zone=False):
    return get_locale().get_timezone_name(dt_or_timezone, width, uncommon, zone_variant, return_zone)


def get_period_names(width='wide', context='stand-alone'):
    return get_locale().get_period_names(width, context)


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


def parse_date(string):
    return get_locale().parse_date(string)


def parse_time(string):
    return get_locale().parse_time(string)


def parse_pattern(pattern):
    return dates.parse_pattern(pattern)


def get_official_languages(regional=False, de_facto=False):
    return get_locale().get_official_languages(regional, de_facto)


def get_territory_language_info():
    return get_locale().get_territory_language_info()


def format_list(lst, style='standard'):
    return get_locale().format_list(lst, style)


def format_number(number):
    return get_locale().format_number(number)


def format_decimal(number, format=None, decimal_quantization=True):
    return get_locale().format_decimal(number, format, decimal_quantization)


def format_currency(
    number, currency, format=None, currency_digits=True,
    format_type='standard', decimal_quantization=True
):
    return get_locale().format_currency(number, currency, format, currency_digits, format_type, decimal_quantization)


def format_percent(number, format=None, decimal_quantization=True):
    return get_locale().format_percent(number, format, decimal_quantization)


def format_scientific(number, format=None, decimal_quantization=True):
    return get_locale().format_scientific(number, format, decimal_quantization)


def parse_number(string):
    return get_locale().parse_number(string)


def parse_decimal(string):
    return get_locale().parse_decimal(string)


def get_currency_name(currency, count=None):
    return get_locale().get_currency_name(currency, count)


def get_currency_symbol(currency):
    return get_locale().get_currency_symbol(currency)


def get_decimal_symbol():
    return get_locale().get_decimal_symbol()


def get_exponential_symbol():
    return get_locale().get_exponential_symbol()


def get_group_symbol():
    return get_locale().get_group_symbol()


def get_plus_sign_symbol():
    return get_locale().get_plus_sign_symbol()


def get_minus_sign_symbol():
    return get_locale().get_minus_sign_symbol()


def get_territory_currencies(
        start_date=None, end_date=None,
        tender=True, non_tender=False,
        include_details=False
):
    return get_locale().get_territory_currencies(start_date, end_date, tender, non_tender, include_details)

# -----------------------------------------------------------------------------


# Locale API
# ----------

_translations_cache = {}  # Already loaded translation objects


class DummyTranslation(object):
    """Identity translation
    """
    @staticmethod
    def gettext(msg):
        return msg

    ugettext = _ = lazy_gettext = lazy_ugettext = _L = gettext

    @staticmethod
    def ngettext(singular, plural, n):
        return singular if n == 1 else plural

    ungettext = _N = lazy_ngettext = lazy_ungettext = _LN = ngettext


class Locale(CoreLocale):
    def __init__(
        self,
        language='en', territory=None, script=None, variant=None,
        dirname=None, domain=None,
        timezone=None, default_timezone=None
    ):
        """
        A locale

        In:
          - ``language`` -- the language code (i.e 'en'),
            as described in `ISO 639 <http://ftp.ics.uci.edu/pub/ietf/http/related/iso639.txt>`_
          - ``territory`` -- the territory (country or region) code (i.e 'US'),
            as described in `ISO 3166 <http://userpage.chemie.fu-berlin.de/diverse/doc/ISO_3166.html>`_
          - ``script`` -- the script code,
            as described in `ISO 15924 <http://www.evertype.com/standards/iso15924/>`_
          - ``variant`` -- the variant code (i.e ``Locale('de', 'DE', '1901')``)

          - ``dirname`` -- the directory containing the ``MO`` files
          - ``domain`` -- the messages domain

          - ``timezone`` -- the timezone (timezone object or code)
            (i.e ``pytz.timezone('America/Los_Angeles')`` or ``America/Los_Angeles``)
          - ``default_timezone`` -- default timezone when a ``datetime`` object has
            no associated timezone. If no default timezone is given, the ``timezone``
            value is used
        """
        super(Locale, self).__init__(language, territory, script, variant)

        self.domain = domain
        self.translation_directories = {}
        if dirname is not None:
            self.add_translation_directory(dirname, domain)

        if isinstance(timezone, (str, type(u''))):
            timezone = pytz.timezone(timezone)
        self.tzinfo = timezone

        if default_timezone is None:
            default_timezone = timezone

        if isinstance(default_timezone, (str, type(u''))):
            default_timezone = pytz.timezone(default_timezone)
        self.default_timezone = default_timezone

        self._previous_locales = []
        self.zone_formats['region'] = '%s'

    def add_translation_directory(self, dirname, domain=None):
        """Associate a directory to a translation domain

        In:
          - ``dirname`` -- the directory
          - ``domain`` -- the translation domain
        """
        self.translation_directories[domain] = dirname

    def has_translation_directory(self, domain=None):
        """Test if a domain has an associated directory

        In:
          - ``domain`` -- the translation domain

        Return:
          - bool
        """
        return domain in self.translation_directories

    def get_translation_directory(self, domain=None):
        """Return the directory associated to the domain

        In:
          - ``domain`` -- the translation domain
        """
        return self.translation_directories.get(domain)

    def _get_translation(self, domain=None):
        """Load the translation object, if not already loaded

        In:
          - ``domain`` -- translation domain

        Return:
          - translation object
        """
        if self.language is None:
            return DummyTranslation()

        domain = domain or self.domain
        dirname = self.get_translation_directory(domain) or self.get_translation_directory(None)
        args = (dirname, str(self), domain)

        translation = _translations_cache.get(args)
        if translation is None:
            translation = support.Translations.load(*args)
            _translations_cache[args] = translation

        return translation

    def gettext(self, msg, domain=None, **kw):
        """Return the localized translation of a message

        In:
          - ``msg`` -- message to translate
          - ``domain`` -- translation domain
          - ``kw`` -- optional values to substitute into the translation

        Return:
          - the localized translation, as a 8-bit string encoded with the
            catalog's charset encoding
        """
        msg = self._get_translation(domain).gettext(msg)
        return msg % kw if kw else msg

    def ugettext(self, msg, domain=None, **kw):
        """Return the localized translation of a message

        In:
          - ``msg`` -- message to translate
          - ``domain`` -- translation domain
          - ``kw`` -- optional values to substitute into the translation

        Return:
          - the localized translation, as an unicode string
        """
        msg = self._get_translation(domain).ugettext(msg)
        return msg % kw if kw else msg
    _ = ugettext

    def ngettext(self, singular, plural, n, domain=None, **kw):
        """Return the plural-forms localized translation of a message

        If a translation is found, apply the ``plural`` formula to ``n``, and
        return the resulting translation. If no translation is found, return
        ``singular`` if ``n`` is 1; return ``plural`` otherwise

        In:
          - ``singular`` -- singular form of the message
          - ``plural`` -- plural form of the message
          - ``n`` -- singular or plural form wanted?
          - ``domain`` -- translation domain
          - ``kw`` -- optional values to substitute into the translation

        Return:
          - the localized translation, as a 8-bit string encoded with the
            catalog's charset encoding
        """
        msg = self._get_translation(domain).ngettext(singular, plural, n)
        return msg % kw if kw else msg

    def ungettext(self, singular, plural, n, domain=None, **kw):
        """Return the plural-forms localized translation of a message

        If a translation is found, apply the ``plural`` formula to ``n``, and
        return the resulting translation. If no translation is found, return
        ``singular`` if ``n`` is 1; return ``plural`` otherwise

        In:
          - ``singular`` -- singular form of the message
          - ``plural`` -- plural form of the message
          - ``n`` -- singular or plural form wanted?
          - ``domain`` -- translation domain
          - ``domain`` -- translation domain
          - ``kw`` -- optional values to substitute into the translation

        Return:
          - the localized translation, as an unicode string
        """
        msg = self._get_translation(domain).ungettext(singular, plural, n)
        return msg % kw if kw else msg
    _N = ungettext

    def lazy_gettext(self, msg, domain=None, **kw):
        """Return the lazy localized translation of a message

        In:
          - ``msg`` -- message to translate
          - ``domain`` -- translation domain
          - ``kw`` -- optional values to substitute into the translation

        Return:
          - the lazy localized translation, as a 8-bit string encoded with the
            catalog's charset encoding
        """
        return LazyProxy(self.gettext, msg, domain, **kw)

    def lazy_ugettext(self, msg, domain=None, **kw):
        """Return the lazy localized translation of a message

        In:
          - ``msg`` -- message to translate
          - ``domain`` -- translation domain
          - ``kw`` -- optional values to substitute into the translation

        Return:
          - the lazy localized translation, as an unicode string
        """
        return LazyProxy(self.ugettext, msg, domain, **kw)
    _L = lazy_ugettext

    def lazy_ngettext(self, singular, plural, n, domain=None, **kw):
        """Return the lazy plural-forms localized translation of a message

        If a translation is found, apply the ``plural`` formula to ``n``, and
        return the resulting translation. If no translation is found, return
        ``singular`` if ``n`` is 1; return ``plural`` otherwise

        In:
          - ``singular`` -- singular form of the message
          - ``plural`` -- plural form of the message
          - ``n`` -- singular or plural form wanted?
          - ``domain`` -- translation domain
          - ``kw`` -- optional values to substitute into the translation

        Return:
          - the lazy localized translation, as a 8-bit string encoded with the
            catalog's charset encoding
        """
        return LazyProxy(self.ngettext, singular, plural, n, domain, **kw)

    def lazy_ungettext(self, singular, plural, n, domain=None, **kw):
        """Return the lazy plural-forms localized translation of a message

        If a translation is found, apply the ``plural`` formula to ``n``, and
        return the resulting translation. If no translation is found, return
        ``singular`` if ``n`` is 1; return ``plural`` otherwise

        In:
          - ``singular`` -- singular form of the message
          - ``plural`` -- plural form of the message
          - ``n`` -- singular or plural form wanted?
          - ``domain`` -- translation domain
          - ``kw`` -- optional values to substitute into the translation

        Return:
          - the lazy localized translation, as an unicode string
        """
        return LazyProxy(self.ungettext, singular, plural, n, domain, **kw)
    _LN = lazy_ungettext

    def to_timezone(self, dt):
        """Return a localized datetime object

        In:
          - ``dt`` -- ``datetime`` object

        Return:
          - new localized ``datetime`` object
        """
        if not self.tzinfo:
            return dt

        if not dt.tzinfo:
            dt = (self.default_timezone or pytz.UTC).localize(dt)

        return dt.astimezone(self.tzinfo)

    def to_utc(self, dt):
        """Return a UTC datetime object

        In:
          - ``dt`` -- ``datetime`` object

        Return:
          - new localized to UTC ``datetime`` object
        """
        if not dt.tzinfo:
            dt = (self.default_timezone or pytz.UTC).localize(dt)

        return dt.astimezone(pytz.UTC)

    # Date & time formatting
    # ======================

    def format_datetime(self, dt=None, format='medium'):
        """Return a date formatted according to the given pattern

        In:
          - ``dt`` -- ``datetime`` object; if ``None``, the current date and time is used
          - ``format`` -- 'full', 'long', 'medium', or 'short', or a custom date/time pattern

        Return:
          - The formatted datetime string
        """
        if dt:
            dt = self.to_timezone(dt)
        return dates.format_datetime(dt, format, locale=self, tzinfo=self.tzinfo)

    def format_date(self, d=None, format='medium'):
        """Return a date formatted according to the given pattern

        In:
          - ``d`` -- ``date`` or ``datetime`` object; if ``None``, the current date is used
          - ``format`` -- 'full', 'long', 'medium', 'short' or a custom date/time pattern

        Return:
          - the formatted date string
        """
        return dates.format_date(d, format, self)

    def format_time(self, t=None, format='medium'):
        """Return a time formatted according to the given pattern

        In:
          - ``t`` --  ``time`` or ``datetime`` object; if `None`, the current time in UTC is used
          - ``format`` -- 'full', 'long', 'medium', 'short' or a custom date/time pattern

        Returns:
          - the formatted time string
        """
        if isinstance(t, datetime.time):
            d = datetime.datetime.now()
            t = d.replace(hour=t.hour, minute=t.minute, second=t.second)

        if isinstance(t, datetime.datetime):
            t = self.to_utc(t)

        return dates.format_time(t, format, locale=self, tzinfo=self.tzinfo)

    def format_timedelta(self, delta, granularity='second', threshold=.85, add_direction=False, format='long'):
        """Return a time delta

        In:
          - ``delta`` -- a `timedelta` object or the delta in seconds
          - ``granularity`` -- 'year', 'month', 'week', 'day', 'hour', 'minute' or 'second'
          - ``threshold`` -- factor that determines at which point the presentation switches to the next higher unit
          - ``add_direction`` -- add information about past or future
          - ``format`` -- 'narrow', 'short' or 'long'

        Returns:
          - the formatted time delta
        """
        return dates.format_timedelta(delta, granularity, threshold, add_direction, format, self)

    def format_skeleton(self, skeleton, datetime=None, fuzzy=True):
        """Return a time and/or date formatted according to the given pattern

        In:
          - ``skeleton`` -- the pattern
          - ``datetime`` --a `time` or `datetime` object; if None, the current time in UTC is used
          - ``fuzzy`` -- If the skeleton is not found, allow choosing a skeleton that's close enough to it

        Returns:
          - the formatted time/date
        """
        return dates.format_skeleton(skeleton, datetime, self.tzinfo, fuzzy, self)

    def format_interval(self, start, end, skeleton=None, fuzzy=True):
        """Format an interval between two instants according to the given pattern

        In:
          - ``start`` -- First instant (`datetime`, `date` or `time`)
          - ``end`` -- Second instant (`datetime`, `date` or `time`)
          - ``skeleton`` -- the pattern
          - ``fuzzy`` -- If the skeleton is not found, allow choosing a skeleton that's close enough to it

        Returns:
          - the formatted interval
        """
        if isinstance(start, datetime.datetime):
            start = self.to_utc(start)

        if isinstance(end, datetime.datetime):
            end = self.to_utc(end)

        return dates.format_interval(start, end, skeleton, self.tzinfo, fuzzy, self)

    # Timezone functionality
    # ======================

    def get_timezone_gmt(self, datetime=None, width='long', return_z=False):
        """Format the timezone associated with the given datetime

        In:
          - ``datetime`` -- the `datetime`
          - ``width`` -- 'long', 'short', 'iso8601' or 'iso8601_short'
          - ``return_z`` -- Have indicator 'Z' when local time offset is 0 to be included?

        Returns:
          - the formatted timezone
        """
        return dates.get_timezone_gmt(datetime, width, self, return_z)

    def get_timezone_location(self, dt_or_timezone=None, return_city=False):
        """Return a representation of the given timezone using "location format"

        The result depends on both the local display name of the country and the
        city associated with the time zone

        In:
          - ``dt_or_tzinfo`` -- ``datetime`` or ``tzinfo`` object that determines
            the timezone; if `None`, the current date and time in UTC is assumed
          - ``return_city`` -- Is the city (location) for the time zone to be included?

        Return:
          - the timezone representation
        """
        return dates.get_timezone_location(dt_or_timezone, self, return_city)

    def get_timezone_name(self, dt_or_timezone=None, width='long', uncommon=False, zone_variant=None, return_zone=False):
        """Return the localized display name for the given timezone

        In:
          - ``dt_or_tzinfo`` -- the ``datetime`` or ``tzinfo`` object that determines
            the timezone; if a ``tzinfo`` object is used, the resulting display
            name will be generic, i.e. independent of daylight savings time;
            if ``None``, the current date in UTC is assumed
          - ``width`` -- either 'long' or 'short'
          - ``uncommon`` -- whether even uncommon timezone abbreviations should be used
          - ``zone_variant`` -- defines the zone variation to return
          - ``return_zone`` -- long time zone ID?

        Return:
          - the localized timezone name
        """
        return dates.get_timezone_name(dt_or_timezone, width, uncommon, self, zone_variant, return_zone)

    # Data access
    # ===========

    def get_period_names(self, width='wide', context='stand-alone'):
        """Return the names for day periods (AM/PM)

        In:
          - ``width`` -- 'abbreviated', 'narrow' or 'wide'
          - ``context`` -- 'format' or 'stand-alone'

        Return:
          - the names for day periods (AM/PM)
        """
        return dates.get_period_names(width, context, locale=self)

    def get_day_names(self, width='wide', context='format'):
        """Return the day names for the specified format

        In:
          - ``width`` -- 'wide', 'abbreviated' or 'narrow'
          - ``context`` -- either 'format' or 'stand-alone'

        Return:
          - the day names
        """
        return dates.get_day_names(width, context, self)

    def get_month_names(self, width='wide', context='format'):
        """Return the month names for the specified format

        In:
          - ``width`` -- 'wide', 'abbreviated' or 'narrow'
          - ``context`` -- either 'format' or 'stand-alone'

        Return:
          - the month names
        """
        return dates.get_month_names(width, context, self)

    def get_quarter_names(self, width='wide', context='format'):
        """Return the quarter names for the specified format

        In:
          - ``width`` -- 'wide', 'abbreviated' or 'narrow'
          - ``context`` -- either 'format' or 'stand-alone'

        Return:
          - the quarter names
        """
        return dates.get_quarter_names(width, context, self)

    def get_era_names(self, width='wide'):
        """Return the era names used for the specified format

        In:
          - ``width`` -- 'wide', 'abbreviated' or 'narrow'

        Return:
          - the era names
        """
        return dates.get_era_names(width, self)

    def get_date_format(self, format='medium'):
        """Return the date formatting pattern for the specified format

        In:
          - ``format`` -- 'full', 'long', 'medium' or 'short'

        Return:
          - the date formatting pattern
        """
        return dates.get_date_format(format, self)

    def get_datetime_format(self, format='medium'):
        """Return the datetime formatting pattern for the specified format

        In:
          - ``format`` -- 'full', 'long', 'medium' or 'short'

        Return:
          - the datetime formatting pattern
        """
        return dates.get_datetime_format(format, self)

    def get_time_format(self, format='medium'):
        """Return the time formatting pattern for the specified format

        In:
          - ``format`` -- 'full', 'long', 'medium' or 'short'

        Return:
          - the time formatting pattern
        """
        return dates.get_time_format(format, self)

    # Basic parsing
    # =============

    def parse_date(self, string):
        """Parse a date from a string

        This function uses the date format for the locale as a hint to determine
        the order in which the date fields appear in the string.

        In:
          - ``string`` -- the string containing the date

        Return:
          - a ``datetime.datetime`` object
        """
        return dates.parse_date(string, self)

    def parse_time(self, string):
        """Parse a time from a string

        This function uses the time format for the locale as a hint to determine
        the order in which the time fields appear in the string.

        In:
          - ``string`` -- the string containing the time

        Return:
          - a ``datetime.time`` object
        """
        return dates.parse_time(string, self)

    # Official languages
    # ==================

    def get_official_languages(self, regional=False, de_facto=False):
        """Get the official language(s) for the given territory

        In:
          - ``regional`` -- include the regionally official languages
          - ``de_facto`` -- include the "de facto" official languages

        Return:
          - the languages
        """
        return languages.get_official_languages(self.territory, regional, de_facto)

    def get_territory_language_info(self):
        """Get a dictionary of language information for a territory

        Return:
          - the languages
        """
        return languages.get_territory_language_info(self.territory)

    # List formatting
    # ===============

    def format_list(self, lst, style='standard'):
        """Format the items in lst as a list.

        In:
          - `lst` -- the items
          - `style` -- 'standard-short', 'or', 'or-short', 'unit', 'unit-short' or
            'unit-narrow'

        Return:
          - the formatted list
        """
        return lists.format_list(lst, style, self)

    # Number formatting
    # =================

    def format_number(self, number):
        """Return the given number formatted
        """
        return numbers.format_number(number, self)

    def format_decimal(self, number, format=None, decimal_quantization=True):
        """Return the given decimal number formatted
        """
        return numbers.format_decimal(number, format, self, decimal_quantization)

    def format_currency(
            self,
            number, currency, format=None,
            currency_digits=True, format_type='standard', decimal_quantization=True
    ):
        """Return formatted currency value
        """
        return numbers.format_currency(number, currency, format, self, currency_digits, format_type, decimal_quantization)

    def format_percent(self, number, format=None, decimal_quantization=True):
        """Return formatted percent value
        """
        return numbers.format_percent(number, format, self, decimal_quantization)

    def format_scientific(self, number, format=None, decimal_quantization=True):
        """Return value formatted in scientific notation
        """
        return numbers.format_scientific(number, format, self, decimal_quantization)

    # Number parsing
    # ==============

    def parse_number(self, string):
        """Parse localized number string into a long integer
        """
        return numbers.parse_number(string, self)

    def parse_decimal(self, string):
        """Parse localized decimal string into a float
        """
        return numbers.parse_decimal(string, self)

    # Data access
    # ===========

    def get_currency_name(self, currency, count=None):
        """Return the name used for the specified currency

        In:
          - ``currency`` -- the currency code
          - ``count`` -- If provided the currency name will be pluealized to that number

        Return:
          - the currency name
        """
        return numbers.get_currency_name(currency, count, self)

    def get_currency_symbol(self, currency):
        """Return the symbol used for the specified currency

        In:
          - ``currency`` -- the currency code

        Return:
          - the currency symbol
        """
        return numbers.get_currency_symbol(currency, self)

    def get_decimal_symbol(self):
        """Return the symbol used to separate decimal fractions
        """
        return numbers.get_decimal_symbol(self)

    def get_exponential_symbol(self):
        """Return the symbol used to separate mantissa and exponent
        """
        return numbers.get_exponential_symbol(self)

    def get_group_symbol(self):
        """Return the symbol used to separate groups of thousands
        """
        return numbers.get_group_symbol(self)

    def get_plus_sign_symbol(self):
        """Return the plus sign symbol
        """
        return numbers.get_plus_sign_symbol(self)

    def get_minus_sign_symbol(self):
        """Return the plus sign symbol
        """
        return numbers.get_minus_sign_symbol(self)

    def get_territory_currencies(
            self,
            start_date=None, end_date=None,
            tender=True, non_tender=False,
            include_details=False
    ):
        """Returns the list of currencies for the given territory that are valid for the given date range

        In:
          - ``start_date`` -- the start date. If not given today is assumed
          - ``end_date`` -- the end date. If not given the start date is assumed
          - ``tender`` -- controls whether tender currencies should be included
          - ``non_tender`` -- controls whether non-tender currencies should be included
          - ``include_detail`` -- the return value will be a dictionnary

        Return:
          - the currencies
        """
        return numbers.get_territory_currencies(self.territory, start_date, end_date, tender, non_tender, include_details)

    def __enter__(self):
        """Push this locale to the stack
        """
        previous_locale = get_locale()

        if not self.translation_directories:
            self.translation_directories.update(previous_locale.translation_directories)

        self._previous_locales.append(previous_locale)
        set_locale(self)

    def __exit__(self, *args, **kw):
        """Pop this locale from the stack
        """
        set_locale(self._previous_locales.pop())

# -----------------------------------------------------------------------------


class NegotiatedLocale(Locale):
    def __init__(
        self,
        request,
        locales, default_locale=(None, None),
        dirname=None, domain=None,
        timezone=None, default_timezone=None
    ):
        """
        A locale with negotiated language and territory

        In:
          - ``request`` -- the HTTP request object
          - ``locales`` -- tuples of (language, territory) accepted by the application
            (i.e ``[('fr', 'FR'), ('de', 'DE'), ('en',)]``)
          - ``default_locale`` -- tuple of (language, territory) to use if the
            negociation failed

          - ``dirname`` -- the directory containing the ``MO`` files
          - ``domain`` -- the messages domain

          - ``timezone`` -- the timezone (timezone object or code)
            (i.e ``pytz.timezone('America/Los_Angeles')`` or ``America/Los_Angeles``)
          - ``default_timezone`` -- default timezone when a ``datetime`` object has
            no associated timezone. If no default timezone is given, the ``timezone``
            value is used
        """
        locale = negotiate_locale(
            map(itemgetter(0), sorted(request.accept_language.parsed or (), key=itemgetter(1), reverse=True)),
            ['-'.join(locale).rstrip('-') for locale in locales],
            '-'
        )

        if not locale:
            language, territory = (default_locale + (None,))[:2]
        else:
            locale = core.LOCALE_ALIASES.get(locale, locale).replace('_', '-')

            if '-' not in locale:
                language = locale
                territory = None
            else:
                language, territory = locale.split('-')
                territory = territory.upper()

        super(NegotiatedLocale, self).__init__(
            language, territory,
            dirname=dirname, domain=domain,
            timezone=timezone, default_timezone=default_timezone
        )
