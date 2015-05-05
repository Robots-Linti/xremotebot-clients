#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='xremotebot',
      version='1.0',
      description='XRemoteBot official Python client',
      author='Fernando López',
      author_email='flopez@linti.unlp.edu.ar',
      url='https://github.com/fernandolopez/xremotebot-clients',
      packages=['xremotebot'],
      install_requires=[
            'websocket-client',
      ],
     )
