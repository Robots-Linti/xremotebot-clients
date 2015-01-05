#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""\
Benchmark

Usage:
    benchmark (json|bson|cbor) <repeat> <input>

Options:
    -h --help   Show this screen
"""
from __future__ import print_function
from __future__ import generators
from __future__ import unicode_literals
from six import iteritems
import six

from docopt import docopt
import sys
import json
import bson
import cbor
from chrono import Timer

if six.PY2:
    range = xrange


def json_load(raw):
    d = json.loads(raw)
    return d


def json_dump(data):
    s = json.dumps(data)
    return s

def bson_load(raw):
    d = bson.BSON.decode(raw)
    return d

def bson_dump(data):
    s = bson.BSON.encode(data)
    return s

def cbor_load(raw):
    d = cbor.loads(raw)
    return d

def cbor_dump(data):
    s = cbor.dumps(data)
    return s

def run(operation, data, avgs):
    with Timer() as timed:
        res = globals()[operation](data)

    avgs[operation] = avgs.get(operation, 0) + timed.elapsed
    print('{}: {:.4f} seconds'.format(operation, timed.elapsed))
    return res

def main(**kwargs):
    infile = kwargs['<input>']
    repeat = int(kwargs['<repeat>'])

    with open(infile) as f:
        data = json.load(f)

    serialization = list(
        filter(lambda kv: kv[0] in ['json', 'bson', 'cbor'] and kv[1],
               iteritems(kwargs)))[0][0]

    avgs = {}

    for i in range(repeat):
        raw = run('{}_dump'.format(serialization), data, avgs)
        run('{}_load'.format(serialization), raw, avgs)

    print('-' * 78)
    for operation, elapsed in iteritems(avgs):
        print('Promedio {}: {:.4f} seconds'.
              format(operation, elapsed / repeat))

    fun = globals()['{}_dump'.format(serialization)]
    print(
        'Tamaño {}: {:.4f} MiB'.format(
            serialization,
            len(fun(data)) / float(1048576)
            )
    )

if __name__ == '__main__':
    main(**docopt(__doc__))
