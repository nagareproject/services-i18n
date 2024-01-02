# --
# Copyright (c) 2008-2023 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""Internationalization service."""

import os

from nagare import i18n
from nagare.admin import i18n as i18n_commands
from nagare.services import plugin


def on_change(event, path, o, method, services):
    return (event.event_type in ('created', 'modified', 'moved')) and services(getattr(o, method), path)


class I18NService(plugin.Plugin):
    LOAD_PRIORITY = 70
    CONFIG_SPEC = dict(plugin.Plugin.CONFIG_SPEC, watch='boolean(default=True)')

    @classmethod
    def create_config_spec(cls, command_name, command):
        config_spec = {}

        if command_name == 'extract':
            config_spec['_root'] = 'string(default="$root")'
            config_spec[
                'relative_location'
            ] = 'boolean(default=False, help="if \\"add_location\\" is \\"full\\" or \\"file\\" generates file names relatives from the project root")'  # noqa: E501

        for name, _, description in command.user_options:
            name = name.strip('=')
            keyword = name.replace('-', '_')

            if name == getattr(command, 'as_args'):
                continue

            if (command_name == 'extract') and (keyword == 'input_dirs'):
                spec = 'string_list(default=list("{}")'.format(getattr(command, keyword))
            else:
                if name in command.boolean_options:
                    spec = 'boolean(default=False'
                elif name in command.multiple_value_options:
                    spec = 'string_list(default=list()'
                else:
                    default = getattr(command, keyword)
                    choices = command.option_choices.get(name)

                    default = 'default=' + ('None' if default is None else ('"%s"' % default))
                    if choices:
                        spec = 'option(' + ', '.join('"%s"' % choice for choice in choices) + ', ' + default
                    else:
                        spec = 'string(' + default

            spec += (', help="{}"'.format(description.replace('"', r'\"')) if description else '') + ')'

            config_spec[keyword] = spec

        config_spec['__many__'] = config_spec.copy()
        cls.CONFIG_SPEC[command_name] = config_spec

    @property
    def input_file(self):
        return self.plugin_config['extract']['output_file']

    @property
    def input_directory(self):
        return self.plugin_config['init']['output_dir'] or os.path.dirname(self.input_file)

    @property
    def output_directory(self):
        return self.plugin_config['compile']['directory'] or self.input_directory

    def handle_start(self, app, services_service, reloader_service=None):
        watch = self.plugin_config['watch']

        if watch and (reloader_service is not None) and self.input_directory and os.path.isdir(self.input_directory):
            for root, dirs, files in os.walk(self.input_directory):
                for filename in files:
                    if filename.endswith('.po'):
                        filename = os.path.join(root, filename)
                        reloader_service.watch_file(
                            filename, on_change, o=self, method='compile_on_change', services=services_service
                        )

            if os.path.isfile(self.input_file):
                reloader_service.watch_file(
                    self.input_file, on_change, o=self, method='update_on_change', services=services_service
                )

    def update_on_change(self, path, services_service):
        services_service(i18n_commands.Update().run)
        return None

    def compile_on_change(self, path, services_service):
        services_service(i18n_commands.Compile().run)
        i18n.invalidate_caches()
        return False


for cls in (i18n_commands.Extract, i18n_commands.Init, i18n_commands.Update, i18n_commands.Compile):
    I18NService.create_config_spec(*cls.create_command())
