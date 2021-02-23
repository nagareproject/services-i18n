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

from nagare.services import plugin
from nagare.i18n import set_locale, Locale, NegotiatedLocale


class I18NLocale(plugin.Plugin):
    LOAD_PRIORITY = 80
    CONFIG_SPEC = dict(plugin.Plugin.CONFIG_SPEC, dirname='string(default=None)')
    LOCALE_FACTORY = Locale

    def __init__(self, name, dist, dirname=None, i18n_service=None, services_service=None, **config):
        services_service(super(I18NLocale, self).__init__, name, dist, dirname=dirname, **config)

        self.config = config
        self.config['dirname'] = dirname or i18n_service.output_directory

    @staticmethod
    def set_locale(locale):
        set_locale(locale)

    def create_locale(self, **config):
        return self.LOCALE_FACTORY(**dict(self.config, **config))

    def handle_request(self, chain, **params):
        locale = self.get_locale(**params)
        self.set_locale(locale)

        return chain.next(**params)

    def get_locale(self, **params):
        raise NotImplementedError()

# -----------------------------------------------------------------------------


class I18NPredefinedLocale(I18NLocale):
    CONFIG_SPEC = dict(
        I18NLocale.CONFIG_SPEC,
        language='string',
        territory='string(default=None)',
        script='string(default=None)',
        variant='string(default=None)',
        dirname='string(default=None)',
        domain='string(default=None)',
        timezone='string(default=None)',
        default_timezone='string(default=None)'
    )

    def __init__(self, name, dist, services_service, **config):
        services_service(super(I18NPredefinedLocale, self).__init__, name, dist, **config)

        self.locale = self.create_locale()

    def get_locale(self, **params):
        return self.locale

# -----------------------------------------------------------------------------


class I18NNegociatedLocale(I18NLocale):
    CONFIG_SPEC = dict(
        I18NLocale.CONFIG_SPEC,
        locales='string_list',
        default_locale='string',
        dirname='string(default=None)',
        domain='string(default=None)',
        timezone='string(default=None)',
        default_timezone='string(default=None)'
    )
    LOCALE_FACTORY = NegotiatedLocale

    def __init__(
        self,
        name, dist,
        locales=(), default_locale='',
        services_service=None,
        **config
    ):
        locales = [(locale + '_').split('_')[:2] for locale in locales]
        default_locale = (default_locale + '_').split('_')[:2]

        services_service(
            super(I18NNegociatedLocale, self).__init__,
            name, dist,
            locales=locales, default_locale=tuple(default_locale),
            **config
        )

    def get_locale(self, request, **params):
        return super(I18NNegociatedLocale, self).create_locale(request=request)
