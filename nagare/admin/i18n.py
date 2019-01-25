# --
# Copyright (c) 2008-2019 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import logging

from nagare.admin import command
from babel import Locale, localedata
from babel.messages.frontend import CommandLineInterface


class Commands(command.Commands):
    DESC = 'i18n catalogs management subcommands'


class Locales(command.Command):
    DESC = 'display all the locales code'
    WITH_CONFIG_FILENAME = WITH_STARTED_SERVICES = False

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

    def run(self, i18n_service, **params):
        command_name, command = self.create_command()
        command.log = i18n_service.logger

        return i18n_service.run(command_name, command, **params)

    @property
    def DESC(self):
        _, command = self.create_command()
        return command.description


class Extract(Command):
    @classmethod
    def create_command(cls, **defaults):
        return super(Extract, cls).create_command(output_file='')


class Init(Command):
    @classmethod
    def create_command(cls, **defaults):
        return super(Init, cls).create_command(
            input_file='${i18n.extract.output_file}',
            output_dir=''
        )

    def set_arguments(self, parser):
        parser.add_argument('locale')
        super(Init, self).set_arguments(parser)


class Update(Command):
    @classmethod
    def create_command(cls, **defaults):
        return super(Update, cls).create_command(
            input_file='${i18n.extract.output_file}',
            domain='${i18n.init.domain}',
            output_dir='${i18n.init.output_dir}'
        )


class Compile(Command):
    @classmethod
    def create_command(cls, **defaults):
        return super(Compile, cls).create_command(
            directory='${i18n.init.output_dir}',
            domain='${i18n.init.domain}'
        )
