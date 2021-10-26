# --
# Copyright (c) 2008-2021 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import os
import logging

from nagare.admin import command
from babel import Locale, localedata
from babel.messages.frontend import CommandLineInterface


class Commands(command.Commands):
    DESC = 'i18n catalogs management subcommands'


class Locales(command.Command):
    DESC = 'display all the locales code'
    WITH_CONFIG_FILENAME = False

    def _create_services(self, *args, **kw):
        return self.SERVICES_FACTORY()

    @staticmethod
    def run():
        identifiers = localedata.locale_identifiers()
        padding = len(max(identifiers, key=len))

        for identifier in sorted(identifiers):
            print(identifier.ljust(padding), Locale.parse(identifier).english_name)


class Command(command.Command):

    def set_arguments(self, parser, **defaults):
        parser.add_argument(
            '-v', '--verbose',
            action='store_const', const=logging.DEBUG, dest='loglevel',
            help='print as much as possible'
        )
        parser.add_argument(
            '-q', '--quiet',
            action='store_const', const=logging.ERROR, dest='loglevel',
            help='print as little as possible'
        )
        super(Command, self).set_arguments(parser)

    @classmethod
    def create_command(cls, **defaults):
        command_name = cls.__name__.lower()
        command = CommandLineInterface.command_classes[command_name]()
        command.__dict__.update(defaults)

        return command_name, command

    @staticmethod
    def run_command(command, **config):
        command.initialize_options()
        command.__dict__.update(config)
        command.finalize_options()

        return command.run()

    def run(self, i18n_service, **params):
        command_name, command = self.create_command()
        command.log = i18n_service.logger

        config = dict(i18n_service.plugin_config[command_name], **params)
        return self.run_command(command, **config)

    @property
    def DESC(self):
        _, command = self.create_command()
        return command.description


class Extract(Command):

    @classmethod
    def create_command(cls, **defaults):
        return super(Extract, cls).create_command(
            input_dirs='$root',
            output_file='$data/locale/messages.pot'
        )

    def run_command(self, command, output_file, keywords, **config):
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        keywords = keywords or (
            '_ , _N:1,2 , _L , _LN:1,2 , gettext , ugettext , ngettext:1,2 , '
            'ungettext:1,2 , lazy_gettext , lazy_ugettext , lazy_ngettext:1,2 , lazy_ungettext:1,2'
        )

        return super(Extract, self).run_command(command, output_file=output_file, keywords=keywords, **config)


class Init(Command):

    def set_arguments(self, parser):
        parser.add_argument('-d', '--domain', dest='forced_domain')
        parser.add_argument('locale')
        super(Init, self).set_arguments(parser)

    @classmethod
    def create_command(cls, **defaults):
        return super(Init, cls).create_command(input_file='${/i18n/extract/output_file}', output_dir='')

    def run_command(self, command, forced_domain, input_file, output_dir, domain, **config):
        output_dir = output_dir or os.path.dirname(input_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        return super(Init, self).run_command(
            command,
            domain=forced_domain or domain,
            input_file=input_file,
            output_dir=output_dir,
            **config
        )


class Update(Command):

    def set_arguments(self, parser):
        parser.add_argument('-d', '--domain', dest='forced_domain')
        parser.add_argument('-l', '--locale')
        super(Update, self).set_arguments(parser)

    @classmethod
    def create_command(cls, **defaults):
        return super(Update, cls).create_command(
            input_file='${/i18n/extract/output_file}',
            domain='${/i18n/init/domain}',
            output_dir=''
        )

    def run_command(self, command, forced_domain, input_file, output_dir, domain, **config):
        output_dir = output_dir or os.path.dirname(input_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        return super(Update, self).run_command(
            command,
            domain=forced_domain or domain,
            input_file=input_file,
            output_dir=output_dir,
            **config
        )


class Compile(Command):

    def set_arguments(self, parser):
        parser.add_argument('-d', '--domain', dest='forced_domain')
        parser.add_argument('-l', '--locale')
        super(Compile, self).set_arguments(parser)

    @classmethod
    def create_command(cls, **defaults):
        return super(Compile, cls).create_command(
            input_file='${/i18n/extract/output_file}',
            directory='${/i18n/init/output_dir}',
            domain='${/i18n/init/domain}'
        )

    def run_command(self, command, forced_domain, input_file, directory, domain, **config):
        directory = directory or os.path.dirname(input_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        return super(Compile, self).run_command(
            command,
            domain=forced_domain or domain,
            directory=directory,
            **config
        )
