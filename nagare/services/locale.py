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

from nagare.services import plugin
from nagare.server import reference
from nagare.i18n import set_locale, Locale, NegotiatedLocale


class I18NBaseLocale(plugin.Plugin):
    LOAD_PRIORITY = 80
    LOCALE_FACTORY = Locale

    def __init__(self, name, dist, dirname=None, i18n_service=None, **config):
        super(I18NBaseLocale, self).__init__(name, dist)

        self.dirname = dirname or i18n_service.output_directory
        self.config = config

    def create_locale(self, **config):
        return self.LOCALE_FACTORY(dirname=self.dirname, **dict(self.config, **config))

    def get_locale(self, **params):
        return None

    @staticmethod
    def set_locale(locale):
        set_locale(locale)

    def handle_request(self, chain, **params):
        locale = self.get_locale(**params)
        self.set_locale(locale)

        return chain.next(**params)

# -----------------------------------------------------------------------------


class I18NPredefinedLocale(I18NBaseLocale):
    CONFIG_SPEC = {
        'language': 'string(default="en")',
        'territory': 'string(default=None)',
        'script': 'string(default=None)',
        'variant': 'string(default=None)',
        'dirname': 'string(default=None)',
        'domain': 'string(default=None)',
        'timezone': 'string(default=None)',
        'default_timezone': 'string(default=None)'
    }

    def __init__(self, name, dist, services_service, **config):
        services_service(super(I18NPredefinedLocale, self).__init__, name, dist, **config)

        self.locale = self.create_locale()

    def get_locale(self, **params):
        return self.locale

# -----------------------------------------------------------------------------


class I18NNegociatedLocale(I18NBaseLocale):
    CONFIG_SPEC = {
        'languages': 'string_list(default=list())',
        'dirname': 'string(default=None)',
        'domain': 'string(default=None)',
        'timezone': 'string(default=None)',
        'default_timezone': 'string(default=None)'
    }
    LOCALE_FACTORY = NegotiatedLocale

    def __init__(self, name, dist, languages=(), services_service=None, **config):
        locales = [(language + '_').split('_')[:2] for language in languages]
        default_locale = self.locales[0] if self.locales else (None, None)

        services_service(
            super(I18NNegociatedLocale, self).__init__,
            name, dist,
            locales=locales, default_locale=default_locale,
            **config
        )

    def get_locale(self, request, **params):
        return super(I18NNegociatedLocale, self).create_locale(request=request)

# -----------------------------------------------------------------------------


class I18NLocale(I18NPredefinedLocale):
    CONFIG_SPEC = {
        'get_locale': 'string(default=None)',
        'dirname': 'string(default=None)',
    }

    def __init__(self, name, dist, get_locale=None, dirname=None, services_service=None):
        services_service(super(I18NLocale, self).__init__, name, dist, dirname=dirname, language='en')

        if get_locale:
            self.get_locale = reference.load_object(get_locale)[0].__get__(self, self.__class__)
