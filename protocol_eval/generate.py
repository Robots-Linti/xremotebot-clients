#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""\
Generador de datos

Usage:
    generator <number_of_entries> <output>

Options:
    -h --help   Show this screen
"""
from __future__ import print_function
from __future__ import generators
from __future__ import unicode_literals
import six

from docopt import docopt
import sys
import json
import random
import uuid

if six.PY2:
    range = xrange
    uuid.UUID.hex = property(uuid.UUID.get_hex)


def randnum():
    return random.randint(0, 2**32 - 1)


def randstring():
    return uuid.uuid4().hex


def main(**kwargs):
    entries = int(kwargs['<number_of_entries>'])
    output = kwargs['<output>']
    root = {'root': []}

    for i in range(entries):
        root['root'].append({})
        for j in range(5):
            # 5 campos numéricos
            root['root'][-1][randstring()] = randnum()
            # 5 campos de tipo string
            root['root'][-1][randstring()] = randstring()
            # 5 campos con un objeto
            root['root'][-1][randstring()] = {randstring(): randnum()}
            # 5 campos con un array
            root['root'][-1][randstring()] = [randstring(), randstring()]

    with open(output, 'w') as f:
        json.dump(root, f)


if __name__ == '__main__':
    main(**docopt(__doc__))
