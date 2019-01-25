# --
# Copyright (c) 2008-2019 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""Internationalization service
"""

import os

from nagare.admin import i18n
from nagare.services import plugin


def on_change(path, o, method):
    return getattr(o, method)(path)


class I18NService(plugin.Plugin):
    LOAD_PRIORITY = 70
    CONFIG_SPEC = {'reload': 'boolean(default=True)'}

    @classmethod
    def create_config_spec(cls, command_name, command):
        config_spec = {}

        for name, _, _ in command.user_options:
            name = name.strip('=')
            keyword = name.replace('-', '_')

            if name == getattr(command, 'as_args'):
                continue

            if name in command.boolean_options:
                spec = 'boolean(default=False)'
            elif name in command.multiple_value_options:
                spec = 'string_list(default=list())'
            else:
                default = getattr(command, keyword)
                choices = command.option_choices.get(name)

                args = 'default=' + ('None' if default is None else ('"%s"' % default))
                if choices:
                    args += ', option(' + ', '.join('"%s"' % choice for choice in choices) + ')'
                spec = 'string(' + args + ')'

            config_spec[keyword] = spec

        cls.CONFIG_SPEC[command_name] = config_spec

    def __init__(self, name, dist, reload, reloader_service=None, **config_commands):
        super(I18NService, self).__init__(name, dist)

        self.reload = reload
        self.reloader = reloader_service
        self.config_commands = config_commands

    @property
    def input_file(self):
        return self.config_commands['extract']['output_file']

    @property
    def input_directory(self):
        return self.config_commands['init']['output_dir']

    @property
    def output_directory(self):
        return self.config_commands['compile']['directory']

    def handle_start(self, app):
        if self.reload and self.reloader and self.input_directory and os.path.isdir(self.input_directory):
            po_files = []

            for root, dirs, files in os.walk(self.input_directory):
                po_files.extend(os.path.join(root, file) for file in files if file.endswith('.po'))

            self.reloader.watch_files([self.input_file], on_change, o=self, method='update_on_change')
            self.reloader.watch_files(po_files, on_change, o=self, method='compile_on_change')

    def update_on_change(self, path):
        i18n.Update().run(self)
        return False

    def compile_on_change(self, path):
        i18n.Compile().run(self)
        return True

    def run(self, command_name, command, **params):
        command.initialize_options()
        command.__dict__.update(self.config_commands[command_name])
        command.__dict__.update(params)
        command.finalize_options()

        return command.run()


for cls in (i18n.Extract, i18n.Init, i18n.Update, i18n.Compile):
    I18NService.create_config_spec(*cls.create_command())
