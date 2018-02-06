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


class I18NPredefinedLocale(plugin.Plugin):
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

    def __init__(
            self,
            name, dist,
            language='en', territory=None, script=None, variant=None,
            dirname=None, domain=None, timezone=None, default_timezone=None,
            i18n_service=None
    ):
        super(I18NPredefinedLocale, self).__init__(name, dist)

        dirname = dirname or i18n_service.output_directory
        self.locale = Locale(language, territory, script, variant, dirname, domain, timezone, default_timezone)

    def handle_request(self, chain, **params):
        set_locale(self.locale)

        return chain.next(**params)

# -----------------------------------------------------------------------------


class I18NNegociatedLocale(plugin.Plugin):
    CONFIG_SPEC = {'languages': 'string_list(default=list())'}

    def __init__(self, name, dist, languages=()):
        super(I18NNegociatedLocale, self).__init__(name, dist)

        self.languages = [(language + '_').split('_')[:2] for language in languages]

    def handle_request(self, chain, request, **params):
        locale = NegotiatedLocale(
            request,
            self.languages,
            default_locale=self.languages[0] if self.languages else (None, None)
        )

        set_locale(locale)

        return chain.next(request=request, **params)

# -----------------------------------------------------------------------------


class I18NLocale(plugin.Plugin):
    CONFIG_SPEC = {
        'get_locale': 'string(default=None)',
        'dirname': 'string(default=None)'
    }

    def __init__(self, name, dist, get_locale=None, dirname=None, i18n_service=None, **config):
        super(I18NLocale, self).__init__(name, dist)

        self.get_locale = get_locale and reference.load_object(get_locale)[0]
        self.dirname = dirname or i18n_service.output_directory
        self.config = config

    def handle_request(self, chain, **params):
        if self.get_locale is not None:
            locale = self.get_locale(dirname=self.dirname, **dict(params, **self.config))
            set_locale(locale)

        return chain.next(**params)
