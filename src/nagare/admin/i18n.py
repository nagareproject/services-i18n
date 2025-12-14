# --
# Copyright (c) 2014-2025 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import os
import types
from tempfile import NamedTemporaryFile

from babel import Locale, localedata
from babel.messages.frontend import CommandLineInterface

from nagare.admin import command
from nagare.server.reference import load_object, is_reference


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
    @classmethod
    def create_command(cls, **defaults):
        command_name = cls.__name__.lower()
        command = CommandLineInterface.command_classes[command_name]()
        command.__dict__.update(defaults)

        return command_name, command

    def create_logger(self, command, i18n_service, **config):
        logger = i18n_service.logger
        if isinstance(logger.info, types.MethodType):
            self.log_info = logger.info

        command.log = logger
        return logger

    def run_command(self, command, services_service, **config):
        services_service(self.create_logger, command, **config)

        command.initialize_options()
        command.__dict__.update(config)
        command.finalize_options()

        return command.run()

    def run(self, i18n_service, services_service, **params):
        command_name, command = self.create_command()

        config = i18n_service.plugin_config[command_name]
        configs = [value for value in config.values() if isinstance(value, dict)]
        config = {name: value for name, value in config.items() if not isinstance(value, dict)}

        for config in [config] + configs:
            config.update(params)
            r = services_service(self.run_command, command, **dict(config, **params))
            if r:
                break

        return r

    @property
    def DESC(self):
        _, command = self.create_command()
        return command.description


class Extract(Command):
    @classmethod
    def create_command(cls, **defaults):
        return super().create_command(
            project='$app_name', version='$app_version', input_dirs='$root', output_file='$data/locale/messages.pot'
        )

    def create_logger(self, command, i18n_service, _output_file, **config):
        logger = super().create_logger(command, i18n_service, **config)
        logger.info = lambda msg, *args: self.log_info(
            msg, *((_output_file,) if msg == 'writing PO template file to %s' else args)
        )

    def run_command(
        self, command, _root, input_dirs, output_file, keywords, relative_location, services_service, **config
    ):
        input_dirs = [load_object(d)[1] if is_reference(d) else d.strip() for d in input_dirs]

        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        keywords = keywords or (
            '_ , _N:1,2 , _L , _LN:1,2 , gettext , ugettext , ngettext:1,2 , '
            'ungettext:1,2 , lazy_gettext , lazy_ugettext , lazy_ngettext:1,2 , lazy_ungettext:1,2'
        )

        with NamedTemporaryFile('rb') as temp:
            r = services_service(
                super().run_command,
                command,
                input_dirs=input_dirs,
                output_file=temp.name,
                keywords=keywords,
                _output_file=output_file,
                **config,
            )

            prefix = b'#: ' + _root.encode('utf8')
            root_len = len(_root)

            with open(output_file, 'wb') as outfile:
                for line in temp:
                    if relative_location and line.startswith(prefix):
                        line = b'#: ' + line[root_len + 4 :]

                    outfile.write(line)

        return r


class Init(Command):
    def set_arguments(self, parser):
        parser.add_argument('locale').completer = lambda **kw: localedata.locale_identifiers()
        super().set_arguments(parser)

    @classmethod
    def create_command(cls, **defaults):
        return super().create_command(input_file='${/i18n/extract/output_file}', output_dir='')

    def run_command(self, command, input_file, output_dir, services_service, **config):
        output_dir = output_dir or os.path.dirname(input_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        return services_service(super().run_command, command, input_file=input_file, output_dir=output_dir, **config)


class Update(Command):
    def set_arguments(self, parser):
        parser.add_argument('-l', '--locale').completer = lambda **kw: localedata.locale_identifiers()
        super().set_arguments(parser)

    @classmethod
    def create_command(cls, **defaults):
        return super().create_command(
            input_file='${/i18n/extract/output_file}', domain='${/i18n/init/domain}', output_dir=''
        )

    def run_command(self, command, input_file, output_dir, services_service, **config):
        output_dir = output_dir or os.path.dirname(input_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        return services_service(super().run_command, command, input_file=input_file, output_dir=output_dir, **config)


class Compile(Command):
    def set_arguments(self, parser):
        parser.add_argument('-l', '--locale').completer = lambda **kw: localedata.locale_identifiers()
        super().set_arguments(parser)

    @classmethod
    def create_command(cls, **defaults):
        return super().create_command(
            input_file='${/i18n/extract/output_file}',
            directory='${/i18n/init/output_dir}',
            domain='${/i18n/init/domain}',
        )

    def run_command(self, command, input_file, directory, services_service, **config):
        directory = directory or os.path.dirname(input_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        return services_service(super().run_command, command, directory=directory, **config)
