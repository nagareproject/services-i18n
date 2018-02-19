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


class I18NService(plugin.Plugin):
    LOAD_PRIORITY = 70
    CONFIG_SPEC = {}

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

    def __init__(self, name, dist, **config_commands):
        super(I18NService, self).__init__(name, dist)

        self.config_commands = config_commands

    @property
    def output_directory(self):
        return self._get_config_value(self.config_commands['compile']['directory'])

    def _get_config_value(self, v):
        if isinstance(v, str) and v.startswith('##'):
            _, _, command_name, v = v.split('#')
            v = self.config_commands[command_name][v]

        return v

    def run(self, command_name, command, **params):
        command.initialize_options()

        config = dict(self.config_commands[command_name], **params)
        for k, v in config.items():
            setattr(command, k, self._get_config_value(v))

        command.finalize_options()

        return command.run()
