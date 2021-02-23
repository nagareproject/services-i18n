# Encoding: utf-8

# --
# Copyright (c) 2008-2021 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

from os import path

from setuptools import setup, find_packages


here = path.normpath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as long_description:
    LONG_DESCRIPTION = long_description.read()

setup(
    name='nagare-services-i18n',
    author='Net-ng',
    author_email='alain.poirier@net-ng.com',
    description='i18n service',
    long_description=LONG_DESCRIPTION,
    license='BSD',
    keywords='',
    url='https://github.com/nagareproject/services-i18n',
    packages=find_packages(),
    zip_safe=False,
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    install_requires=['Babel>=2.5.0', 'pytz', 'nagare-services', 'nagare-server'],
    entry_points='''
        [nagare.commands]
        i18n = nagare.admin.i18n:Commands

        [nagare.commands.i18n]
        locales = nagare.admin.i18n:Locales
        extract = nagare.admin.i18n:Extract
        init = nagare.admin.i18n:Init
        update = nagare.admin.i18n:Update
        compile = nagare.admin.i18n:Compile

        [nagare.services]
        i18n = nagare.services.i18n:I18NService
    '''
)
